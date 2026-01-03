from dataclasses import dataclass, field, asdict
from typing import List, Optional, Literal

############### si usamos enums es mejor pero se complica bastante ####################
# from enum import Enum

# class TipoFormacion(Enum):
#     OFICIAL = "oficial"
#     COMPLEMENTARIA = "complementaria"

@dataclass
class FormacionItem:
    titulo: str
    institucion: str
    tipo: Literal["oficial", "complementaria"]
    descripcion: Optional[str] = None
    logros: Optional[str] = None
    fecha: Optional[str] = None
    en_curso: bool = False
    # tipo: TipoFormacion

@dataclass
class Formacion:
    items: List[FormacionItem] = field(default_factory=list)

    def to_dict(self):
        return {"formacion": [asdict(i) for i in self.items]}