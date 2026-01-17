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


def _v(ctx) -> str:
    """Devuelve el texto del rule value, limpiando espacios."""
    return ctx.getText().strip()


def _split_tecnologias(s: str) -> List[str]:
    raw = s.strip()
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
    # Puedes arrancar llamando visitor.visit(tree) donde tree sea parser.start() o parser.cv()
    def visitStart(self, ctx: CVLangParser.StartContext):
        return self.visit(ctx.cv())

    # ---------- TOP ----------
    def visitCv(self, ctx: CVLangParser.CvContext):
        self.visit(ctx.cvId())
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

    def visitCvId(self, ctx: CVLangParser.CvIdContext):
        self._cv_id = _v(ctx.value())
        return None

    # ---------- DATOS PERSONALES ----------
    def visitDatospersonales(self, ctx: CVLangParser.DatospersonalesContext):
        nombre = _v(ctx.nomyape().value())
        datos = DatosPersonales(nombre=nombre)

        if ctx.foto():
            datos.foto = _v(ctx.foto().value())
        if ctx.fecha():
            datos.fecha_nacimiento = _v(ctx.fecha().value())
        if ctx.bio():
            datos.bio = _v(ctx.bio().value())

        c = ctx.contacto()
        datos.email = _v(c.email().value())
        datos.telefono = c.telefono().NUMBER().getText()

        redes = c.redes()
        if redes.linkedin():
            datos.linkedin = _v(redes.linkedin().value())
        if redes.github():
            datos.github = _v(redes.github().value())
        if redes.web():
            datos.web = _v(redes.web().value())

        self._datos = datos
        return None

    # ---------- FORMACIÓN ----------
    def visitFormacion(self, ctx: CVLangParser.FormacionContext):
        items: List[FormacionItem] = []

        for o in ctx.oficial():
            titulo = _v(o.titulo().value())
            inst = _v(o.expedidor().value())
            desc = _v(o.descripcion().value()) if o.descripcion() else None
            logros = _v(o.logros().value()) if o.logros() else None
            fecha = _v(o.fecha().value())

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

        for c in ctx.complementaria():
            titulo = _v(c.titulo().value())
            inst = _v(c.expedidor().value()) if c.expedidor() else "—"
            fecha = _v(c.fecha().value()) if c.fecha() else None

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
            nombre = _v(it.value())
            niv = _v(it.nivel().value())
            exp = _v(it.expedidor().value()) if it.expedidor() else None
            lst.append(Idioma(nombre=nombre, nivel=niv, expedidor=exp))

        self._idiomas = Idiomas(idiomas=lst)
        return None

    # ---------- EXPERIENCIA ----------
    def visitExperiencia(self, ctx: CVLangParser.ExperienciaContext):
        items: List[ExperienciaItem] = []

        for l in ctx.laboral():
            f = self._read_xp_block(l)
            items.append(
                ExperienciaItem(
                    tipo="laboral",
                    organizacion=f.get("organizacion", "—"),
                    puesto=f.get("puesto", "—"),
                    descripcion=f.get("descripcion"),
                    horas=int(f["horas"]) if "horas" in f else None,
                )
            )

        for v in ctx.voluntariado():
            f = self._read_xp_block(v)
            items.append(
                ExperienciaItem(
                    tipo="voluntariado",
                    organizacion=f.get("organizacion", "—"),
                    puesto=f.get("puesto", "—"),
                    descripcion=f.get("descripcion"),
                    horas=int(f["horas"]) if "horas" in f else None,
                )
            )

        self._xp = Experiencia(experiencias=items)
        return None

    def _read_xp_block(self, ctx) -> Dict[str, Any]:
        out: Dict[str, Any] = {}

        # Estas reglas pueden repetirse (en tu gramática están como "+"),
        # así que recogemos la última aparición.
        if hasattr(ctx, "organizacion") and ctx.organizacion():
            # si hay varias, ctx.organizacion() puede ser lista en algunos targets, pero en ANTLR Python suele ser 1
            out["organizacion"] = _v(ctx.organizacion().value())
        if hasattr(ctx, "puesto") and ctx.puesto():
            out["puesto"] = _v(ctx.puesto().value())
        if hasattr(ctx, "horas") and ctx.horas():
            out["horas"] = ctx.horas().NUMBER().getText()

        # laboral: responsabilidades(...) -> la usamos como descripcion
        if hasattr(ctx, "responsabilidades") and ctx.responsabilidades():
            out["descripcion"] = _v(ctx.responsabilidades().value())

        # voluntariado: descripcion(...)
        if hasattr(ctx, "descripcion") and ctx.descripcion():
            out["descripcion"] = _v(ctx.descripcion().value())

        return out

    # ---------- HABILIDADES ----------
    def visitHabilidades(self, ctx: CVLangParser.HabilidadesContext):
        hs: List[Habilidad] = []

        for s in ctx.soft():
            for h in s.habilidad():
                hs.append(Habilidad(nombre=_v(h.value()), tipo="soft"))

        for hd in ctx.hard():
            for item in hd.hard_item():
                nombre = _v(item.habilidad().value())
                cat = _v(item.categoria().value())
                nv = _v(item.nvhab().value())
                hs.append(Habilidad(nombre=nombre, tipo="hard", categoria=cat, nivel=nv))

        self._skills = Habilidades(habilidades=hs)
        return None

    # ---------- PORTAFOLIO ----------
    def visitPortafolio(self, ctx: CVLangParser.PortafolioContext):
        proyectos: List[Proyecto] = []
        meritos: List[Merito] = []

        for p in ctx.proyecto():
            nombre = _v(p.nombre().value())
            desc = _v(p.descripcion().value())
            cat = _v(p.categoria().value())
            tec = _split_tecnologias(_v(p.tecnologias().value()))
            proyectos.append(Proyecto(nombre=nombre, descripcion=desc, categoria=cat, tecnologias=tec))

        for m in ctx.meritos():
            meritos.append(Merito(nombre=_v(m.nombre().value()), descripcion=_v(m.descripcion().value())))

        self._folio = Portafolio(proyectos=proyectos, meritos=meritos)
        return None
