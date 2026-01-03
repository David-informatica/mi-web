from dataclasses import dataclass, field, asdict
from typing import List, Optional, Literal

############### si usamos enums es mejor pero se complica bastante ####################
# from enum import Enum

# class TipoHabilidad(Enum):
#     SOFT = "soft"
#     HARD = "hard"

@dataclass
class Habilidad:
    nombre: str
    # tipo: TipoHabilidad
    tipo: Literal["soft", "hard"]
    categoria: Optional[str] = None
    nivel: Optional[str] = None

@dataclass
class Habilidades:
    habilidades: List[Habilidad] = field(default_factory=list)

    def to_dict(self):
        return {"habilidades": [asdict(h) for h in self.habilidades]}