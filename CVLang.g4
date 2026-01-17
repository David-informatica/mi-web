grammar CVLang;

// ======== Palabras clave ========
CV              : 'cv' ;
GVAR            : 'gvar' ;
LVAR            : 'lvar' ;

DP              : 'datospersonales' ;
NOMYAPE         : 'nomyape' ;
FOTO            : 'foto' ;
FECHA           : 'fecha' ;
BIO             : 'bio' ;
CONTACTO        : 'contacto' ;
EMAIL           : 'email' ;
TELEFONO        : 'telefono' ;
REDES           : 'redes' ;
LINKEDIN        : 'linkedin' ;
GITHUB          : 'github' ;
WEB             : 'web' ;

FORMACION       : 'formacion' ;
OFICIAL         : 'oficial' ;
TITULO          : 'titulo' ;
EXPEDIDOR       : 'expedidor' ;
DESCRIPCION     : 'descripcion' ;
LOGROS          : 'logros' ;
COMPLEMENTARIA  : 'complementaria' ;
CERTIFICADO     : 'certificado' ;
HORAS           : 'horas' ;

IDIOMAS         : 'idiomas' ;
IDIOMA          : 'idioma' ;
NIVEL           : 'nivel' ;

EXPERIENCIA     : 'experiencia' ;
LABORAL         : 'laboral' ;
PUESTO          : 'puesto' ;
RESPONSABILIDADES: 'responsabilidades' ;
VOLUNTARIADO    : 'voluntariado' ;
ORGANIZACION    : 'organizacion' ;


HABILIDADES     : 'habilidades' ;
SOFT            : 'soft' ;
HARD            : 'hard' ;
HABILIDAD       : 'habilidad' ;
NVHAB           : 'nvhab' ;
CATEGORIA       : 'categoria' ;

PORTAFOLIO      : 'portafolio' ;
PROYECTO        : 'proyecto' ;
NOMBRE          : 'nombre' ;
GRUPO           : 'grupo' ;
COMPANERO       : 'companero' ;
TECNOLOGIAS     : 'tecnologias' ;
MERITOS         : 'meritos' ;


// ======== Símbolos ========
LL_A            : '{' ;
LL_C            : '}' ;
PA_A            : '(' ;
PA_C            : ')' ;
IG              : '=' ;
PYC             : ';' ;
CO              : ',' ;

// ======== Comentarios estilo C ========
COMMENT
    : '/*' ( ~'*' | '*' ~'/' )* '*/' -> skip
    ;

UNCLOSED_COMMENT
    : '/*' ( ~'*' | '*' ~'/' )* EOF
      { raise Exception("Error lexico: comentario no cerrado antes del fin de archivo."); }
    ;

UNOPENED_COMMENT
    : '*/'
      { raise Exception("Error lexico: comentario no abierto."); }
    ;

// ======== Macros ========

WS              : [ \t\r\n]+ -> skip ;
NUM             : ('0' | [1-9][0-9]*) ;
PAL             : [A-Za-zÁÉÍÓÚáéíóúÑñ]+ ;
TFNO            : ([5-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]) ;
MAIL            : [A-Za-z0-9]+ ('.' [A-Za-z0-9]+)* '@' [A-Za-z0-9]+ ('.' [A-Za-z0-9]+)* ;
RUTA            : [A-Za-z]+ ( [./\-:]+ [A-Za-z]+ )+ ;
FECHA_NUM       : ('0'[1-9] | [12][0-9] | '30' | '31') '/' ('0'[1-9] | '1'[0-2]) '/' ([12][0-9][0-9][0-9]);
BOOL            : 'Si' | 'No' ;
NVI             : ([ABC][12]) | 'nativo' ;
NVH             : 'bajo' | 'medio' | 'alto' ;
IDENT           : '"' CONJPALYNUM '"' ;
CONJPALYNUM     : PAL (','? (WS (PAL | NUM)) '.'?)* ;

// ======== Manejo de errores ========
ERROR : . { System.err.println("Error léxico: carácter no reconocido " + getText()); } ;

// ========== Sintaxis ==========
start:          cvs EOF ;

cvs:            global_var? cv+ ;
        
global_var:     GVAR LL_A variable+ LL_C ;
local_var:      LVAR LL_A variable+ LL_C;
variable:       IDENT IG CONJPALYNUM PYC ;

cv:             CV IDENT LL_A local_var? datospersonales formacion idiomas? experiencia? habilidades? portafolio? LL_C ;

datospersonales:DP LL_A nomyape foto? fecha bio? contacto LL_C ;
nomyape:        NOMYAPE PA_A (CONJPALYNUM|IDENT) PA_C ;
foto:           FOTO PA_A RUTA PA_C ;
fecha:          FECHA PA_A FECHA_NUM PA_C ;
bio:            BIO PA_A (CONJPALYNUM|IDENT) PA_C ;
contacto:       CONTACTO LL_A email telefono redes LL_C ;
email:          EMAIL PA_A MAIL PA_C ;
telefono:       TELEFONO PA_A TFNO PA_C ;
redes:          REDES LL_A (linkedin github? web?
            |   github web?
            |   web) LL_C;
linkedin:       LINKEDIN PA_A RUTA PA_C ;
github:         GITHUB PA_A RUTA PA_C ;
web:            WEB PA_A RUTA PA_C ;

formacion:      FORMACION LL_A oficial+ complementaria* LL_C ;
oficial:        OFICIAL LL_A titulo expedidor descripcion? logros? fecha LL_C ;
titulo:         TITULO PA_A (CONJPALYNUM|IDENT) PA_C ;
expedidor:      EXPEDIDOR PA_A (CONJPALYNUM|IDENT) PA_C ;
descripcion:    DESCRIPCION PA_A (CONJPALYNUM|IDENT) PA_C ;
logros:         LOGROS PA_A (CONJPALYNUM|IDENT) PA_C ;
complementaria: COMPLEMENTARIA LL_A titulo certificado? expedidor horas? fecha LL_C;
certificado:    CERTIFICADO PA_A BOOL PA_C;
horas:          HORAS PA_A NUM PA_C; 

idiomas:        IDIOMAS LL_A idioma+ LL_C ;
idioma:         IDIOMA LL_A nombre nvi expedidor? LL_C  ;
nvi:            NIVEL PA_A NVI PA_C ;

experiencia:    EXPERIENCIA LL_A (laboral+ voluntariado* | voluntariado+) LL_C;
laboral:        LABORAL LL_A puesto horas organizacion responsabilidades? LL_C;
puesto:         PUESTO PA_A (CONJPALYNUM|IDENT) PA_C;
responsabilidades: RESPONSABILIDADES PA_A (CONJPALYNUM|IDENT) PA_C;
voluntariado:   VOLUNTARIADO LL_A puesto descripcion horas organizacion LL_C;
organizacion:   ORGANIZACION PA_A (CONJPALYNUM|IDENT) PA_C;

habilidades:    HABILIDADES LL_A (soft hard? | hard) LL_C ;
soft:           SOFT LL_A habilidad (CO habilidad)* LL_C;
hard:           HARD LL_A categoria+ LL_C;
nvh:            NVHAB PA_A NVH PA_C;
habilidad:      HABILIDAD PA_A (CONJPALYNUM|IDENT) PA_C;
categoria:      CATEGORIA LL_A nombre habilidad nvh (CO habilidad nvh)* LL_C;

portafolio:     PORTAFOLIO LL_A (proyecto+ merito* | merito+) LL_C;
proyecto:       PROYECTO LL_A nombre grupo? descripcion tecnologias web? LL_C;
nombre:         NOMBRE PA_A (CONJPALYNUM|IDENT) PA_C;
grupo:          GRUPO LL_A companero+ LL_C;
companero:      COMPANERO LL_A nomyape github? LL_C;
tecnologias:    TECNOLOGIAS PA_A (CONJPALYNUM|IDENT) PA_C;
merito:         MERITOS LL_A nombre descripcion LL_C;
