from pydantic import BaseModel

class CompatibilidadeProdutoModel(BaseModel):
    item_id: str
    compatibility: list[dict]  # Exemplo: [{"make": {"id": "marca_id"}, "model": {"id": "modelo_id"}}]