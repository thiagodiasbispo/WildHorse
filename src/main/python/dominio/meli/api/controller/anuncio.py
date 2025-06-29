from dominio.meli.api.controller.catalogo_de_dominio import CatalogoDeDominioController
from dominio.meli.api.controller.comum import SystemBaseControllerAutenticated
from dominio.meli.api.models import ProdutosAnunciadosModel


class AnuncioController(SystemBaseControllerAutenticated):
    def __init__(self, base_url, token, user_id, catalogo_controller: CatalogoDeDominioController):
        super().__init__(token)
        self._base_url = base_url
        self._user_id = user_id
        self._catalogo_controller = catalogo_controller

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
        categorias_com_permissao_compatibilidade_universal = self._catalogo_controller.get_categorias_com__permissao_compatibilidade_universal()

        print("Categorias com permissão para compatibilidade universal:", categorias_com_permissao_compatibilidade_universal)

        while True:
            if first_request:
                endpoint = f"{self._base_url}/users/{self._user_id}/items/search?search_type=scan"
                first_request = False
            else:
                endpoint = f"{self._base_url}/users/{self._user_id}/items/search?search_type=scan&scroll_id={scroll_id}"

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
                    categoria = item_info["category_id"]
                    aceita_compatibilidade_universal = categoria in categorias_com_permissao_compatibilidade_universal
                    produto = ProdutosAnunciadosModel(
                        sku=self._get_sku(item_info),
                        mlb=item_info.get("id"),
                        title=item_info.get("title"),
                        requer_compatibilidade="incomplete_compatibilities" in tags,
                        tem_sugestao_compabilidade="pending_compatibilities" in tags,
                        aceita_compatibilidade_universal = aceita_compatibilidade_universal
                    )
                    yield produto
                    # produtos.append(produto)

            if not scroll_id:
                break

        # return produtos
