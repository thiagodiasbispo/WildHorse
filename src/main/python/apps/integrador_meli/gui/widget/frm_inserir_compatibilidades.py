import os
import traceback
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.controller import InserirCompatibilidadeController
from apps.integrador_meli.gui.ui.frm_inserir_compatibilidades_meli import Ui_FrmInserirCompatibilidadesMeli
from comum.widget_models import TableDataframeModel
from comum.widget_utils import escolher_panilha_excel, mostrar_mensagem_erro
from dominio.meli.api.autenticacao_utils import usuario_esta_autenticado


class FrmInserirCompatibilidadeMeli(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmInserirCompatibilidadeMeli, self).__init__(*args, **kwargs)
        self.ui = Ui_FrmInserirCompatibilidadesMeli()
        self.ui.setupUi(self)
        self.ui.btnAbrirPlanilhaCompatibilidade.clicked.connect(self._abrir_planilha_compatibilidade)
        self.ui.btnPlanilhaMarcaModelosAnos.clicked.connect(self._abrir_panilha_marca_modelo_ano)
        self.ui.btnInserirCompatibilidades.clicked.connect(self._inserir_compatibilidades)
        self._compatibilidade_controller = InserirCompatibilidadeController()

    def _log_info(self, mensagem):
        mensagem = f"<font color='white'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_error(self, mensagem):
        mensagem = f"<font color='red'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_html(self, mensagem):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ui.txtLogs.appendHtml(f"{now} - {mensagem}")

    def _inserir_compatibilidades(self):
        try:
            if not usuario_esta_autenticado():
                mostrar_mensagem_erro(self, titulo="Erro de autenticação",
                                      mensagem="Você não está autenticado! Autentique-se na tela de Configurações da Mercado Livre.")
                return
            gerador = self._compatibilidade_controller.inserir_compatibilidade_por_planilha(self.planilha_compatibilidade,
                                                                                  self.planilha_associacao_atributos)
            for mlb, compat_result in gerador:
               self._log_info(f"Compatibilidades inserida para o MLB {mlb}: {compat_result.created_compatibilities_count}")

        except Exception as e:
            self._log_error(str(e))
            traceback.print_exc()

    def _habilitar_botao_inserir_compatibilidades(self):
        habilitar = bool(self.planilha_compatibilidade) and bool(self.planilha_associacao_atributos)
        self.ui.btnInserirCompatibilidades.setEnabled(habilitar)

    def _abrir_planilha_compatibilidade(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)

        arquivo = escolher_panilha_excel(self, titulo="Selecione a planilha de compatibilidade", directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaCompatibilidade.setText(arquivo)

        self._habilitar_botao_inserir_compatibilidades()
        self._atualizar_tabela_compatibilidades()

    def _atualizar_tabela_compatibilidades(self):
        df = self._compatibilidade_controller.ler_planilha_compatibilidade(self.planilha_compatibilidade)
        if not (model := self.ui.tblCompatibilidades.model()):
            self.ui.tblCompatibilidades.setModel(TableDataframeModel(df))
        else:
            model.set_df(df)
        self.ui.tblCompatibilidades.resizeColumnsToContents()

    def _abrir_panilha_marca_modelo_ano(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)
        elif self.planilha_associacao_atributos:
            diretorio = str(Path(self.planilha_associacao_atributos).parent)

        arquivo = escolher_panilha_excel(self, titulo="Selecione a planilha com relação de marca e modelo",
                                         directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaAssociacaoAtributos.setText(arquivo)

        self._habilitar_botao_inserir_compatibilidades()

    @property
    def planilha_compatibilidade(self):
        return self.ui.edtPlanilhaCompatibilidade.text().strip()

    @property
    def planilha_associacao_atributos(self):
        return self.ui.edtPlanilhaAssociacaoAtributos.text().strip()
