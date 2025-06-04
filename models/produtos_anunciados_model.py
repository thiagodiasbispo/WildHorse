from pydantic import BaseModel

class ProdutosAnunciadosModel(BaseModel):
    sku: str | None
    mlb: str
    title: str
    requer_compatibilidade: bool
    tem_sugestao_compabilidade: bool