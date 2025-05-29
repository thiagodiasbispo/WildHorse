from datetime import datetime, timedelta

from comum.configuracoes.base import (
    get_string_as_datetime,
    get_datetime_as_string,
)
from comum.configuracoes.configuracao_meli_service import (
    ler_configuracoes_api_meli,
    ConfiguracoesAPIMeli,
    atualizar_configuracoes_api_meli,
)
from dominio.meli.api.controller_factory import MeliApiControllerFactory


def usuario_esta_autenticado():
    config = ler_configuracoes_api_meli()

    if not config.ultimo_token:
        return False

    validade_token = get_string_as_datetime(config.validade_token)

    if validade_token > datetime.now():
        return True

    try:
        refresh_token(config)
        return True
    except Exception:
        return False


def get_url_autenticacao():
    config = ler_configuracoes_api_meli()
    controller_factory = MeliApiControllerFactory(config)
    autenticacao_controller = controller_factory.autenticacao_controller

    return autenticacao_controller.get_url_autenticacao()


def refresh_token(config=None):
    print("Atualizando token")

    if not config:
        config = ler_configuracoes_api_meli()

    controller_factory = MeliApiControllerFactory(config)
    autenticacao_controller = controller_factory.autenticacao_controller
    token_data = autenticacao_controller.refresh_token(config.refresh_token)

    _update_config(config, token_data)
    print("Token atualizado e exportado com sucesso")


def orquestrar_obtencao_token(code):
    print("Obtendo novo token")

    config = ler_configuracoes_api_meli()
    controller_factory = MeliApiControllerFactory(config)
    autenticacao_controller = controller_factory.autenticacao_controller

    token_data = autenticacao_controller.get_token(code)

    _update_config(config, token_data)
    print("Token obtido e exportado com sucesso")


def _update_config(config, token_data: dict):
    config_dict = config.to_dict()

    config_dict["ultimo_token"] = token_data["access_token"]
    config_dict["refresh_token"] = token_data["refresh_token"]

    validade = token_data["expires_in"]
    validade = datetime.now() + timedelta(seconds=validade)
    config_dict["validade_token"] = get_datetime_as_string(validade)

    config = ConfiguracoesAPIMeli.from_dict(config_dict)

    atualizar_configuracoes_api_meli(config)
