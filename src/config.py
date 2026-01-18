from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class RunConfig:
    engine: str          # "ANTLR" o "CUP"
    input_path: Path     # ./entradas/...
    template_path: Path  # ./templates/...

def load_config(project_root: Path) -> RunConfig:
    cfg_path = project_root / "argumentos.txt"
    if not cfg_path.is_file():
        raise FileNotFoundError(f"No existe argumentos.txt en {cfg_path}")

    lines = [ln.strip() for ln in cfg_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) < 3:
        raise ValueError("argumentos.txt debe tener 3 lineas: ENGINE, INPUT_TXT, TEMPLATE_HTML")

    engine = lines[0].upper()
    input_name = lines[1]
    template_name = lines[2]

    if engine not in {"ANTLR", "CUP"}:
        raise ValueError("ENGINE debe ser ANTLR o CUP (Flex/CUP)")

    input_path = project_root / "entradas" / input_name
    template_path = project_root / "templates" / template_name

    if not input_path.is_file():
        raise FileNotFoundError(f"No existe la entrada: {input_path}")
    if not template_path.is_file():
        raise FileNotFoundError(f"No existe la plantilla: {template_path}")

    return RunConfig(engine=engine, input_path=input_path, template_path=template_path)
