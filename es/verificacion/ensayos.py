"""Controles negativos del cotejo. Se comparan muestras en memoria."""
from cotejo import extraer, diferencia, normal
from exacto import exigir

def verificar():
    def tabla(s):return {"ejemplo.tex":[list(x) for x in extraer(s)[0]]}
    base=r"Dos pares; valor 0,125. $a+b$ \[z=3\]\input{fin}"
    cambios=[("signo",base.replace("a+b","a-b")),("cifra",base.replace("125","124")),
             ("número en letras",base.replace("Dos","Tres")),("fórmula añadida",base+" $a$"),
             ("inclusión",base.replace(r"\input{fin}",""))]
    for a,b in [("-5a_2","-6a_2"),("4a_2","3a_2"),("a_2","2a_2")]:
        cambios.append(("prefactor "+a,None))
        exigir(diferencia(tabla("$"+a+"$"),tabla("$"+b+"$")),"Cambio no detectado: "+a)
    for n,s in cambios:
        if s is not None:exigir(diferencia(tabla(base),tabla(s)),"Cambio no detectado: "+n)
    exigir(diferencia(tabla(base),{}),"Sección ausente no detectada")
    exigir(not diferencia(tabla(base),tabla(base.replace("a+b"," a + b "))),"Espaciado inocuo")
    exigir(normal(r"\log x")!=normal(r"\logx"),"Una macro no debe confundirse con dos símbolos")
    return {"alteraciones_detectadas":len(cambios)+1,"controles_positivos":2}
