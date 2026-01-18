from __future__ import annotations
from pathlib import Path
from antlr4 import FileStream, CommonTokenStream

from CVLangLexer import CVLangLexer
from CVLangParser import CVLangParser
from cv_builder import BuildObjectsVisitor

def parse_with_antlr(input_path: Path) -> dict:
    stream = FileStream(str(input_path), encoding="utf-8")
    lexer = CVLangLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = CVLangParser(tokens)

    tree = parser.start()  # tu regla raíz
    visitor = BuildObjectsVisitor()
    objs = visitor.visit(tree)

    # Unifica salida a dict para Jinja
    # Si tu visitor devuelve dataclass CVObjects, conviértelo:
    return {
        "cv_id": getattr(objs, "cv_id", ""),
        "datos": getattr(objs, "datos", None),
        "formacion": getattr(objs, "formacion", None),
        "idiomas": getattr(objs, "idiomas", None),
        "experiencia": getattr(objs, "experiencia", None),
        "habilidades": getattr(objs, "habilidades", None),
        "portafolio": getattr(objs, "portafolio", None),
    }
