import argparse
from pathlib import Path
import sys

from antlr4 import FileStream, CommonTokenStream
from jinja2 import Environment, FileSystemLoader

from CVLangLexer import CVLangLexer
from CVLangParser import CVLangParser

from cv_builder import BuildObjectsVisitor


def parse_cv(input_path: str):
    stream = FileStream(input_path, encoding="utf-8")
    lexer = CVLangLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = CVLangParser(tokens)

    # Regla raíz: start
    tree = parser.start()

    visitor = BuildObjectsVisitor()
    objs = visitor.visit(tree)
    return objs


def render_html(objs, template_path: str) -> str:
    template_path = Path(template_path)
    env = Environment(loader=FileSystemLoader(str(template_path.parent)))
    template = env.get_template(template_path.name)

    html = template.render(
        datos=objs.datos.to_dict(),
        formacion=objs.formacion.to_dict(),
        idiomas=objs.idiomas.to_dict() if objs.idiomas else {"idiomas": []},
        # FIX: la clave debe ser "experiencia" (no "experiencias")
        experiencia=objs.experiencia.to_dict() if objs.experiencia else {"experiencia": []},
        habilidades=objs.habilidades.to_dict() if objs.habilidades else {"habilidades": []},
        portafolio=objs.portafolio.to_dict() if objs.portafolio else {"proyectos": [], "meritos": []},
    )
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Ruta al .txt (ej: entradas/entrada.txt)")
    ap.add_argument("--template", required=True, help="Ruta al .html (ej: templates/plantilla_cv.html)")
    ap.add_argument("--out", required=True, help="Ruta de salida (ej: index.html)")
    args = ap.parse_args()

    input_path = Path(args.input)
    template_path = Path(args.template)
    out_path = Path(args.out)

    if not input_path.exists():
        print(f"[ERROR] No existe input: {input_path}", file=sys.stderr)
        sys.exit(2)

    if not template_path.exists():
        print(f"[ERROR] No existe template: {template_path}", file=sys.stderr)
        sys.exit(2)

    objs = parse_cv(str(input_path))
    html = render_html(objs, str(template_path))

    out_path.write_text(html, encoding="utf-8")

    if not out_path.exists() or out_path.stat().st_size == 0:
        print("[ERROR] index.html no se generó o está vacío", file=sys.stderr)
        sys.exit(3)

    print(f"OK -> {out_path} generado")


if __name__ == "__main__":
    main()
