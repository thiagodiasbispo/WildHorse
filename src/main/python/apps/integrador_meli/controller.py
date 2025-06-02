from pathlib import Path

import pandas as pd

from comum.configuracoes.configuracao_meli_service import ler_configuracoes_api_meli
from dominio.meli.api.controller.comum import RequisitionAwaiter
from dominio.meli.api.controller_factory import MeliApiControllerFactory
from dominio.meli.api.models import CompatibilidadeAtributoCarroPost, CompatibilidadeAtributoCarroVariosPost


class InserirCompatibilidadeController(RequisitionAwaiter):
    MARCA = "marca"
    MARCA_ID = "marca_id"
    MODELO = "modelo"
    MODELO_ID = "modelo_id"
    ANO_INICIAL = "ano_inicial"
    ANO_FINAL = "ano_final"
    ANOS = "anos"
    MLB = "mlb"

    def __init__(self):
        RequisitionAwaiter.__init__(self)
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
            anos_nao_vazios = df[ano].dropna().astype(int)
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

        df_compat.to_excel(r"G:\Meu Drive\Freelas\Carlos_WildHorse\merge.xlsx")

        assert len(df_compat) == len(
            df_compat), "Erro ao obter IDs correspondentes. Verifique as planilhas de compatibilidade e associação."

        return df_compat.reset_index()

    def expandir_planilha_compatibilidade(self, df_compat, df_associacao) -> list[dict]:
        df = self.get_ids_meli_correspondentes(df_compat, df_associacao)
        data_list = []

        for _, row in df.iterrows():
            ano_final = row[self.ANO_FINAL]
            ano_inicial = row[self.ANO_INICIAL]
            data = {self.MARCA_ID: row[self.MARCA_ID], self.MODELO_ID: row[self.MODELO_ID], self.MLB: row[self.MLB]}

            if ano_final == ano_inicial:
                anos = [int(ano_inicial)]
            else:
                self._await()
                anos_disponiveis = self._catalogo_dominio_controller.get_anos_marca_modelo(data[self.MARCA_ID],
                                                                                           data[self.MODELO_ID])
                anos_disponiveis = [a.to_dict() for a in anos_disponiveis]
                anos_disponiveis = pd.DataFrame(anos_disponiveis)

                if not (ano_final and ano_inicial):
                    anos = anos_disponiveis["id"].values
                elif ano_final and ano_inicial:
                    anos = anos_disponiveis[
                        (anos_disponiveis["name"] >= ano_inicial) & (anos_disponiveis["name"] <= ano_final)][
                        "id"].values
                elif ano_inicial and not ano_final:  # Todos a partir do ano inicial
                    anos = anos_disponiveis[anos_disponiveis["name"] >= ano_inicial]["id"].values
                else:  # Todos a partir até o ano final
                    anos = anos_disponiveis[anos_disponiveis["name"] <= ano_final]["id"].values

            data[self.ANOS] = anos
            data_list.append(data)
        return data_list

    def inserir_compatibilidade_por_planilha(self, planilha_compatibilidade, planilha_associacao_atributos):
        df_compat = pd.read_excel(planilha_compatibilidade)
        df_associacao = pd.read_excel(planilha_associacao_atributos)

        self._validar_planilha_colunas(df_compat, planilha_compatibilidade,
                                       [self.MARCA, self.MODELO, self.ANO_INICIAL,
                                        self.ANO_FINAL, self.MLB])
        self._validar_planilha_colunas(df_associacao, planilha_associacao_atributos,
                                       [self.MARCA, self.MARCA_ID, self.MODELO, self.MODELO_ID])

        for coluna in [self.MARCA, self.MODELO]:
            self._validar_planilha_valores(df_compat, planilha_compatibilidade, coluna,
                                           df_associacao[coluna].unique())

        self._validar_anos_validos(df_compat, planilha_compatibilidade)

        data_list = self.expandir_planilha_compatibilidade(df_compat, df_associacao)

        for data in data_list:
            print(data)
            compat_marca = CompatibilidadeAtributoCarroPost(id=self._compatibilidade_controller.MARCA,
                                                            value_id=data[self.MARCA_ID])

            compat_modelo = CompatibilidadeAtributoCarroPost(id=self._compatibilidade_controller.MODELO,
                                                             value_id=data[self.MODELO_ID])

            compat_ano = CompatibilidadeAtributoCarroVariosPost(id=self._compatibilidade_controller.ANO,
                                                                value_ids=data[self.ANOS])

            compatibilidades = [compat_marca, compat_modelo, compat_ano]
            # self._await()
            # self._compatibilidade_controller.post_compatibilidade_por_dominio(data[self.MLB], compatibilidades)
