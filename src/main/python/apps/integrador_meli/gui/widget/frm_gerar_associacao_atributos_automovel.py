import traceback
from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.gui.ui.frm_gerar_associacao_atributos_automovel import Ui_frmGeradorAssociadoMarcaModeloAno
from apps.integrador_meli.models import AssociacaoAtributosAutomovel
from comum.assincrono import ExecutorAssincronaDeFuncaoGeradora
from comum.widget_models import ItemModelObjectAttributeBased
from comum.widget_utils import escolher_diretorio, mostrar_mensagem_erro
from dominio.meli.api.autenticacao_utils import usuario_esta_autenticado
from dominio.meli.api.controller.catalogo_de_dominio import CatalogoDeDominioController
from dominio.meli.api.controller_factory import get_factory
from wild_horse.gui.widget.frm_barra_progresso_para_operacao_assincrona import FrmBarraProgressoParaExecucaoAssincrona


class AssociacaoAtributosAutomovelModel(ItemModelObjectAttributeBased):
    def __init__(self):
        atributos = {"marca": "Marca", "marca_id": "Marca ID", "modelo": "Modelo", "modelo_id": "Modelo ID"}
        super().__init__(atributos)


class FrmGerarAssociacaoAtributosAutomovel(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmGerarAssociacaoAtributosAutomovel, self).__init__(*args, **kwargs)
        self.ui = Ui_frmGeradorAssociadoMarcaModeloAno()
        self.ui.setupUi(self)

        self.ui.btnInformarDiretorio.clicked.connect(self._informar_diretorio_destino)
        self.ui.btnGerarAssociacoes.clicked.connect(self._gerar_associacoes)

        self.ui.tblAssociacoes.setModel(AssociacaoAtributosAutomovelModel())

        self._catalogo_controller = self._get_catalogo_controller()

    @property
    def _arquivo_destino(self):
        return self.ui.edtDiretorioDestino.text()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.ui.tblAssociacoes.resizeColumnsToContents()

    def _get_catalogo_controller(self) -> CatalogoDeDominioController:
        return get_factory().catalogo_dominio_controller

    def _criar_listador_associacoes(self):
        def listar():
            batch_size = 150
            batch = []
            for marca in self._catalogo_controller.get_marcas():
                for modelo in self._catalogo_controller.get_modelos_marca(marca.id):
                    batch.append(AssociacaoAtributosAutomovel(marca=marca.name,
                                                              marca_id=marca.id,
                                                              modelo=modelo.name,
                                                              modelo_id=modelo.id))
                    if len(batch) == batch_size:
                        yield batch
                        batch = []
            if batch:
                yield batch

        gerador_anuncios = ExecutorAssincronaDeFuncaoGeradora(listar, parent=self)
        gerador_anuncios.erro_no_carregamento.connect(self._erro_no_carregamento)
        gerador_anuncios.carregamento_finalizado.connect(self._carregamento_finalizado)

        return gerador_anuncios

    def _criar_barra_progresso_de_carregamento_de_anuncio(self, litador_associacoes):
        return FrmBarraProgressoParaExecucaoAssincrona(litador_associacoes, parent=self,
                                                       mensagem="Listando associações")

    def _gerar_associacoes(self):
        try:
            if not usuario_esta_autenticado():
                mostrar_mensagem_erro(
                    self,
                    titulo="Usuário não autenticado",
                    mensagem="É necessário autenticar o usuário antes de gerar as associações.\n A autenticação pode ser realizada na tela de Configurações.",
                )
                return

            self.ui.tblAssociacoes.model().clear()
            listador_associacoes = self._criar_listador_associacoes()
            frm_barra_progresso = self._criar_barra_progresso_de_carregamento_de_anuncio(listador_associacoes)

            frm_barra_progresso.iniciar_carregamento_assincrono(
                callback_novos_dados_carregados=self._novas_associacoes_carregadas)

        except Exception as e:
            mostrar_mensagem_erro(self, mensagem=f"Erro baixar associações: {e}")
            traceback.print_exc()

    def _log_info(self, mensagem):
        mensagem = f"<font color='blue'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_error(self, mensagem):
        mensagem = f"<font color='red'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_html(self, mensagem):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ui.txtLogs.appendHtml(f"{now} - {mensagem}")

    def _exportar_associacoes(self):
        try:
            itens = self.ui.tblAssociacoes.model().get_itens()
            df = pd.DataFrame(itens)
            df.to_excel(self._arquivo_destino, index=False)
            self._log_info(f"Associações exportadas para: {self._arquivo_destino}")
        except Exception as e:
            self._log_error(f"Erro ao exportar associações: {e}")
            traceback.print_exc()

    def _carregamento_finalizado(self):
        self._log_info(f"Total de itens carregados: {self.ui.tblAssociacoes.model().rowCount()}")
        self._exportar_associacoes()

    def _novas_associacoes_carregadas(self, associacoes: Iterable[AssociacaoAtributosAutomovel]):
        self.ui.tblAssociacoes.model().add_itens(associacoes)
        self.ui.tblAssociacoes.resizeColumnsToContents()

    def _erro_no_carregamento(self, mensagem: str):
        print(mensagem)
        mostrar_mensagem_erro(
            self, titulo="Erro na geração das associações!", mensagem=mensagem
        )

    @staticmethod
    def _get_nome_arquivo():
        data = date.today().strftime("%d.%m.%Y")
        return f"atributos_automovel_{data}.xlsx"

    def _informar_diretorio_destino(self):
        diretorio = escolher_diretorio(self)
        if diretorio:
            nome_arquivo = Path(diretorio) / self._get_nome_arquivo()
            self.ui.edtDiretorioDestino.setText(str(nome_arquivo))
        else:
            self.ui.edtDiretorioDestino.clear()

        self.ui.btnGerarAssociacoes.setEnabled(bool(diretorio))
