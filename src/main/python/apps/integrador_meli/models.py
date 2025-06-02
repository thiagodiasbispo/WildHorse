from dataclasses import dataclass, asdict


@dataclass(frozen=False)
class AssociacaoAtributosAutomovel:
    marca:str
    marca_id:str
    modelo:str
    modelo_id:str

    def to_dict(self):
        return asdict(self)