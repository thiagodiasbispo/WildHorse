import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from PyQt6.QtWidgets import QWidget

from apps.integrador_meli.controller import InserirCompatibilidadeController
from apps.integrador_meli.gui.ui.frm_inserir_compatibilidades_meli import Ui_FrmInserirCompatibilidadesMeli
from comum.widget_models import DataframeModel
from comum.widget_utils import escolher_panilha_excel


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
        mensagem = f"<font color='blue'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_error(self, mensagem):
        mensagem = f"<font color='red'>{mensagem}</font>"
        self._log_html(mensagem)

    def _log_html(self, mensagem):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ui.txtLogs.appendHtml(f"{now} - {mensagem}")

    def _inserir_compatibilidades(self):
        try:
            self._compatibilidade_controller.inserir_compatibilidade_por_planilha(self.planilha_compatibilidade,
                                                                                  self.planilha_associacao_atributos)
        except Exception as e:
            self._log_error(str(e))

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
        df = pd.read_excel(self.planilha_compatibilidade)
        if not (model := self.ui.tblCompatibilidades.model()):
            self.ui.tblCompatibilidades.setModel(DataframeModel(df))
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
