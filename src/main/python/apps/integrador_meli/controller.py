import functools
import traceback
from itertools import chain
from pathlib import Path

import numpy as np
import pandas as pd

from comum.configuracoes.configuracao_meli_service import ler_configuracoes_api_meli
from dominio.meli.api.controller.comum import RequisitionAwaiter
from dominio.meli.api.controller_factory import MeliApiControllerFactory
from dominio.meli.api.models import CompatibilidadeAtributoCarroPost, CompatibilidadeAtributoCarroVariosPost


def _ano_informado(ano):
    try:
        return not np.isnan(ano)
    except TypeError:
        return bool(ano)


class InserirCompatibilidadeController(RequisitionAwaiter):
    MARCA = "Marca"
    MARCA_ID = "Marca ID"
    MODELO = "Modelo"
    MODELO_ID = "Modelo ID"
    ANO_INICIAL = "Ano Inicial"
    ANO_FINAL = "Ano Final"
    ANOS = "Anos"
    ANOS_NOME = "Ano Nome"
    MLB = "MLB"

    def __init__(self):
        RequisitionAwaiter.__init__(self, tempo_espera=0.4)
        config = ler_configuracoes_api_meli()
        factory = MeliApiControllerFactory(config)

        self._catalogo_dominio_controller = factory.catalogo_dominio_controller
        self._compatibilidade_controller = factory.compatibilidade_controller

    def _validar_planilha_colunas(self, df, nome_planilha, colunas_esperadas):
        nome_planilha = Path(nome_planilha).name
        colunas_faltantes = [col for col in colunas_esperadas if col not in df.columns]
        if colunas_faltantes:
            raise ValueError(f"Colunas faltantes na planilha '{nome_planilha}': {', '.join(colunas_faltantes)}")

    def _validar_planilha_valores(self, df, nome_planilha, coluna, valores_permitidos):
        nome_planilha = Path(nome_planilha).name
        valores_invalidos = df[coluna][~df[coluna].isin(valores_permitidos)].unique()
        if valores_invalidos.size > 0:
            raise ValueError(
                f"Valores inválidos na coluna '{coluna}' da planilha '{nome_planilha}': {', '.join(map(str, valores_invalidos))}")

    def _validar_anos_validos(self, df, nome_planilha):
        nome_planilha = Path(nome_planilha).name

        if (df[self.ANO_FINAL] < df[self.ANO_INICIAL]).any():
            raise ValueError(
                f"Os anos na planilha {nome_planilha} estão inconsistentes: 'ano_final' deve ser maior ou igual a 'ano_inicial'.")

        for ano in [self.ANO_INICIAL, self.ANO_FINAL]:
            anos_nao_vazios = df[ano][~df[ano].isna()]
            anos_invalidos = anos_nao_vazios[~anos_nao_vazios.astype(str).str.match(r'^\d{4}$')].unique()
            if anos_invalidos.size > 0:
                raise ValueError(
                    f"Anos inválidos na coluna '{ano}' da planilha '{nome_planilha}': {', '.join(map(str, anos_invalidos))}")

    def get_ids_meli_correspondentes(self, df_compat, df_associacao):
        marca_map = {r[self.MARCA]: r[self.MARCA_ID] for _, r in
                     df_associacao[[self.MARCA, self.MARCA_ID]].drop_duplicates().iterrows()}

        modelo_map = {r[self.MODELO]: r[self.MODELO_ID] for _, r in
                      df_associacao[[self.MODELO, self.MODELO_ID]].drop_duplicates().iterrows()}

        df_compat = df_compat.copy()

        df_compat[self.MARCA_ID] = df_compat[self.MARCA].map(marca_map)
        df_compat[self.MODELO_ID] = df_compat[self.MODELO].map(modelo_map)

        assert len(df_compat) == len(
            df_compat), "Erro ao obter IDs correspondentes. Verifique as planilhas de compatibilidade e associação."

        return df_compat.reset_index()

    def ler_planilha_compatibilidade(self, planilha_compatibilidade):
        print("Lendo planilha de compatibilidade:", planilha_compatibilidade)
        df = pd.read_excel(planilha_compatibilidade, dtype={self.MARCA: str, self.MODELO: str})
        return df

    @functools.lru_cache(maxsize=1024)
    def anos_disponiveis(self, marca_id: str, modelo_id: str):
        self._await()
        return self._catalogo_dominio_controller.get_anos_marca_modelo(marca_id, modelo_id)

    def _expandir_anos(self, ano_inicial, ano_final, marca_id, modelo_id) -> list[str]:
        anos_disponiveis = self.anos_disponiveis(marca_id, modelo_id)

        anos_disponiveis = [a.to_dict() for a in anos_disponiveis]
        anos_disponiveis = pd.DataFrame(anos_disponiveis)
        anos_disponiveis["name"] = anos_disponiveis["name"].astype(int)

        # ano_inicial = ano_inicial if _ano_informado(ano_inicial) else ""
        # ano_final = ano_final if _ano_informado(ano_final) else ""

        if not ano_inicial and not ano_final:
            anos = anos_disponiveis
        elif ano_final == ano_inicial:
            ano_final = int(ano_final)
            anos = anos_disponiveis.query('name == @ano_final')
        elif ano_final and ano_inicial:
            ano_final = int(ano_final)
            ano_inicial = int(ano_inicial)
            anos = anos_disponiveis.query("name >= @ano_inicial and name <= @ano_final")
        elif ano_inicial and not ano_final:  # Todos a partir do ano inicial
            ano_inicial = int(ano_inicial)
            anos = anos_disponiveis.query("name >= @ano_inicial")
        else:  # Todos  até o ano final
            ano_final = int(ano_final)
            anos = anos_disponiveis.query("name <= @ano_final")

        return list(map(str, anos["name"].values))

    def expandir_planilha_compatibilidade(self, df_compat, df_associacao):
        df = self.get_ids_meli_correspondentes(df_compat, df_associacao)
        df = df.sort_values(by=[self.MLB])

        for mlb, group in df.groupby(self.MLB):
            data_list = []
            for _, row in group.iterrows():
                ano_inicial = row[self.ANO_INICIAL]
                ano_final = row[self.ANO_FINAL]

                ano_inicial = ano_inicial if _ano_informado(ano_inicial) else ""
                ano_final = ano_final if _ano_informado(ano_final) else ""

                data = {self.MARCA_ID: str(row[self.MARCA_ID]),
                        self.MARCA: str(row[self.MARCA]),
                        self.MODELO: str(row[self.MODELO]),
                        self.MODELO_ID: str(row[self.MODELO_ID]),
                        self.MLB: str(row[self.MLB]),
                        "ano_inicial": ano_inicial,
                        "ano_final": ano_final, }

                anos = self._expandir_anos(ano_inicial, ano_final, data[self.MARCA_ID], data[self.MODELO_ID])

                data[self.ANOS_NOME] = anos
                data_list.append(data)
            maximo = self._compatibilidade_controller.QUANTIDADE_MAXIMA_DE_INSERCAO_POR_DOMINIO
            if len(data_list) <= maximo:
                yield mlb, data_list
            else:
                for i in range(0, len(data_list), maximo):
                    yield mlb, data_list[i:i + maximo]

    def inserir_compatibilidade_por_planilha(self, planilha_compatibilidade, planilha_associacao_atributos):
        try:
            yield True, f"Relendo planilha de compatibilidades", None, ""
            df_compat = self.ler_planilha_compatibilidade(planilha_compatibilidade)
            df_associacao = pd.read_excel(planilha_associacao_atributos)

            yield True, f"Validando valores em colunas", None, ""
            self._validar_planilha_colunas(df_compat, planilha_compatibilidade,
                                           [self.MARCA, self.MODELO, self.ANO_INICIAL,
                                            self.ANO_FINAL, self.MLB])

            self._validar_planilha_colunas(df_associacao, planilha_associacao_atributos,
                                           [self.MARCA, self.MARCA_ID, self.MODELO, self.MODELO_ID])

            for coluna in [self.MARCA, self.MODELO]:
                self._validar_planilha_valores(df_compat, planilha_compatibilidade, coluna,
                                               df_associacao[coluna].unique())

            self._validar_anos_validos(df_compat, planilha_compatibilidade)

            yield True, f"Associando Ids de marcas e modelos", None, ""
            compatibilidades_expandidas = self.expandir_planilha_compatibilidade(df_compat, df_associacao)

        except Exception as e:
            yield False, None, None, str(e)
            traceback.print_exc()
            return

        for mlb, data_list in compatibilidades_expandidas:

            marcas = sorted(set([data[self.MARCA] for data in data_list]))
            modelos = sorted(set([data[self.MODELO] for data in data_list]))
            anos = chain.from_iterable([data[self.ANOS_NOME] for data in data_list])
            anos = sorted(set(anos))

            marcas = ', '.join(marcas)
            modelos = ', '.join(modelos)
            anos = ', '.join(map(str, anos))

            descricao = f"{mlb} Marcas: [{marcas}] Modelos: [{modelos}] Anos: [{anos}]"

            compatibilidades = []

            for data in data_list:
                if not data[self.ANOS]:
                    yield False, mlb, None, f"Nenhum ano disponível para {data[self.MARCA]} {data[self.MODELO]}."
                    continue

                compat_marca = CompatibilidadeAtributoCarroPost(id=self._compatibilidade_controller.MARCA,
                                                                value_id=data[self.MARCA_ID])

                compat_modelo = CompatibilidadeAtributoCarroPost(id=self._compatibilidade_controller.MODELO,
                                                                 value_id=data[self.MODELO_ID])

                compat_ano = CompatibilidadeAtributoCarroVariosPost(id=self._compatibilidade_controller.ANO,
                                                                    value_ids=data[self.ANOS])

                compatibilidades.append([compat_marca, compat_modelo, compat_ano])

            try:
                self._await()
                if compatibilidades:
                    result = self._compatibilidade_controller.post_compatibilidade_por_dominio(mlb,
                                                                                               *compatibilidades)
                    yield True, descricao, result, ""
                else:
                    yield False, descricao, None, f"{mlb} - Nenhuma compatibilidade encontrada para inserção."
                # yield True, f"Inseridas {len(data_list)} compatibilidades:", None, ""
            except Exception as e:
                yield False, descricao, None, str(e)
