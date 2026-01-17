grammar CVLang;

start           : cv EOF ;

cv              : 'cv' LBRACE cvId datospersonales formacion idiomas? experiencia? habilidades? portafolio? RBRACE ;

cvId            : 'id' LPAREN value RPAREN ;

datospersonales : 'datospersonales' LBRACE
                  nomyape foto? fecha? bio? contacto
                  RBRACE ;

nomyape         : 'nomyape' LPAREN value RPAREN ;
foto            : 'foto' LPAREN value RPAREN ;
fecha           : 'fecha' LPAREN value RPAREN ;
bio             : 'bio' LPAREN value RPAREN ;

contacto        : 'contacto' LBRACE email telefono redes RBRACE ;
email           : 'email' LPAREN value RPAREN ;
telefono        : 'telefono' LPAREN NUMBER RPAREN ;

redes           : 'redes' LBRACE linkedin? github? web? RBRACE ;
linkedin        : 'linkedin' LPAREN value RPAREN ;
github          : 'github' LPAREN value RPAREN ;
web             : 'web' LPAREN value RPAREN ;

/* -------- FORMACION -------- */
formacion       : 'formacion' LBRACE oficial+ complementaria* RBRACE ;

oficial         : 'oficial' LBRACE
                  titulo expedidor descripcion? logros? fecha
                  RBRACE ;

complementaria  : 'complementaria' LBRACE
                  titulo certificado? expedidor? horas? fecha
                  RBRACE ;

titulo          : 'titulo' LPAREN value RPAREN ;
expedidor       : 'expedidor' LPAREN value RPAREN ;
descripcion     : 'descripcion' LPAREN value RPAREN ;
logros          : 'logros' LPAREN value RPAREN ;
certificado     : 'certificado' LPAREN value RPAREN ;
horas           : 'horas' LPAREN NUMBER RPAREN ;

/* -------- IDIOMAS -------- */
idiomas         : 'idiomas' LBRACE idioma+ RBRACE ;
idioma          : 'idioma' LPAREN value nivel expedidor? RPAREN ;
nivel           : 'nivel' LPAREN value RPAREN ;

/* -------- EXPERIENCIA -------- */
experiencia     : 'experiencia' LBRACE (laboral | voluntariado)+ RBRACE ;

laboral         : 'laboral' LBRACE
                  (organizacion | puesto | horas | responsabilidades)+
                  RBRACE ;

voluntariado    : 'voluntariado' LBRACE
                  (organizacion | puesto | horas | descripcion)+
                  RBRACE ;

organizacion    : 'organizacion' LPAREN value RPAREN ;
puesto          : 'puesto' LPAREN value RPAREN ;
responsabilidades: 'responsabilidades' LPAREN value RPAREN ;

/* -------- HABILIDADES -------- */
habilidades     : 'habilidades' LBRACE (soft | hard)+ RBRACE ;

soft            : 'soft' LBRACE habilidad+ RBRACE ;

hard            : 'hard' LBRACE hard_item+ RBRACE ;
hard_item       : habilidad categoria nvhab ;

habilidad       : 'habilidad' LPAREN value RPAREN ;
categoria       : 'categoria' LPAREN value RPAREN ;
nvhab           : 'nvhab' LPAREN value RPAREN ;

/* -------- PORTAFOLIO -------- */
portafolio      : 'portafolio' LBRACE (proyecto | meritos)+ RBRACE ;

proyecto        : 'proyecto' LBRACE
                  nombre descripcion categoria tecnologias
                  RBRACE ;

meritos         : 'meritos' LBRACE
                  nombre descripcion
                  RBRACE ;

nombre          : 'nombre' LPAREN value RPAREN ;
tecnologias     : 'tecnologias' LPAREN value RPAREN ;

/* -------- LEXER -------- */
LBRACE          : '{' ;
RBRACE          : '}' ;
LPAREN          : '(' ;
RPAREN          : ')' ;

COMMENT         : '/*' .*? '*/' -> skip ;
WS              : [ \t\r\n]+ -> skip ;

NUMBER          : [0-9]+ ;
VALUE_CHUNK     : ~[)\r\n]+ ;
value           : VALUE_CHUNK ;
