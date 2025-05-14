from pydantic import BaseModel

class ProdutosAnunciadosModel(BaseModel):
    sku: str | None
    codigo_mlp: str
    title: str
    requer_compatibilidade: bool
    tem_sugestao_compabilidade: bool