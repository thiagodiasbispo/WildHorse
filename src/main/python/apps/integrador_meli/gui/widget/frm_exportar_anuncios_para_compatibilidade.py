from collections.abc import Iterable
from datetime import date
from pathlib import Path
import pandas as pd

from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.gui.ui.frm_exportar_anuncios_para_compatibilidade import \
    Ui_FrmExportarAnunciosParaCompatibilidade
from comum.assincrono import ExecutorAssincronaDeFuncaoGeradora
from comum.widget_models import ItemModelObjectAttributeBased
from comum.widget_utils import escolher_diretorio, mostrar_mensagem_erro, mostrar_mensagem_sucesso
from dominio.meli.api.autenticacao_utils import usuario_esta_autenticado
from dominio.meli.api.controller_factory import get_factory
from dominio.meli.api.models import ProdutosAnunciadosModel
from wild_horse.gui.widget.frm_barra_progresso_para_operacao_assincrona import FrmBarraProgressoParaExecucaoAssincrona


class AnunciosCompatibilidadeModel(ItemModelObjectAttributeBased):
    def __init__(self):
        atributos = {"sku": "SKU", "mlb": "MLB", "title": "Título",
                     "requer_compatibilidade": "Requer compatibilidade",
                     "tem_sugestao_compabilidade": "Tem sugestão de compatabilidade"}

        def sim_nao(x):
            return "Sim" if x else "Não"

        formatador = {"tem_sugestao_compabilidade": sim_nao,
                      "requer_compatibilidade": sim_nao}

        super().__init__(atributos, formatador)


class FrmExportarAnunciosParaCompatibilidade(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmExportarAnunciosParaCompatibilidade, self).__init__(*args, **kwargs)
        self.ui = Ui_FrmExportarAnunciosParaCompatibilidade()
        self.ui.setupUi(self)

        self.ui.btnInformarDiretorio.clicked.connect(self._informar_diretorio_destino)
        self.ui.btnExportarAnuncios.clicked.connect(self._exportar_anuncios)

        self._anuncio_controller = get_factory().anuncio_controller

        self.ui.tblAnuncios.setModel(AnunciosCompatibilidadeModel())

    def _novo_anuncio_carregado(self, novos_anuncios: Iterable[ProdutosAnunciadosModel]):
        self.ui.tblAnuncios.model().add_itens(novos_anuncios)
        self.ui.tblAnuncios.resizeColumnsToContents()

    def _erro_no_carregamento(self, mensagem):
        mostrar_mensagem_erro(self, titulo="Erro!", mensagem=f"Erro no carregamento dos anúncios: {mensagem}")

    @property
    def get_arquivo_destino(self):
        return self.ui.edtArquivoDestino.text()

    def _carregamento_de_anuncios_finalizado(self):
        itens = self.ui.tblAnuncios.model().get_itens()
        df = pd.DataFrame(itens)
        df.to_excel(self.get_arquivo_destino, index=False)
        mostrar_mensagem_sucesso(self, mensagem="Anúncios exportados com sucesso")

    def _criar_carregador_assincrono_de_anuncios(self):
        def listar_anuncios():
            batch_size = 100
            batch = []
            for anuncio in self._anuncio_controller.get_produtos_anunciados_com_informacoes_de_compatabilidade():
                batch.append(anuncio)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            if batch:
                yield batch

        gerador_anuncios = ExecutorAssincronaDeFuncaoGeradora(listar_anuncios)
        gerador_anuncios.erro_no_carregamento.connect(self._erro_no_carregamento)
        gerador_anuncios.carregamento_finalizado.connect(self._carregamento_de_anuncios_finalizado)
        return gerador_anuncios

    def _criar_barra_progresso_de_carregamento_de_anuncio(self, gerador_anuncios):
        frm_barra_progresso = FrmBarraProgressoParaExecucaoAssincrona(gerador_anuncios, mensagem="Carregando anúncios")
        return frm_barra_progresso

    def _exportar_anuncios(self):
        if not usuario_esta_autenticado():
            mostrar_mensagem_erro(self, titulo="Erro de autenticação",
                                  mensagem="Você não está autenticado! Autentique-se na tela de Configurações da Mercado Livre.")
            return

        self.ui.tblAnuncios.model().clear()

        gerador_anuncios = self._criar_carregador_assincrono_de_anuncios()
        frm_barra_progresso = self._criar_barra_progresso_de_carregamento_de_anuncio(gerador_anuncios)
        frm_barra_progresso.iniciar_carregamento_assincrono(
            callback_novos_dados_carregados=self._novo_anuncio_carregado)

    @staticmethod
    def _get_nome_arquivo():
        data = date.today().strftime("%d.%m.%Y")
        return f"anuncios_{data}.xlsx"

    def _informar_diretorio_destino(self):
        diretorio = escolher_diretorio(self)
        if diretorio:
            nome_arquivo = Path(diretorio) / self._get_nome_arquivo()
            self.ui.edtArquivoDestino.setText(str(nome_arquivo))
        else:
            self.ui.edtArquivoDestino.clear()

        self.ui.btnExportarAnuncios.setEnabled(bool(diretorio))
