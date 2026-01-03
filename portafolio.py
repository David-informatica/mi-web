from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Proyecto:
    nombre: str
    descripcion: str
    categoria: str
    tecnologias: List[str] = field(default_factory=list)
    web: Optional[str] = None
    grupo: Optional[List[str]] = None  # nombres de compañeros

@dataclass
class Merito:
    nombre: str
    descripcion: str

@dataclass
class Portafolio:
    proyectos: List[Proyecto] = field(default_factory=list)
    meritos: List[Merito] = field(default_factory=list)

    def to_dict(self):
        return {
            "proyectos": [asdict(p) for p in self.proyectos],
            "meritos": [asdict(m) for m in self.meritos]
        }