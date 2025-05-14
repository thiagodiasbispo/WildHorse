from services.mercadolivre_service import MercadoLivreService


class AtributosVeiculosController:
    def __init__(self):
        self.service = MercadoLivreService()

    def get_marcas(self, site_id="MLB"):
        endpoint = f"/catalog_domains/MLB-CARS_AND_VANS/attributes/BRAND"
        response = self.service.get(endpoint)
        return  response.get("suggested_values", [])
        # atributo_marca = None
        #
        # for atributo in attributes:
        #     if atributo["id"] == "BRAND":
        #         atributo_marca = atributo
        #         break
        #
        # return atributo_marca["suggested_values"]
        #

    def get_modelos(self, marca_id):
        endpoint = f"/categories/MLB1747/attributes/MODEL/values?brand_id={marca_id}"
        response = self.service.get(endpoint)
        return response.get("values", [])

    def get_anos(self, modelo_id, site_id="MLB"):
        endpoint = f"/categories/MLB/attributes/VEHICLE_YEAR/values?model_id={modelo_id}"
        response = self.service.get(endpoint)
        return response.get("values", [])
