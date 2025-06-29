from comum.configuracoes.configuracao_meli_service import (
    ConfiguracoesAPIMeli
)
from dominio.meli.api.controller.anuncio import AnuncioController
from dominio.meli.api.controller.autenticacao import AutenticacaoController
from dominio.meli.api.controller.catalogo_de_dominio import CatalogoDeDominioController
from dominio.meli.api.controller.compatibilidade import CompatibilidadeController


class MeliApiControllerFactory:

    def __init__(self, config: ConfiguracoesAPIMeli):
        self._compatibilidade = None
        self._catalogo_dominio = None
        self._autenticacao = None
        self._anuncio = None
        self._config = config

    @property
    def anuncio_controller(self) -> AnuncioController:
        if self._anuncio is None:
            self._anuncio = AnuncioController(
                base_url=self._config.url_base,
                token=self._config.ultimo_token,
                user_id=self._config.user_id,
                catalogo_controller = self.catalogo_dominio_controller,
            )
        return self._anuncio

    @property
    def catalogo_dominio_controller(self) -> CatalogoDeDominioController:
        if self._catalogo_dominio is None:
            self._catalogo_dominio = CatalogoDeDominioController(
                base_url=self._config.url_base,
                token=self._config.ultimo_token,
            )
        return self._catalogo_dominio

    @property
    def compatibilidade_controller(self) -> CompatibilidadeController:
        if self._compatibilidade is None:
            self._compatibilidade = CompatibilidadeController(
                base_url=self._config.url_base,
                token=self._config.ultimo_token,
            )
        return self._compatibilidade

    @property
    def autenticacao_controller(self) -> AutenticacaoController:
        if self._autenticacao is None:
            self._autenticacao = AutenticacaoController(
                url_base = self._config.url_base,
                url_autenticacao=self._config.url_autenticacao,
                url_token=self._config.url_token,
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
                redirect_uri=self._config.redirect_uri
            )
        return self._autenticacao


def get_factory() -> MeliApiControllerFactory:
    from comum.configuracoes.configuracao_meli_service import (
        ler_configuracoes_api_meli
    )
    config = ler_configuracoes_api_meli()
    return MeliApiControllerFactory(config)
