import json

from dominio.meli.api.controller.comum import (
    converter_resultado,
    SystemBaseControllerAutenticated, )
from dominio.meli.api.models import MarcaGet, ModelGet, AnoGet


class CatalogoDeDominioController(SystemBaseControllerAutenticated):
    DOMINIO_MLB_CARS_AND_VANS = "MLB-CARS_AND_VANS"

    def __init__(self, base_url, token):
        super().__init__(token)
        self._base_url_atributos = f"{base_url}/catalog_domains/{self.DOMINIO_MLB_CARS_AND_VANS}/attributes"
        self._base_url_compatibilidade = f"{base_url}/catalog/dumps/domains/MLB/compatibilities"

    def get_categorias_com__permissao_compatibilidade_universal(self) -> set[str]:
        """
            Retorna as categorias que possuem permissão para compatibilidade universal.
        """
        data = self.get(self._base_url_compatibilidade)
        categorias_permissao = set()
        for data_nive1 in data:
            for compatibilidade in data_nive1["compatibilities"]:
                for categoria in  compatibilidade["categories"]:
                    if categoria["universal_status"] == "ENABLED":
                        categorias_permissao.add(categoria["id"])

        return categorias_permissao

    @converter_resultado(MarcaGet)
    def get_marcas(self):
        url = f"{self._base_url_atributos}/BRAND/top_values"
        return self.post(url, data={})

    @converter_resultado(ModelGet)
    def get_modelos_marca(self, id_marca: str):
        url = f"{self._base_url_atributos}/MODEL/top_values"
        data = {"known_attributes": [{"id": "BRAND", "value_id": str(id_marca)}]}
        return self.post(url, data=json.dumps(data))

    @converter_resultado(AnoGet)
    def get_anos_marca_modelo(self, id_marca: str, id_modelo: str):
        url = f"{self._base_url_atributos}/VEHICLE_YEAR/top_values"
        data = {"known_attributes": [{"id": "BRAND", "value_id": str(id_marca)}, {"id": "MODEL", "value_id": str(id_modelo)}]}
        return self.post(url, data=json.dumps(data))
