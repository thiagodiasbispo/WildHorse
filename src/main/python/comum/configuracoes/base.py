import json
from typing import Iterable
from datetime import datetime
from PyQt6.QtCore import QSettings

_NOME_EMPRESA = "ANCESTRIA"
_NOME_SOFTWARE = "ANCESTRIA"

_CONFIGURACAO_PADRAO = QSettings(_NOME_EMPRESA, _NOME_SOFTWARE)


def _ler_arquivo_configuracao_padrao() -> QSettings:
    return QSettings(_NOME_EMPRESA, _NOME_SOFTWARE)


def ler_configuracao(chave: str, config: QSettings = None, default=""):
    config = config or _ler_arquivo_configuracao_padrao()
    return config.value(chave, default)


def ler_configuracoes(secao, chaves: Iterable[str]):
    config = _ler_arquivo_configuracao_padrao()
    return {c: ler_configuracao(f"{secao}/{c}", config) for c in chaves}


def atualizar_configuracao(secao, valores: dict):
    config = _ler_arquivo_configuracao_padrao()
    config.beginGroup(secao)

    for chave, valor in valores.items():
        config.setValue(chave, valor)

    config.endGroup()
    config.sync()


def ler_configuracoes_padrao(arquivo):
    with open(arquivo) as arquivo_config:
        return json.load(arquivo_config)


def configuracoes_contem_secao(secao: str):
    config = _ler_arquivo_configuracao_padrao()
    return config.contains(secao)


def limpar_configuracoes():
    _ler_arquivo_configuracao_padrao().clear()


def get_datetime_as_string(datetime_: datetime):
    return datetime_.strftime("%d/%m/%Y %H:%M:%S")


def get_string_as_datetime(datetime_str: str):
    return datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
