import pandas as pd
from models.produtos_anunciados_model import ProdutosAnunciadosModel

def exportar_produtos_para_excel(produtos: list[ProdutosAnunciadosModel]):
    df = pd.DataFrame([produto.model_dump() for produto in produtos])
    df.to_excel("produtos.xlsx", index=False)