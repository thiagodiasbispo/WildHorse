import json
from collections.abc import Iterable

from dominio.meli.api.controller.comum import (
    converter_resultado,
    SystemBaseControllerAutenticated, pydantic_custom_encoder,
)
from dominio.meli.api.models import CompatibilidadeAtributoCarroVariosPost, \
    ResultadoCompatibilidadePorDominioFamiliaProdutoPost, CompatibilidadePorDominioFamiliaProdutoPost


class CompatibilidadeController(SystemBaseControllerAutenticated):
    DOMAIN_MLB_CARS_AND_VAN = "MLB-CARS_AND_VAN"
    MARCA = "BRAND"
    MODELO = "MODEL"
    ANO = "VEHICLE_YEAR"

    def __init__(self, base_url, token):
        super().__init__(token)
        self._base_url = f"{base_url}/items/" + "{mlb}/compatibilities"

    @converter_resultado(ResultadoCompatibilidadePorDominioFamiliaProdutoPost)
    def post_compatibilidade_por_dominio(self, mlb: str,
                                         compatibilidades: list[
                                             CompatibilidadeAtributoCarroVariosPost | CompatibilidadeAtributoCarroVariosPost]) -> ResultadoCompatibilidadePorDominioFamiliaProdutoPost:
        comp = CompatibilidadePorDominioFamiliaProdutoPost(domain_id=self.DOMAIN_MLB_CARS_AND_VAN,
                                                           attributes=compatibilidades)
        encoder = pydantic_custom_encoder(by_alias=True, exclude_none=True)

        data = {
            "products_families": [encoder(comp)]
        }
        print(data)
        return self.post(self._base_url.format(mlb=mlb), data=json.dumps(data))
