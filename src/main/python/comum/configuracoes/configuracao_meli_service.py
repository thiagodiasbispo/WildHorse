from dataclasses import dataclass, asdict, fields
from enum import Enum

from fbs_runtime.application_context.PyQt6 import ApplicationContext

from comum.configuracoes.base import (
    atualizar_configuracao,
    configuracoes_contem_secao,
    ler_configuracoes_padrao,
    ler_configuracoes,
    ler_configuracao,
)

_MELI_CONFIG_FILE_PROD = "config/meli_default_prod.json"
_MELI_CONFIG_FILE_HOMOL = "config/meli_default_prod.json"

_MELI_SECAO = "MELI"
_MELI_API_SECAO = f"{_MELI_SECAO}/API"


class TipoAmbienteDesenvolvimento(Enum):
    HOMOLOGACAO = "HOMOLOGACAO"
    PRODUCAO = "PRODUCAO"


@dataclass(frozen=True)
class ConfiguracoesAPIMeli:
    client_id: str
    client_secret: str
    authorization_code:str
    url_base: str
    url_token: str
    url_autenticacao: str
    redirect_uri: str
    ultimo_token: str
    refresh_token: str
    validade_token: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return asdict(self)
        return data


def _get_meli_file_prod(app_context: ApplicationContext):
    return app_context.get_resource(_MELI_CONFIG_FILE_PROD)


def _get_meli_file_homol(app_context: ApplicationContext):
    return app_context.get_resource(_MELI_CONFIG_FILE_HOMOL)


def ler_configuracoes_api_meli() -> ConfiguracoesAPIMeli:
    colunas = tuple(f.name for f in fields(ConfiguracoesAPIMeli))
    valores = ler_configuracoes(_MELI_API_SECAO, colunas)
    return ConfiguracoesAPIMeli.from_dict(valores)


def atualizar_configuracoes_api_meli(config: ConfiguracoesAPIMeli) -> None:
    atualizar_configuracao(_MELI_API_SECAO, config.to_dict())


def carga_inicial_se_primeira_execucao(
    app_context: ApplicationContext, ambiente=TipoAmbienteDesenvolvimento.PRODUCAO
):

    if configuracoes_contem_secao(f"{_MELI_API_SECAO}/client_id"):
        return

    if ambiente == TipoAmbienteDesenvolvimento.PRODUCAO:
        dados = ler_configuracoes_padrao(_get_meli_file_prod(app_context))
    else:
        dados = ler_configuracoes_padrao(_get_meli_file_homol(app_context))

    atualizar_configuracao(_MELI_API_SECAO, dados["api"])


def configurar_para_ambiente_homologacao(app_context: ApplicationContext):
    dados = ler_configuracoes_padrao(_get_meli_file_prod(app_context))
    atualizar_configuracao(_MELI_API_SECAO, dados["api"])


def configurar_para_ambiente_producao(app_context: ApplicationContext):
    dados = ler_configuracoes_padrao(_get_meli_file_prod(app_context))
    atualizar_configuracao(_MELI_API_SECAO, dados["api"])


def get_ambiente_desenvolvimento():
    ambiente_configurado = ler_configuracao(
        f"{_MELI_API_SECAO}/ambiente_desenvolvimento"
    )
    return TipoAmbienteDesenvolvimento(ambiente_configurado)


def eh_ambiente_homologacao():
    return get_ambiente_desenvolvimento() == TipoAmbienteDesenvolvimento.HOMOLOGACAO
