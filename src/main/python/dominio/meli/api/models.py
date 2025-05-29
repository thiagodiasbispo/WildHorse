from datetime import date
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


def _convert_data(v):
    return v.strftime("%Y-%m-%d")


class TiposSituacoesPedidos(IntEnum):
    ATENDIDO = 9
    EM_ABERTO = 6
    CANCELADO = 12
    EM_ANDAMENTO = 15
    VENDA_AGENCIADA = 18
    EM_DIGITACAO = 21
    VERIFICADO = 24
    CHECKOUT_PARCIAL = 126724


class DefaultBaseModel(BaseModel):
    class Config:
        validate_by_name = True
        json_encoders = {
            date: _convert_data,
        }


class AtributoCarroGet(DefaultBaseModel):
    id: int
    name: str


class MarcaGet(AtributoCarroGet):
    pass


class ModelGet(AtributoCarroGet):
    pass


class AnoGet(AtributoCarroGet):
    pass


class CompatibilidadeAtributoCarroPost(DefaultBaseModel):
    id: str
    value_id: str


class CompatibilidadeAtributoCarroVariosPost(DefaultBaseModel):
    id: str
    value_ids: Optional[list[str]]


class ResultadoPostCompatibilidadeAtributoCarroVariosPost(DefaultBaseModel):
    id: str
    value_ids: Optional[list[str]]


class CompatibilidadePorDominioFamiliaProdutoPost(DefaultBaseModel):
    domain_id: str
    atrributes: list[CompatibilidadeAtributoCarroPost | CompatibilidadeAtributoCarroVariosPost]


class ResultadoCompatibilidadePorDominioFamiliaProdutoPost(DefaultBaseModel):
    created_compatibilities_count: int


class Contato(DefaultBaseModel):
    id: int
    nome: str
    tipo_pessoa: str = Field(alias="tipoPessoa", default=None)
    numero_documento: str = Field(alias="numeroDocumento", default=None)


class SituacaoModulo(DefaultBaseModel):
    id: int
    nome: str
    id_herdado: int = Field(alias="idHerdado")
    cor: str


class SituacaoPedido(DefaultBaseModel):
    id: int
    valor: int


class LojaPedido(DefaultBaseModel):
    id: int


class PedidoVenda(DefaultBaseModel):
    id: int
    numero: int
    numero_loja: str = Field(alias="numeroLoja")
    data: date
    data_saida: date = Field(alias="dataSaida")
    data_prevista: str = Field(alias="dataPrevista")
    total_produtos: float = Field(alias="totalProdutos")
    total: float
    contato: Contato
    situacao: SituacaoPedido
    loja: LojaPedido

    # @field_validator('data_prevista', mode="before")
    # def validate_age(cls, v):
    #     try:
    #         return _convert_data(v)
    #     except Exception as e:
    #         print("Erro na conversão de data prevista: ", str(e))
    #         return None


class DescontoPedidoVendaDetalhes(DefaultBaseModel):
    valor: float
    unidade: str


class CategoriaPedidoVendaDetalhes(DefaultBaseModel):
    id: int


class NotaFiscalPedidoVendaDetalhes(DefaultBaseModel):
    id: int


class TributacaoPedidoVendaDetalhes(DefaultBaseModel):
    total_icms: float = Field(alias="totalICMS")
    total_ipi: float = Field(alias="totalIPI")


class ProdutoItemPedidoVendaDetalhes(DefaultBaseModel):
    id: int


class ComissaoItemPedidoVendaDetalhes(DefaultBaseModel):
    base: float
    aliquota: float
    valor: float


class ItemPedidoVendaDetalhes(DefaultBaseModel):
    id: int
    codigo: str
    unidade: str
    quantidade: int
    desconto: float
    valor: float
    aliquota_ipi: float = Field(alias="aliquotaIPI")
    descricao: str
    descricao_detalhada: str = Field(alias="descricaoDetalhada")
    produto: ProdutoItemPedidoVendaDetalhes
    comissao: ComissaoItemPedidoVendaDetalhes


class VendasParcelaFormaPagamentoDetalhes(DefaultBaseModel):
    id: int


class ParcelasPedidoVendaDetalhes(DefaultBaseModel):
    id: int
    data_vencimento: date = Field(alias="dataVencimento")
    valor: float
    observacoes: str
    forma_pagamento: VendasParcelaFormaPagamentoDetalhes = Field(alias="formaPagamento")


class EtiquetaTransporte(DefaultBaseModel):
    nome: str
    endereco: str
    numero: str
    complemento: str
    municipio: str
    uf: str
    cep: str
    bairro: str
    nome_pais: str = Field(alias="nomePais")


class VolumeTransporte(DefaultBaseModel):
    id: int
    servico: str
    codigo_rastreamento: str = Field(alias="codigoRastreamento")


class VendasTransporteContato(DefaultBaseModel):
    id: int
    nome: str


class TransportePedidoVenda(DefaultBaseModel):
    frete_por_conta: int = Field(alias="fretePorConta")
    frete: float
    quantidade_volumes: int = Field(alias="quantidadeVolumes")
    peso_bruto: float = Field(alias="pesoBruto")
    prazo_entrega: int = Field(alias="prazoEntrega")
    contato: VendasTransporteContato
    etiqueta: EtiquetaTransporte
    volumes: list[VolumeTransporte]


class Vendedor(DefaultBaseModel):
    id: int


class Intermediador(DefaultBaseModel):
    cnpj: str
    nome_usuario: str = Field(alias="nomeUsuario")


class Taxas(DefaultBaseModel):
    taxa_comissao: float = Field(alias="taxaComissao")
    custo_frete: float = Field(alias="custoFrete")
    valor_base: float = Field(alias="valorBase")


class PedidoVendaDetalhes(PedidoVenda):
    numero_pedido_compra: str = Field(alias="numeroPedidoCompra")
    outras_despesas: float = Field(alias="outrasDespesas")
    observacoes: str
    observacoes_internas: str = Field(alias="observacoesInternas")
    desconto: DescontoPedidoVendaDetalhes
    categoria: CategoriaPedidoVendaDetalhes
    nota_fiscal: Optional[NotaFiscalPedidoVendaDetalhes] = Field(alias="notaFiscal")
    tributacao: TributacaoPedidoVendaDetalhes
    itens: list[ItemPedidoVendaDetalhes]
    parcelas: list[ParcelasPedidoVendaDetalhes]
    transporte: TransportePedidoVenda
    vendedor: Vendedor
    intermediador: Intermediador
    taxas: Taxas


class ItemPedidoVendaDetalhesPut(DefaultBaseModel):
    codigo: str
    unidade: str
    quantidade: int
    desconto: float
    valor: float
    aliquota_ipi: float = Field(alias="aliquotaIPI")
    descricao: str
    descricao_detalhada: str = Field(alias="descricaoDetalhada")
    produto: ProdutoItemPedidoVendaDetalhes
    comissao: ComissaoItemPedidoVendaDetalhes


class ContatoPut(DefaultBaseModel):
    id: int
    tipo_pessoa: str = Field(alias="tipoPessoa", default=None)
    numero_documento: str = Field(alias="numeroDocumento", default=None)


class PedidoVendaDetalhesPut(DefaultBaseModel):
    numero: Optional[int] = None
    numero_loja: Optional[str] = Field(alias="numeroLoja", default=None)
    data: date
    data_saida: date = Field(alias="dataSaida", default=None)
    data_prevista: str = Field(alias="dataPrevista", default=None)
    loja: LojaPedido
    contato: ContatoPut
    numero_pedido_compra: str = Field(alias="numeroPedidoCompra")
    outras_despesas: float = Field(alias="outrasDespesas")
    observacoes: str = None
    observacoes_internas: str = Field(alias="observacoesInternas")
    desconto: DescontoPedidoVendaDetalhes
    categoria: CategoriaPedidoVendaDetalhes
    tributacao: TributacaoPedidoVendaDetalhes
    itens: list[ItemPedidoVendaDetalhesPut]
    parcelas: list[ParcelasPedidoVendaDetalhes]
    transporte: TransportePedidoVenda
    vendedor: Vendedor
    intermediador: Intermediador
    taxas: Taxas


class Modulo(DefaultBaseModel):
    id: int
    nome: str
    descricao: str
    criar_situacoes: bool = Field(alias="criarSituacoes")


class CanalVenda(DefaultBaseModel):
    id: int
    descricao: str
    tipo: str
    situacao: int


from pydantic import BaseModel, Field
from typing import List


class AlertaRespostaPutPedido(BaseModel):
    index: int
    code: int
    msg: str
    element: str
    namespace: str


class AlertasRespostaPutPedido(BaseModel):
    code: int
    msg: str
    element: str
    namespace: str
    collection: List[AlertaRespostaPutPedido]


class RespostaPutPedido(BaseModel):
    id: int
    warnings: List[AlertasRespostaPutPedido] = Field(default=[], alias="alertas")
    tracking: dict = Field(default=[], alias="rastreamento")

    def sucesso(self):
        return bool(self.warnings)

    def mensagens(self):
        if self.sucesso():
            return ""
        mensagens = [a.msg for a in self.warnings]
        return ".".join(mensagens)
