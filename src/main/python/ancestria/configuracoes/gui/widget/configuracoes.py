import traceback

from PyQt6 import QtWidgets
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from fbs_runtime.application_context.PyQt6 import ApplicationContext

from comum.configuracoes.configuracao_meli_service import (
    ler_configuracoes_api_meli,
    ConfiguracoesAPIMeli,
    atualizar_configuracoes_api_meli,
)
from comum.widget_utils import mostrar_mensagem_sucesso, mostrar_mensagem_erro
from dominio.meli.api.controller_factory import MeliApiControllerFactory

from dominio.meli.api.autenticacao_utils import orquestrar_obtencao_token
from ancestria.configuracoes.gui.ui.configuracoes import Ui_FrmConfiguracoes


class FrmConfiguracoes(QtWidgets.QWidget):
    def __init__(self, app_context: ApplicationContext, *args, **kwargs):
        super(FrmConfiguracoes, self).__init__(*args, **kwargs)
        self.ui = Ui_FrmConfiguracoes()
        self.ui.setupUi(self)
        self._app_context = app_context
        self.ui.btnSalvar.clicked.connect(self._salvar_configuracoes)
        self.ui.edtAuthorizationCode.textChanged.connect(
            lambda text: self.ui.btnAtualizarToken.setEnabled(len(text.strip()) > 0))
        self.ui.btnAbrirJanelaAutenticacao.clicked.connect(self._abrir_janela_autenticacao)
        self.ui.btnAtualizarToken.clicked.connect(self._atualizar_token)

        self._carregar_configuracoes()

    @property
    def authorization_code(self):
        return self.ui.edtAuthorizationCode.text()

    def _abrir_janela_autenticacao(self):

        try:
            config = self._get_configuracoes_atualizadas()
            autenticacao_controller = MeliApiControllerFactory(config).autenticacao_controller
            url = autenticacao_controller.get_url_autenticacao()
            QDesktopServices.openUrl(QUrl(url))
        except Exception as e:
            mostrar_mensagem_erro(
                self, f"Erro ao iniciar a rotina de autenticação:\n{e}"
            )
            traceback.print_exc()


    def _carregar_configuracoes(self):

        try:
            ui = self.ui
            config = self._configuracoes_originais = ler_configuracoes_api_meli()

            ui.edtClientId.setText(config.client_id)
            ui.edtClientSecret.setText(config.client_secret)
            ui.edtToken.setText(config.ultimo_token)
            ui.edtRefreshToken.setText(config.refresh_token)
            ui.edtValidadeToken.setText(config.validade_token)
            ui.edtRedirectUri.setText(config.redirect_uri)

        except Exception as e:
            mostrar_mensagem_erro(
                self, f"Não foi possível carregar as configurações:\n{e}"
            )
    def _atualizar_token(self):
        try:
            orquestrar_obtencao_token(self.authorization_code)
            mostrar_mensagem_sucesso(self, "Token atualizado com sucesso!")
            mostrar_mensagem_sucesso(self, "Configurações atualizadas com sucesso!")
            self._carregar_configuracoes()
        except Exception as e:
            mostrar_mensagem_erro(
                self, f"Não ao atualizar token:\n{e}"
            )
            traceback.print_exc()

    def _get_configuracoes_atualizadas(self):
        ui = self.ui
        return ConfiguracoesAPIMeli(
            client_id=ui.edtClientId.text(),
            client_secret=ui.edtClientSecret.text(),
            url_base=self._configuracoes_originais.url_base,
            url_token=self._configuracoes_originais.url_token,
            url_autenticacao=self._configuracoes_originais.url_autenticacao,
            redirect_uri=self._configuracoes_originais.redirect_uri,
            ultimo_token=self.ui.edtToken.text(),
            refresh_token=self.ui.edtRefreshToken.text(),
            validade_token=self.ui.edtValidadeToken.text(),
            authorization_code=self.authorization_code
        )

    def _salvar_configuracoes(self):
        try:
            config = self._get_configuracoes_atualizadas()
            atualizar_configuracoes_api_meli(config)
            mostrar_mensagem_sucesso(self, "Configurações atualizadas com sucesso!")
        except Exception as e:
            mostrar_mensagem_erro(
                self, f"Não foi possível salvar as atualizações:\n{e}"
            )
