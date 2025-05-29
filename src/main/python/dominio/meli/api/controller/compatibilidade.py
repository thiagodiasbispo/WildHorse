import json

from dominio.meli.api.controller.comum import (
    converter_resultado,
    SystemBaseControllerAutenticated, pydantic_custom_encoder,
)
from dominio.meli.api.models import CompatibilidadeAtributoCarroVariosPost, \
    ResultadoCompatibilidadePorDominioFamiliaProdutoPost


class CompatibilidadeController(SystemBaseControllerAutenticated):
    def __init__(self, base_url, token):
        super().__init__(token)
        self._base_url = f"{base_url}/tems/{0}/compatibilities"

    @converter_resultado(ResultadoCompatibilidadePorDominioFamiliaProdutoPost)
    def post_compatibilidade_por_dominio(self, mlb: str, compatibilidades: CompatibilidadeAtributoCarroVariosPost):
        return self.post(self._base_url.format(mlb), data=json.dumps(
            compatibilidades,
            default=pydantic_custom_encoder(by_alias=True, exclude_none=True),
        ))
