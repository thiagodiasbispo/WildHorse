from services.mercadolivre_service import MercadoLivreService


class CompatibilidadeController:
    def __init__(self):
        self.service = MercadoLivreService()

    def remover_compatibilidades(self, mlb):
        endpoint = f"/items/{mlb}/compatibilities"
        response = self.service.delete(endpoint)
        try:
            return response["deleted_compatibilities"]
        except KeyError:
            return []
