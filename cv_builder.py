from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict, Any

from datosPersonales import DatosPersonales
from formacion import Formacion, FormacionItem
from idiomas import Idiomas, Idioma
from experiencia import Experiencia, ExperienciaItem
from habilidades import Habilidades, Habilidad
from portafolio import Portafolio, Proyecto, Merito

from CVLangVisitor import CVLangVisitor
from CVLangParser import CVLangParser


# ---------- helpers de texto ----------
def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def _inside_parens(s: str) -> str:
    """
    Convierte:
      'nomyape(Antonio Lobato)' -> 'Antonio Lobato'
      '(Antonio Lobato)'       -> 'Antonio Lobato'
    Si no hay paréntesis, devuelve el string original.
    """
    s = s.strip()
    if "(" in s and s.endswith(")"):
        return s[s.find("(") + 1 : -1].strip()
    if s.startswith("(") and s.endswith(")"):
        return s[1:-1].strip()
    return s


def _ctx_text(ctx) -> str:
    return ctx.getText().strip()


def _ctx_value(ctx) -> str:
    # Saca el texto del nodo y devuelve lo de dentro de (...)
    return _unquote(_inside_parens(_ctx_text(ctx)))


def _split_tecnologias(s: str) -> List[str]:
    raw = s.strip()
    if not raw:
        return []
    if "," in raw:
        return [t.strip() for t in raw.split(",") if t.strip()]
    return [t.strip() for t in raw.split() if t.strip()]


@dataclass
class CVObjects:
    cv_id: str
    datos: DatosPersonales
    formacion: Formacion
    idiomas: Optional[Idiomas]
    experiencia: Optional[Experiencia]
    habilidades: Optional[Habilidades]
    portafolio: Optional[Portafolio]


class BuildObjectsVisitor(CVLangVisitor):
    def __init__(self) -> None:
        super().__init__()
        self._cv_id: str = "CV"
        self._datos: Optional[DatosPersonales] = None
        self._form: Optional[Formacion] = None
        self._idiomas: Optional[Idiomas] = None
        self._xp: Optional[Experiencia] = None
        self._skills: Optional[Habilidades] = None
        self._folio: Optional[Portafolio] = None

    def result(self) -> CVObjects:
        if self._datos is None:
            raise ValueError("datospersonales no parseados")
        if self._form is None:
            raise ValueError("formacion no parseada")
        return CVObjects(
            cv_id=self._cv_id,
            datos=self._datos,
            formacion=self._form,
            idiomas=self._idiomas,
            experiencia=self._xp,
            habilidades=self._skills,
            portafolio=self._folio,
        )

    # ---------- ENTRY ----------
    def visitStart(self, ctx: CVLangParser.StartContext):
        return self.visit(ctx.cvs())

    def visitCvs(self, ctx: CVLangParser.CvsContext):
        cvs = ctx.cv()
        if not cvs:
            raise ValueError("No se encontró ningún bloque cv en el archivo.")
        # Si hay varios cv, aquí podrías iterar. Por ahora, usamos el primero:
        return self.visit(cvs[0])

    # ---------- CV ----------
    def visitCv(self, ctx: CVLangParser.CvContext):
        # Dependiendo de tu gramática, el nombre puede ser IDENT o algo similar.
        # Lo más robusto: usa getText() y extrae lo que haya tras 'cv'.
        # Si tu cv es: cv "Antonio Lobato" { ... }
        # suele existir IDENT() en el contexto.
        if hasattr(ctx, "IDENT") and ctx.IDENT():
            self._cv_id = _unquote(ctx.IDENT().getText())
        else:
            # fallback: intenta capturar el "nombre" desde el texto completo
            full = _ctx_text(ctx)
            # full empieza por "cv..." -> toma hasta la primera '{'
            head = full.split("{", 1)[0].strip()
            # quita el 'cv'
            head = head[2:].strip() if head.lower().startswith("cv") else head
            self._cv_id = _unquote(head) if head else "CV"

        self.visit(ctx.datospersonales())
        self.visit(ctx.formacion())

        if ctx.idiomas():
            self.visit(ctx.idiomas())
        if ctx.experiencia():
            self.visit(ctx.experiencia())
        if ctx.habilidades():
            self.visit(ctx.habilidades())
        if ctx.portafolio():
            self.visit(ctx.portafolio())

        return self.result()

    # ---------- DATOS PERSONALES ----------
    def visitDatospersonales(self, ctx: CVLangParser.DatospersonalesContext):
        nombre = _ctx_value(ctx.nomyape())
        datos = DatosPersonales(nombre=nombre)

        if ctx.foto():
            datos.foto = _ctx_value(ctx.foto())
        if ctx.fecha():
            datos.fecha_nacimiento = _ctx_value(ctx.fecha())
        if ctx.bio():
            datos.bio = _ctx_value(ctx.bio())

        c = ctx.contacto()
        datos.email = _ctx_value(c.email())
        datos.telefono = _ctx_value(c.telefono())

        if c.redes():
            redes = c.redes()
            if redes.linkedin():
                datos.linkedin = _ctx_value(redes.linkedin())
            if redes.github():
                datos.github = _ctx_value(redes.github())
            if redes.web():
                datos.web = _ctx_value(redes.web())

        self._datos = datos
        return None

    # ---------- FORMACIÓN ----------
    def visitFormacion(self, ctx: CVLangParser.FormacionContext):
        items: List[FormacionItem] = []

        for o in ctx.oficial():
            titulo = _ctx_value(o.titulo())
            inst = _ctx_value(o.expedidor())
            desc = _ctx_value(o.descripcion()) if o.descripcion() else None
            logros = _ctx_value(o.logros()) if o.logros() else None
            fecha = _ctx_value(o.fecha())

            items.append(
                FormacionItem(
                    titulo=titulo,
                    institucion=inst,
                    tipo="oficial",
                    descripcion=desc,
                    logros=logros,
                    fecha=fecha,
                    en_curso=False,
                )
            )

        # Si tienes complementaria en tu gramática, descomenta y adapta:
        if hasattr(ctx, "complementaria"):
            for c in ctx.complementaria() or []:
                titulo = _ctx_value(c.titulo())
                inst = _ctx_value(c.expedidor()) if hasattr(c, "expedidor") and c.expedidor() else "—"
                fecha = _ctx_value(c.fecha()) if hasattr(c, "fecha") and c.fecha() else None
                en_curso = (fecha or "").strip().lower() in {"en_curso", "encurso", "en curso"}
                items.append(
                    FormacionItem(
                        titulo=titulo,
                        institucion=inst,
                        tipo="complementaria",
                        descripcion=None,
                        logros=None,
                        fecha=fecha,
                        en_curso=en_curso,
                    )
                )

        self._form = Formacion(items=items)
        return None

    # ---------- IDIOMAS ----------
    def visitIdiomas(self, ctx: CVLangParser.IdiomasContext):
        lst: List[Idioma] = []
        for it in ctx.idioma():
            # En muchas gramáticas: idioma( Inglés nivel(B2) expedidor(...) )
            # Como no usamos value(), cogemos texto y buscamos sub-nodos:
            nombre = ""
            if hasattr(it, "CONJPALYNUM") and it.CONJPALYNUM():
                nombre = it.CONJPALYNUM().getText()
            else:
                nombre = _ctx_text(it).strip("()").strip()

            niv = _ctx_value(it.nivel()) if hasattr(it, "nivel") and it.nivel() else ""
            exp = _ctx_value(it.expedidor()) if hasattr(it, "expedidor") and it.expedidor() else None
            lst.append(Idioma(nombre=_unquote(nombre), nivel=niv, expedidor=exp))

        self._idiomas = Idiomas(idiomas=lst)
        return None

    # ---------- EXPERIENCIA ----------
    def visitExperiencia(self, ctx: CVLangParser.ExperienciaContext):
        items: List[ExperienciaItem] = []

        for l in ctx.laboral() or []:
            f = self._read_xp_block(l)
            items.append(
                ExperienciaItem(
                    tipo="laboral",
                    organizacion=f.get("organizacion", "—"),
                    puesto=f.get("puesto", "—"),
                    descripcion=f.get("descripcion"),
                    horas=int(f["horas"]) if "horas" in f and f["horas"] is not None else None,
                )
            )

        for v in ctx.voluntariado() or []:
            f = self._read_xp_block(v)
            items.append(
                ExperienciaItem(
                    tipo="voluntariado",
                    organizacion=f.get("organizacion", "—"),
                    puesto=f.get("puesto", "—"),
                    descripcion=f.get("descripcion"),
                    horas=int(f["horas"]) if "horas" in f and f["horas"] is not None else None,
                )
            )

        self._xp = Experiencia(experiencias=items)
        return None

    def _read_xp_block(self, ctx) -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        if hasattr(ctx, "organizacion") and ctx.organizacion():
            out["organizacion"] = _ctx_value(ctx.organizacion())
        if hasattr(ctx, "puesto") and ctx.puesto():
            out["puesto"] = _ctx_value(ctx.puesto())
        if hasattr(ctx, "horas") and ctx.horas():
            # horas(NUM) normalmente
            try:
                out["horas"] = _ctx_value(ctx.horas())
            except Exception:
                out["horas"] = None

        # laboral: responsabilidades(...)
        if hasattr(ctx, "responsabilidades") and ctx.responsabilidades():
            out["descripcion"] = _ctx_value(ctx.responsabilidades())

        # voluntariado: descripcion(...)
        if hasattr(ctx, "descripcion") and ctx.descripcion():
            out["descripcion"] = _ctx_value(ctx.descripcion())

        return out

    # ---------- HABILIDADES ----------
    def visitHabilidades(self, ctx: CVLangParser.HabilidadesContext):
        hs: List[Habilidad] = []

        if ctx.soft():
            for s in ctx.soft():
                for h in s.habilidad():
                    hs.append(Habilidad(nombre=_ctx_value(h), tipo="soft"))

        # Tu hard ha cambiado a categoria{...} en tu ejemplo.
        # Si tu gramática tiene categoria(), lo soportamos:
        if hasattr(ctx, "hard") and ctx.hard():
            for hd in ctx.hard():
                if hasattr(hd, "categoria") and hd.categoria():
                    for cat in hd.categoria():
                        # cat.getText() contiene todo el bloque; sacamos "nombre(...)", "habilidad(...)", "nvhab(...)"
                        txt = _ctx_text(cat)
                        # extrae simple por substrings (robusto para tu DSL)
                        cat_nombre = self._extract_field(txt, "nombre")
                        hab_nombre = self._extract_field(txt, "habilidad")
                        nivel = self._extract_field(txt, "nvhab")
                        if hab_nombre:
                            hs.append(Habilidad(nombre=hab_nombre, tipo="hard", categoria=cat_nombre, nivel=nivel))

        self._skills = Habilidades(habilidades=hs)
        return None

    def _extract_field(self, block_text: str, field: str) -> str:
        """
        Extrae field(...) de un texto como:
          categoria{nombre(Venta)habilidad(Vender coches)nvhab(alto)}
        """
        key = field + "("
        i = block_text.find(key)
        if i == -1:
            return ""
        j = block_text.find(")", i)
        if j == -1:
            return ""
        return _unquote(block_text[i + len(key) : j].strip())

    # ---------- PORTAFOLIO ----------
    def visitPortafolio(self, ctx: CVLangParser.PortafolioContext):
        proyectos: List[Proyecto] = []
        meritos: List[Merito] = []

        if hasattr(ctx, "proyecto") and ctx.proyecto():
            for p in ctx.proyecto():
                nombre = _ctx_value(p.nombre()) if hasattr(p, "nombre") and p.nombre() else ""
                desc = _ctx_value(p.descripcion()) if hasattr(p, "descripcion") and p.descripcion() else ""
                tec = _split_tecnologias(_ctx_value(p.tecnologias())) if hasattr(p, "tecnologias") and p.tecnologias() else []
                proyectos.append(Proyecto(nombre=nombre, descripcion=desc, categoria=None, tecnologias=tec))

        # Si en tu gramática existen meritos(), también podrías leerlos:
        if hasattr(ctx, "meritos") and ctx.meritos():
            for m in ctx.meritos():
                n = _ctx_value(m.nombre()) if hasattr(m, "nombre") and m.nombre() else ""
                d = _ctx_value(m.descripcion()) if hasattr(m, "descripcion") and m.descripcion() else ""
                meritos.append(Merito(nombre=n, descripcion=d))

        self._folio = Portafolio(proyectos=proyectos, meritos=meritos)
        return None
