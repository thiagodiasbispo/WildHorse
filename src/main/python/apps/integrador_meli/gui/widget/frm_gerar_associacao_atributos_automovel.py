import traceback
from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.gui.ui.frm_gerar_associacao_atributos_automovel import Ui_frmGeradorAssociadoMarcaModeloAno
from apps.integrador_meli.gui.widget.models import AssociacaoAtributosAutomovelModel
from apps.integrador_meli.models import AssociacaoAtributosAutomovel
from comum.configuracoes.configuracao_meli_service import ler_configuracoes_api_meli
from comum.widgets import escolher_diretorio, mostrar_mensagem_erro
from dominio.meli.api.autenticacao_utils import usuario_esta_autenticado
from dominio.meli.api.controller.catalogo_de_dominio import CatalogoDeDominioController
from dominio.meli.api.controller_factory import MeliApiControllerFactory
from wild_horse.gui.widget.frm_barra_progresso import FrmBarraProgressoWindow


class GeradorAssincronoDeAtributosDeAutomovel(QThread):
    novos_dados_carregados = pyqtSignal(object)
    erro_no_carregamento = pyqtSignal(str)

    def __init__(self, funcao_geradora, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._funcao_geradora = funcao_geradora

    def run(self):
        try:
            for data in self._funcao_geradora():
                if self.isInterruptionRequested():
                    return
                self.novos_dados_carregados.emit(data)
        except Exception as e:
            self.erro_no_carregamento.emit(str(e))
            traceback.print_exc()


class FrmGerarAssociacaoAtributosAutomovel(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmGerarAssociacaoAtributosAutomovel, self).__init__(*args, **kwargs)
        self.ui = Ui_frmGeradorAssociadoMarcaModeloAno()
        self.ui.setupUi(self)
        self.ui.btnInformarDiretorio.clicked.connect(self._informar_diretorio_destino)
        self.ui.btnGerarAssociacoes.clicked.connect(self._gerar_associacoes)

        self.ui.tblAssociacoes.setModel(AssociacaoAtributosAutomovelModel())

    @property
    def _arquivo_destino(self):
        return self.ui.edtDiretorioDestino.text()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.ui.tblAssociacoes.resizeColumnsToContents()

    def _get_catalogo_controller(self) -> CatalogoDeDominioController:
        config = ler_configuracoes_api_meli()
        return MeliApiControllerFactory(config).catalogo_dominio_controller

    def _gerar_associacoes(self):
        try:
            catalogo_controller = self._get_catalogo_controller()
            self.ui.tblAssociacoes.model().clear()

            if not usuario_esta_autenticado():
                mostrar_mensagem_erro(
                    self,
                    titulo="Usuário não autenticado",
                    mensagem="É necessário autenticar o usuário antes de gerar as associações.\n A autenticação pode ser realizada na tela de Configurações.",
                )
                return

            def get_associacoes():
                batch_size = 150
                batch = []
                for marca in catalogo_controller.get_marcas():
                    for modelo in catalogo_controller.get_modelos_marca(marca.id):
                        batch.append(AssociacaoAtributosAutomovel(marca=marca.name,
                                                                  marca_id=marca.id,
                                                                  modelo=modelo.name,
                                                                  modelo_id=modelo.id))
                        if len(batch) == batch_size:
                            yield batch
                            batch = []
                if batch:
                    yield batch

            self._iniciar_carregamento_assincrono(
                mensagem="Carregando atributos",
                funcao=get_associacoes,
                callback=self._novas_associacoes_carregadas,
            )

            self.frm_barra_progresso.accepted.connect(
                self._carregamento_finalizado
            )

            self.frm_barra_progresso.rejected.connect(
                self._carregamento_finalizado
            )
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
            associacoes = self.ui.tblAssociacoes.model().get_data()
            associacoes_dict = [a.to_dict() for a in associacoes]
            pd.DataFrame(associacoes_dict).to_excel(self._arquivo_destino, index=False)
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
        mostrar_mensagem_erro(
            self, titulo="Erro na geração das associações!", mensagem=mensagem
        )

    def _iniciar_carregamento_assincrono(self, mensagem, funcao, callback=None):
        self.frm_barra_progresso = FrmBarraProgressoWindow(self)
        self.frm_barra_progresso.set_mensagem(mensagem)

        self._gerador_assincrono_atributos = GeradorAssincronoDeAtributosDeAutomovel(
            funcao
        )

        self.frm_barra_progresso.rejected.connect(
            self._gerador_assincrono_atributos.requestInterruption
        )

        self._gerador_assincrono_atributos.erro_no_carregamento.connect(
            self.frm_barra_progresso.close
        )

        self._gerador_assincrono_atributos.finished.connect(
            self.frm_barra_progresso.close
        )

        if callback:
            self._gerador_assincrono_atributos.novos_dados_carregados.connect(
                callback
            )

        self._gerador_assincrono_atributos.novos_dados_carregados.connect(
            lambda _: self.frm_barra_progresso.incremento(10)
        )
        self._gerador_assincrono_atributos.erro_no_carregamento.connect(
            self._erro_no_carregamento
        )

        self.frm_barra_progresso.open()
        self._gerador_assincrono_atributos.start()

    @staticmethod
    def _get_nome_arquivo():
        data = date.today().strftime("%d%m%Y")
        return f"atributos_automovel_{data}.xlsx"

    def _informar_diretorio_destino(self):
        diretorio = escolher_diretorio(self)
        if diretorio:
            nome_arquivo = Path(diretorio) / self._get_nome_arquivo()
            self.ui.edtDiretorioDestino.setText(str(nome_arquivo))
        else:
            self.ui.edtDiretorioDestino.clear()

        self.ui.btnGerarAssociacoes.setEnabled(bool(diretorio))
