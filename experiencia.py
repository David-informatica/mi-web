from dataclasses import dataclass, field, asdict
from typing import List, Optional, Literal

############### si usamos enums es mejor pero se complica bastante ####################
# from enum import Enum

# class TipoExperiencia(Enum):
#     LABORAL = "laboral"
#     VOLUNTARIADO = "voluntariado"

@dataclass
class ExperienciaItem:
    # tipo: TipoExperiencia
    tipo: Literal["laboral", "voluntariado"]
    organizacion: str
    puesto: str
    descripcion: Optional[str] = None
    horas: Optional[int] = None

@dataclass
class Experiencia:
    experiencias: List[ExperienciaItem] = field(default_factory=list)

    def to_dict(self):
        return {"experiencia": [asdict(e) for e in self.experiencias]}