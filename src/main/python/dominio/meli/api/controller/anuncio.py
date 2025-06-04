from dominio.meli.api.controller.comum import SystemBaseControllerAutenticated
from dominio.meli.api.models import ProdutosAnunciadosModel


class AnuncioController(SystemBaseControllerAutenticated):
    def __init__(self, base_url, token):
        super().__init__(token)
        self._base_url = base_url #f"{base_url}/users/2280689507/items/search?search_type=scan"

    def _get_sku(self, item_info: dict):
        for atributo in item_info["attributes"]:
            if atributo["id"] == "SELLER_SKU":
                return atributo["value_name"]
        return None

    def get_produtos_anunciados_com_informacoes_de_compatabilidade(self):
        # produtos = []
        scroll_id = None
        first_request = True
        limit = 20

        while True:
            if first_request:
                endpoint = f"{self._base_url}/users/2280689507/items/search?search_type=scan"
                first_request = False
            else:
                endpoint = f"{self._base_url}/users/2280689507/items/search?search_type=scan&scroll_id={scroll_id}"

            produtos_data = self.get(endpoint)
            all_items_ids = produtos_data.get("results", [])
            scroll_id = produtos_data.get("scroll_id", None)

            if not all_items_ids:
                break

            item_ids_group = [all_items_ids[i:i + limit] for i in range(0, len(all_items_ids), limit)]

            for items_id in item_ids_group:
                items_id_str = map(str, items_id)
                items_id_str = ",".join(items_id_str)
                items_info = self.get(f"{self._base_url}/items?ids={items_id_str}")

                for item_info in items_info:
                    item_info = item_info["body"]
                    tags = item_info.get("tags", [])
                    produto = ProdutosAnunciadosModel(
                        sku=self._get_sku(item_info),
                        mlb=item_info.get("id"),
                        title=item_info.get("title"),
                        requer_compatibilidade="incomplete_compatibilities" in tags,
                        tem_sugestao_compabilidade="pending_compatibilities" in tags,
                    )
                    yield produto
                    # produtos.append(produto)

            if not scroll_id:
                break

        # return produtos
