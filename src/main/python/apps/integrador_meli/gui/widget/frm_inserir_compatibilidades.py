import os

from PyQt6.QtWidgets import QWidget
from pathlib import Path

from apps.integrador_meli.controller import InserirCompatibilidadeController
from apps.integrador_meli.gui.ui.frm_inserir_compatibilidades_meli import Ui_FrmInserirCompatibilidadesMeli
from comum.widgets import escolher_panilha_excel


class FrmInserirCompatibilidadeMeli(QWidget):
    def __init__(self, *args, **kwargs):
        super(FrmInserirCompatibilidadeMeli, self).__init__(*args, **kwargs)
        self.ui = Ui_FrmInserirCompatibilidadesMeli()
        self.ui.setupUi(self)
        self.ui.btnAbrirPlanilhaCompatibilidade.clicked.connect(self._abrir_planilha_compatibilidade)
        self.ui.btnPlanilhaMarcaModelosAnos.clicked.connect(self._abrir_panilha_marca_modelo_ano)
        self.ui.btnInserirCompatibilidades.clicked.connect(self._inserir_compatibilidades)

        self._compatibilidade_controller = InserirCompatibilidadeController()


    def _inserir_compatibilidades(self):
        self._compatibilidade_controller.inserir_compatibilidade_por_planilha(self.planilha_compatibilidade, self.planilha_compatibilidade)


    def _abrir_planilha_compatibilidade(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)

        arquivo = escolher_panilha_excel(self, titulo ="Selecione a planilha de compatibilidade", directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaCompatibilidade.setText(arquivo)

    def _abrir_panilha_marca_modelo_ano(self):
        diretorio = os.getenv("USERPROFILE")

        if self.planilha_compatibilidade:
            diretorio = str(Path(self.planilha_compatibilidade).parent)
        elif self.planilha_associacao_atributos:
            diretorio = str(Path(self.planilha_associacao_atributos).parent)

        arquivo = escolher_panilha_excel(self, titulo="Selecione a planilha com relação de marca, modelo e ano", directory=diretorio)

        if arquivo:
            self.ui.edtPlanilhaAssociacaoAtributos.setText(arquivo)


    @property
    def planilha_compatibilidade(self):
        return self.ui.edtPlanilhaCompatibilidade.text().strip()

    @property
    def planilha_associacao_atributos(self):
        return self.ui.edtPlanilhaAssociacaoAtributos.text().strip()