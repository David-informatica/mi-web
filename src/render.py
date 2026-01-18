from __future__ import annotations
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_html(template_path: Path, context: dict, output_path: Path) -> None:
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template(template_path.name)
    html = template.render(**context)
    output_path.write_text(html, encoding="utf-8")
