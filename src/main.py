from __future__ import annotations
from pathlib import Path

from config import load_config
from render import render_html
from parsers.antlr_engine import parse_with_antlr
from parsers.flexcup_engine import parse_with_flexcup

def main() -> None:
    project_root = Path(__file__).resolve().parents[1]  # src/.. = raiz
    cfg = load_config(project_root)

    if cfg.engine == "ANTLR":
        context = parse_with_antlr(cfg.input_path)
    else:
        context = parse_with_flexcup(cfg.input_path, project_root)

    output_path = project_root / "index.html"
    render_html(cfg.template_path, context, output_path)

if __name__ == "__main__":
    main()
