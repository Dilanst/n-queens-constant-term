"""Inventory of formulas and constants in the LaTeX sources."""
import json
import re
from pathlib import Path
from collections import Counter
from exacto import exigir

ENTORNO = r"(?:equation|align|alignat|gather|multline|flalign|displaymath|math)\*?"
INICIO = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}|\\begin\{("+ENTORNO+
                    r")\}|\\\[|\\\(|(?<!\\)\$\$|(?<!\\)\$")
VOCAB = re.compile(r"(?<![^\W\d_])(?:[+\-−]?\d+(?:[.,]\d+)*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|half|double|triple)(?![^\W\d_])",re.I)
LEX = re.compile(r"\\[a-zA-Z@]+|\\.|[^\W\d_]+|\d+|[^\s]")
MAC = re.compile(r"(?m)^\s*(\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator|def|newtheorem)\b[^\n]+)")
ANCHAS = {
 "pivot":(r"\tau_d-\frac{\tau_d^2}{q+\tau_d}=\tau_{d-1}",r"b_d(q+\tau_d)=b_{d-1}"),
 "rectangle":(r"{\rm tr}((EE^T)^2)",),
 "prefactor":(r"-5a_2+O(k^{-1})",r"4a_2+O(k^{-1})",r"\log\det U=a_2+O(\varepsilon_{\rm out}+k^{-1})"),
 "generator":(r"-\frac{Y_e(s)}{k}\bigl(2+\ell_{D(e)}+\ell_{A(e)}-3p_e\bigr)",),
 "permanent":(r"\pdet S_0=2\det(I-B^TB)",),
 "covolume":(r"-\tfrac12\bigl((-5+4+1)a_2\bigr)",),
 "histories":(r"g(B_0)=\E_\mu[A_\tau+g(B_\tau)]-D(\mu^\tau\Vert\nu^\tau)",)
}

def normal(s):
    return " ".join(LEX.findall(s))

def sin_comentarios(s):
    return re.sub(r"(?<!\\)(?:\\\\)*%[^\n]*", lambda m:m.group(0).split("%")[0],s)

def extraer(s):
    # Both branches of each listed literal typesetting alternative are inspected.
    for nombre in ("microtype.sty", "titlesec.sty"):
        s=s.replace(r"\IfFileExists{"+nombre+"}", "")
    s=sin_comentarios(s)
    if re.search(r"\\(?:includeonly|subfile|import|subimport|InputIfFileExists|IfFileExists|catcode|csname|write18|openin|read)\b|\\(?:input|include)(?![a-zA-Z]|\s*\{)",s):
        raise ValueError("Dynamic input or unsupported inclusion syntax.")
    activos=[]; hijos=[]; pos=0
    def prosa(a):
        activos.extend(("texto",m.group(0).casefold()) for m in VOCAB.finditer(a))
    for m in MAC.finditer(s):
        activos.append(("definicion",normal(m.group(1))))
    while True:
        m=INICIO.search(s,pos)
        if not m:
            prosa(s[pos:]); break
        prosa(s[pos:m.start()]); signal=m.group()
        if m.group(1):
            hijo=m.group(1); hijos.append(hijo);activos.append(("inclusion",hijo));pos=m.end();continue
        if m.group(2):
            fin=r"\end{"+m.group(2)+"}"
        else:
            fin={r"\[":r"\]",r"\(":r"\)","$":"$","$$":"$$"}[signal]
        cierre=re.search((r"(?<!\\)" if fin[0]=="$" else "")+re.escape(fin),s[m.end():])
        if not cierre:raise ValueError("Unclosed formula: "+signal)
        i=m.end()+cierre.start();activos.append(("formula",normal(s[m.end():i])))
        pos=i+len(fin)
    return activos,hijos

def inventario(main):
    main=Path(main)
    if main.is_dir():main=main/"main.tex"
    main=main.resolve(strict=True);base=main.parent; datos={};visitando=set()
    def visita(path):
        path=path.resolve(strict=True)
        if not path.is_relative_to(base) or path.suffix!=".tex":
            raise ValueError("Source outside the project tree or with an unexpected extension.")
        nombre=path.relative_to(base).as_posix()
        if nombre in visitando:raise ValueError("Circular inclusion: "+nombre)
        if nombre in datos:return
        visitando.add(nombre)
        tablas,hijos=extraer(path.read_text(encoding="utf-8-sig"))
        datos[nombre]=[list(i) for i in tablas]
        for h in hijos:
            child=Path(h)
            if child.is_absolute() or ".." in child.parts:raise ValueError("Inclusions must use relative paths within the project.")
            visita(base/(child if child.suffix else child.with_suffix(".tex")))
        visitando.remove(nombre)
    visita(main)
    return datos

def diferencia(ref,cand):
    if set(ref)!=set(cand):return "Different file sets: "+str(sorted(set(ref)^set(cand)))
    for f,items in ref.items():
        other=cand[f]
        for i in range(max(len(items),len(other))):
            a=items[i] if i<len(items) else None;b=other[i] if i<len(other) else None
            if a!=b:return f"{f}, item {i+1}: expected {str(a)[:160]}; found {str(b)[:160]}."
    return ""

def verificar(articulo):
    catalogo=Path(__file__).parent/"catalogo.json"
    ref=json.loads(catalogo.read_text(encoding="utf-8")); actual=inventario(articulo)
    d=diferencia(ref,actual)
    if d:raise ValueError(d)
    todo=[" "+x[1]+" " for xs in actual.values() for x in xs if x[0]=="formula"]
    for nombre,formas in ANCHAS.items():
        for forma in formas:exigir(any(" "+normal(forma)+" " in s for s in todo),"Missing formula: "+nombre)
    return {"archivos":len(actual),**dict(sorted(Counter(x[0] for items in actual.values() for x in items).items()))}
