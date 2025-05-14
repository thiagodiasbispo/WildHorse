import os

from models.compatibilidade_produto_model import CompatibilidadeProdutoModel
from models.produtos_anunciados_model import ProdutosAnunciadosModel
from services.mercadolivre_service import MercadoLivreService
from utils.export_utils import exportar_produtos_para_excel


class ProdutosAnunciadosController:
    def __init__(self):
        self.service = MercadoLivreService()

    def _get_sku(self, item_info: dict):
        for atributo in item_info["attributes"]:
            if atributo["id"] == "SELLER_SKU":
                return atributo["value_name"]
        return None

    def get_produtos(self):
        user_id = os.getenv('USER_ID')
        produtos = []
        scroll_id = None
        first_request = True
        limit = 20

        while True:
            if first_request:
                endpoint = f"/users/{user_id}/items/search?search_type=scan"
                first_request = False
            else:
                endpoint = f"/users/{user_id}/items/search?search_type=scan&scroll_id={scroll_id}"

            produtos_data = self.service.get(endpoint)
            all_items_ids = produtos_data.get("results", [])
            scroll_id = produtos_data.get("scroll_id", None)

            if not all_items_ids:
                break

            item_ids_group = [all_items_ids[i:i + limit] for i in range(0, len(all_items_ids), limit)]

            for items_id in item_ids_group:
                items_id_str = map(str, items_id)
                items_id_str = ",".join(items_id_str)
                items_info = self.service.get(f"/items?ids={items_id_str}")

                for item_info in items_info:
                    item_info = item_info["body"]
                    tags = item_info.get("tags", [])
                    produto = ProdutosAnunciadosModel(
                        sku=self._get_sku(item_info),
                        codigo_mlp=item_info.get("id"),
                        title=item_info.get("title"),
                        requer_compatibilidade="incomplete_compatibilities" in tags,
                        tem_sugestao_compabilidade="pending_compatibilities" in tags,
                    )
                    produtos.append(produto)

            if not scroll_id:
                break

        return produtos

    def exportar_para_excel(self, produtos):
        exportar_produtos_para_excel(produtos)

    def post_compatibilidades(self, compatibilidades: list[CompatibilidadeProdutoModel]):
        for compat in compatibilidades:
            self.service.post(
                f"/items/{compat.item_id}/compatible_products",
                json=compat.model_dump()
            )
