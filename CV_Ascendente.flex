/* ======== Analizador léxico JFlex corregido ======== */

import java_cup.runtime.Symbol;

%%

%class Yylex
%unicode
%line
%column
%cup
%state COMMENT


/* ======== Macros ======== */


<YYINITIAL>{IDENT}       { return new Symbol(sym.IDENT, yytext()); }
<YYINITIAL>{NVH}         { return new Symbol(sym.NVH, yytext()); }
<YYINITIAL>{NVI}         { return new Symbol(sym.NVI, yytext()); }
<YYINITIAL>{BOOL}        { return new Symbol(sym.BOOL, yytext()); }
<YYINITIAL>{FECHA_NUM}   { return new Symbol(sym.FECHA_NUM, yytext()); }
<YYINITIAL>{RUTA}        { return new Symbol(sym.RUTA, yytext()); }
<YYINITIAL>{MAIL}        { return new Symbol(sym.MAIL, yytext()); }
<YYINITIAL>{TFNO}        { return new Symbol(sym.TFNO, yytext()); }
<YYINITIAL>{NUM}         { return new Symbol(sym.NUM, yytext()); }
<YYINITIAL>{CONJPALYNUM} { return new Symbol(sym.CONJPALYNUM, yytext()); }


%%

/* ================================================== */
/* ==================   REGLAS   ==================== */
/* ================================================== */

/* ======== Comentarios estilo C ======== */
<COMMENT> "*/"                   { yybegin(YYINITIAL); }
<COMMENT> <<EOF>>                { System.err.println("Error léxico en la línea " + (yyline+1) + ", columna " + (yycolumn+1) + ": Fin de archivo dentro de comentario."); System.exit(1); }
<COMMENT> .                      {} /* ignorar contenido del comentario */

/* ======== Palabras clave ======== */
<YYINITIAL>"cv"                  { return new Symbol(sym.CV); }
<YYINITIAL>"gvar"                { return new Symbol(sym.GVAR); }
<YYINITIAL>"lvar"                { return new Symbol(sym.LVAR); }

<YYINITIAL>"datospersonales"     { return new Symbol(sym.DP); }
<YYINITIAL>"nomyape"             { return new Symbol(sym.NOMYAPE); }
<YYINITIAL>"foto"                { return new Symbol(sym.FOTO); }
<YYINITIAL>"fecha"               { return new Symbol(sym.FECHA); }
<YYINITIAL>"bio"                 { return new Symbol(sym.BIO); }
<YYINITIAL>"contacto"            { return new Symbol(sym.CONTACTO); }
<YYINITIAL>"email"               { return new Symbol(sym.EMAIL); }
<YYINITIAL>"telefono"            { return new Symbol(sym.TELEFONO); }
<YYINITIAL>"redes"               { return new Symbol(sym.REDES); }
<YYINITIAL>"linkedin"            { return new Symbol(sym.LINKEDIN); }
<YYINITIAL>"github"              { return new Symbol(sym.GITHUB); }
<YYINITIAL>"web"                 { return new Symbol(sym.WEB); }

<YYINITIAL>"formacion"           { return new Symbol(sym.FORMACION); }
<YYINITIAL>"oficial"             { return new Symbol(sym.OFICIAL); }
<YYINITIAL>"titulo"              { return new Symbol(sym.TITULO); }
<YYINITIAL>"expedidor"           { return new Symbol(sym.EXPEDIDOR); }
<YYINITIAL>"descripcion"         { return new Symbol(sym.DESCRIPCION); }
<YYINITIAL>"logros"              { return new Symbol(sym.LOGROS); }
<YYINITIAL>"complementaria"      { return new Symbol(sym.COMPLEMENTARIA); }
<YYINITIAL>"certificado"         { return new Symbol(sym.CERTIFICADO); }
<YYINITIAL>"horas"               { return new Symbol(sym.HORAS); }

<YYINITIAL>"idiomas"             { return new Symbol(sym.IDIOMAS); }
<YYINITIAL>"idioma"              { return new Symbol(sym.IDIOMA); }
<YYINITIAL>"nivel"               { return new Symbol(sym.NIVEL); }

<YYINITIAL>"experiencia"         { return new Symbol(sym.EXPERIENCIA); }
<YYINITIAL>"laboral"             { return new Symbol(sym.LABORAL); }
<YYINITIAL>"puesto"              { return new Symbol(sym.PUESTO); }
<YYINITIAL>"responsabilidades"   { return new Symbol(sym.RESPONSABILIDADES); }
<YYINITIAL>"voluntariado"        { return new Symbol(sym.VOLUNTARIADO); }
<YYINITIAL>"organizacion"        { return new Symbol(sym.ORGANIZACION); }

<YYINITIAL>"habilidades"         { return new Symbol(sym.HABILIDADES); }
<YYINITIAL>"soft"                { return new Symbol(sym.SOFT); }
<YYINITIAL>"hard"                { return new Symbol(sym.HARD); }
<YYINITIAL>"habilidad"           { return new Symbol(sym.HABILIDAD); }
<YYINITIAL>"nvhab"               { return new Symbol(sym.NVHAB); }
<YYINITIAL>"categoria"           { return new Symbol(sym.CATEGORIA); }

<YYINITIAL>"portafolio"          { return new Symbol(sym.PORTAFOLIO); }
<YYINITIAL>"proyecto"            { return new Symbol(sym.PROYECTO); }
<YYINITIAL>"nombre"              { return new Symbol(sym.NOMBRE); }
<YYINITIAL>"grupo"               { return new Symbol(sym.GRUPO); }
<YYINITIAL>"companero"           { return new Symbol(sym.COMPANERO); }
<YYINITIAL>"tecnologias"         { return new Symbol(sym.TECNOLOGIAS); }
<YYINITIAL>"meritos"             { return new Symbol(sym.MERITOS); }

/* ======== Símbolos y operadores ======== */
<YYINITIAL>"/*"                  { yybegin(COMMENT); }

<YYINITIAL>"{" { return new Symbol(sym.LL_A); }
<YYINITIAL>"}" { return new Symbol(sym.LL_C); }
<YYINITIAL>"(" { return new Symbol(sym.PA_A); }
<YYINITIAL>")" { return new Symbol(sym.PA_C); }
<YYINITIAL>"=" { return new Symbol(sym.IG); }
<YYINITIAL>";" { return new Symbol(sym.PYC); }
<YYINITIAL>"," { return new Symbol(sym.CO); }

/* ======== Macros ======== */
<YYINITIAL>{IDENT}       { return new Symbol(sym.IDENT); }
<YYINITIAL>{NVH}         { return new Symbol(sym.NVH); }
<YYINITIAL>{NVI}         { return new Symbol(sym.NVI); }
<YYINITIAL>{BOOL}        { return new Symbol(sym.BOOL); }
<YYINITIAL>{FECHA_NUM}   { return new Symbol(sym.FECHA_NUM); }
<YYINITIAL>{RUTA}        { return new Symbol(sym.RUTA); }
<YYINITIAL>{MAIL}        { return new Symbol(sym.MAIL); }
<YYINITIAL>{TFNO}        { return new Symbol(sym.TFNO); }
<YYINITIAL>{NUM}         { return new Symbol(sym.NUM); }
<YYINITIAL>{CONJPALYNUM} { return new Symbol(sym.CONJPALYNUM); }

/* ======== Espacios en blanco ======== */
{WS}                {} /* ignorar */

/* ======== Error léxico ======== */
<YYINITIAL>.                    {System.err.println("Error léxico en la línea " + (yyline) + ", columna " + (yycolumn) + ": carácter inesperado '" + yytext() + "'"); System.exit(1); }
