from __future__ import annotations
from pathlib import Path
import json
import subprocess

def parse_with_flexcup(input_path: Path, project_root: Path) -> dict:
    """
    Espera que exista un runner Java que:
      - lea el input
      - parsee con CUP
      - imprima un JSON por stdout
    """

    # Ruta donde generas/compilas el Java (puedes elegir build/java o similar)
    build_dir = project_root / "build" / "flexcup"
    build_dir.mkdir(parents=True, exist_ok=True)

    # IMPORTANTE:
    # Aquí tienes dos opciones:
    # A) si ya subes los .java generados/compilados al repo, solo ejecutas.
    # B) si quieres generar/compilar en CI, haces aquí (o en workflow) los pasos con jflex + cup + javac.

    # Este comando es un placeholder. Ajusta Main class y classpath a lo que tú tengas.
    cmd = [
        "java",
        "-cp",
        str(build_dir),  # y/o jars necesarios
        "Main",
        str(input_path)
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            "Flex/CUP fallo.\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}\n"
        )

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            "Flex/CUP no devolvió JSON válido.\n"
            f"STDOUT:\n{proc.stdout}\n"
            f"STDERR:\n{proc.stderr}\n"
        ) from e
