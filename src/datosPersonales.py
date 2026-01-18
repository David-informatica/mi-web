from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class DatosPersonales:
    nombre: str
    foto: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    web: Optional[str] = None

    def to_dict(self):
        return asdict(self)