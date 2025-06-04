from typing import Type

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QMenu
from fbs_runtime.application_context.PyQt6 import ApplicationContext


from wild_horse.gui.ui.main_window import Ui_MainWindow
from wild_horse.gui.widget.frm_sobre import FrmSobre


class MainWindows(QMainWindow):
    def __init__(self, app_context: ApplicationContext, *args, **kwargs):
        super(MainWindows, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.widget_central.setStyleSheet(self.styleSheet())

        self.ui.widgetApenasIcones.setHidden(True)

        self.ui.btnConfiguracoesComTexto.clicked.connect(self._abrir_configuracoes)
        self.ui.btnConfiguracoesSemTexto.clicked.connect(self._abrir_configuracoes)
        self.ui.btnSobreComTexto.clicked.connect(self._abrir_tela_sobre)
        self.ui.btnSobreSemTexto.clicked.connect(self._abrir_tela_sobre)

        self._widget_central_padrao = self.ui.frameCentralNomeSistema
        self._widget_atual = None
        self._app_context = app_context
        self._add_opcoes_mercado_livre()

    def _add_opcoes_mercado_livre(self):
        menu = QMenu(self)
        menu.addAction(
            QIcon(":/icones/icones/compatibilidade.png"),
            "Inserir compatibilidades",
            self._abrir_tela_inserir_compatibilidade,
        )

        menu.addAction(
            QIcon(":/icones/icones/anuncio.png"),
            "Exportar anúncios para compatibilidades",
            self._abrir_tela_exportacao_anuncios,
        )

        menu.addAction(
            QIcon(":/icones/icones/atributos.png"),
            "Associar atributos de automóvel",
            self._abrir_tela_associacao_atributos,
        )

        self.ui.btnMeliComTexto.setMenu(menu)
        self.ui.btnMeliSemTexto.setMenu(menu)

    def _abrir_tela_exportacao_anuncios(self):
        from apps.integrador_meli.gui.widget.frm_exportar_anuncios_para_compatibilidade import \
            FrmExportarAnunciosParaCompatibilidade

        self._abrir_tela(FrmExportarAnunciosParaCompatibilidade)

    def _abrir_tela_associacao_atributos(self):
        from apps.integrador_meli.gui.widget.frm_gerar_associacao_atributos_automovel import \
            FrmGerarAssociacaoAtributosAutomovel
        self._abrir_tela(FrmGerarAssociacaoAtributosAutomovel)

    def _abrir_tela(self, cls_widget: Type[QWidget]):
        if isinstance(self._widget_atual, cls_widget):
            return

        self.fechar_widget_atual()

        frm = cls_widget(self)
        self.ui.widget_central.setStyleSheet(self.styleSheet())
        self.set_widget_central(frm)
        self._widget_atual = frm

    def _abrir_tela_inserir_compatibilidade(self):
        from apps.integrador_meli.gui.widget.frm_inserir_compatibilidades import FrmInserirCompatibilidadeMeli
        self._abrir_tela(FrmInserirCompatibilidadeMeli)

    def _abrir_tela_sobre(self):
        frm = FrmSobre(self)
        frm.setStyleSheet(self.styleSheet())
        frm.exec()

    def _abrir_configuracoes(self):
        from wild_horse.configuracoes.gui.widget.configuracoes import (
            FrmConfiguracoes,
        )

        self._abrir_tela(FrmConfiguracoes)

    def fechar_widget_atual(self):
        if self._widget_atual:
            self._widget_atual.close()
        self._widget_atual = None

    def set_widget_central(self, widget: QWidget):
        self._widget_central_padrao.setHidden(True)
        self.limpar_conteudo_widget_central()
        self.ui.widget_central.layout().addWidget(widget)

    def limpar_conteudo_widget_central(self):
        layout = self.ui.widget_central.layout()
        for i in range(layout.count()):
            item = layout.takeAt(i)
            layout.removeWidget(item.widget())


import resources_rc
