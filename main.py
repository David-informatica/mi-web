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

    # IMPORTANTE: ahora la regla raíz se llama start
    tree = parser.start()

    visitor = BuildObjectsVisitor()
    objs = visitor.visit(tree)
    return objs


def render_html(objs, template_dir: str = "templates/", template_name: str = "plantilla_cv.html") -> str:
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    html = template.render(
        datos=objs.datos.to_dict(),
        formacion=objs.formacion.to_dict(),
        idiomas=objs.idiomas.to_dict() if objs.idiomas else {"idiomas": []},
        experiencia=objs.experiencia.to_dict() if objs.experiencia else {"experiencias": []},
        habilidades=objs.habilidades.to_dict() if objs.habilidades else {"habilidades": []},
        portafolio=objs.portafolio.to_dict() if objs.portafolio else {"proyectos": [], "meritos": []},
    )
    return html


if __name__ == "__main__":
    objs = parse_cv("entrada.txt")

    html = render_html(objs, template_dir=".", template_name="plantilla_cv.html")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("OK -> index.html generado")
