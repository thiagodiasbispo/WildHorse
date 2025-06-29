from datetime import date
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


def _convert_data(v):
    return v.strftime("%Y-%m-%d")


class TiposSituacoesPedidos(IntEnum):
    ATENDIDO = 9
    EM_ABERTO = 6
    CANCELADO = 12
    EM_ANDAMENTO = 15
    VENDA_AGENCIADA = 18
    EM_DIGITACAO = 21
    VERIFICADO = 24
    CHECKOUT_PARCIAL = 126724


class DefaultBaseModel(BaseModel):
    class Config:
        validate_by_name = True
        json_encoders = {
            date: _convert_data,
        }


class AtributoCarroGet(DefaultBaseModel):
    id: int
    name: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class MarcaGet(AtributoCarroGet):
    pass


class ModelGet(AtributoCarroGet):
    pass


class AnoGet(AtributoCarroGet):
    pass


class CompatibilidadeAtributoCarroPost(DefaultBaseModel):
    id: str
    value_id: str


class CompatibilidadeAtributoCarroVariosPost(DefaultBaseModel):
    id: str
    value_ids: Optional[list[str]]


class ResultadoPostCompatibilidadeAtributoCarroVariosPost(DefaultBaseModel):
    id: str
    value_ids: Optional[list[str]]


class CompatibilidadePorDominioFamiliaProdutoPost(DefaultBaseModel):
    domain_id: str
    attributes: list[CompatibilidadeAtributoCarroPost | CompatibilidadeAtributoCarroVariosPost]


class ResultadoCompatibilidadePorDominioFamiliaProdutoPost(DefaultBaseModel):
    created_compatibilities_count: int


class ProdutosAnunciadosModel(DefaultBaseModel):
    sku: str | None
    mlb: str
    title: str
    requer_compatibilidade: bool
    tem_sugestao_compabilidade: bool
    aceita_compatibilidade_universal: bool






















