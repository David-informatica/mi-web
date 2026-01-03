from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class Idioma:
    nombre: str
    nivel: str
    expedidor: Optional[str] = None

@dataclass
class Idiomas:
    idiomas: List[Idioma] = field(default_factory=list)

    def to_dict(self):
        return {"idiomas": [asdict(i) for i in self.idiomas]}