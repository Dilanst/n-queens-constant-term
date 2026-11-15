"""Comparación de historias detenidas sin evaluar logaritmos."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from math import factorial
from exacto import exigir, soluciones


def clave(B):
    return tuple(sorted(B))

def disponibles(n,B):
    return tuple(r for r in range(n) if all(i!=r for i,_ in B))

def jugadas(n,B,r):
    return tuple((r,c) for c in range(n) if all(
        c!=j and abs(i-r)!=abs(j-c) for i,j in B))

def parada(regla,prof,r_anterior,descenso,n):
    return (prof==n or regla=="inicio" or (regla=="una" and prof>=1)
            or (regla=="orden" and descenso))

def familias(n):
    def racional(B):
        x=sum((r+1)*(c+2)**2 for r,c in B)
        return F(2+(x+3*len(B))%13, 1+(x+len(B))%5)
    return {"unidad": lambda B:F(1), "racional":racional}


def comprobar(n):
    sols=soluciones(n)
    total=len(sols)*factorial(n)
    @lru_cache(None)
    def hijos(B,r):
        return tuple(clave((*B,e)) for e in jugadas(n,B,r))
    @lru_cache(None)
    def Q(B):
        vivas=disponibles(n,B)
        return sum(Q(h) for h in hijos(B,vivas[0])) if vivas else 1
    exigir(Q(())==len(sols), "conteos de raíz distintos")

    resultados=[]
    for regla in ("inicio","una","orden","completa"):
        # Frecuencias independientes: la ley uniforme no utiliza pesos de inserción.
        mu=Counter()
        for p in sols:
            for orden in permutations(range(n)):
                pref=[]
                for r in orden:
                    prev=pref[-1][0] if pref else -1
                    descenso=len(pref)>=2 and pref[-1][0]<pref[-2][0]
                    if parada(regla,len(pref),prev,descenso,n):
                        break
                    pref.append((r,p[r]))
                mu[tuple(pref)]+=1
        exigir(sum(mu.values())==total, "falta masa de soluciones")

        for nombre,w0 in familias(n).items():
            w=lru_cache(None)(w0)
            @lru_cache(None)
            def S(B,r):
                return sum((w(h) for h in hijos(B,r)),F(0))

            # Sumar el número de hojas, incluidas las fallidas, y certificar su
            # masa total por inducción exacta. El tablero parcial conserva la última fila
            # y la condición de parada; se respetan las multiplicidades al sumar.
            @lru_cache(None)
            def arbol(B,ultima,descenso):
                if parada(regla,len(B),ultima,descenso,n):
                    return 1,int(Q(B)==0),F(1)
                vivos=disponibles(n,B); hojas=muertas=0; masa=F(0)
                for r in vivos:
                    H=hijos(B,r)
                    if not H:
                        hojas+=1; muertas+=1; masa+=F(1,len(vivos))
                        continue
                    for h in H:
                        num,fallos,submasa=arbol(h,r,(r<ultima if regla=="orden" else False))
                        hojas+=num;muertas+=fallos
                        masa+=w(h)*submasa/(S(B,r)*len(vivos))
                exigir(masa==1,"la referencia pierde masa en un tablero parcial")
                return hojas,muertas,masa

            hojas,fallos,masa=arbol((),-1,False)
            exigir(masa==1 and hojas-fallos==len(mu),"hojas o masa incorrectas")
            for pref, multiplicidad in mu.items():
                B=()
                nu=F(1); prod=F(1)
                # Dos lados formales: peso de cada tablero y normalizador de
                # cada fila son símbolos; las constantes Q y las probabilidades
                # de las filas se comprueban independientemente.
                izq=Counter(); der=Counter()
                orden_inv=1
                for d,(r,c) in enumerate(pref):
                    hijo=clave((*B,(r,c)))
                    exigir(hijo in hijos(B,r),"prefijo ilegal en la muestra uniforme")
                    normal=S(B,r)
                    nu*=w(hijo)/(normal*(n-d))
                    prod*=normal/w(B)
                    orden_inv*=n-d
                    izq[("s",B,r)]+=1; izq[("w",hijo)]-=1
                    der[("s",B,r)]+=1; der[("w",B)]-=1
                    B=hijo
                der[("w",())]+=1;der[("w",B)]-=1
                exigir(all(izq[t]==der[t] for t in set(izq)|set(der)),
                       "no se cancelan los pesos simbólicos")
                m=F(multiplicidad,total)
                exigir(m*orden_inv==F(Q(B),Q(())),"coeficiente de la identidad formal")
                exigir(m/nu==prod*Q(B)*w(())/(Q(())*w(B)),
                       "identidad puntual previa al logaritmo")
            if n==4 and regla=="una" and nombre=="unidad":
                # No usar Q para seleccionar a los hijos de la referencia.
                mala=sum((w(h)/(4*S((),r)) for r in range(4) for h in hijos((),r)
                          if not Q(h)),F(0))
                exigir(mala==F(1,2), "no se conservaron los hijos no completables")
            if n==4 and regla=="completa" and nombre=="unidad":
                B=(); prob=F(1)
                for r,c in ((0,0),(1,2)):
                    h=clave((*B,(r,c)))
                    prob*=w(h)/(len(disponibles(4,B))*S(B,r));B=h
                exigir(not hijos(B,2) and prob/len(disponibles(4,B))==F(1,192),
                       "se volvió a sortear una fila bloqueada")
            resultados.append({"n":n,"parada":regla,"pesos":nombre,
                               "historias":hojas,"sin_completacion":fallos,
                               "historias_con_masa_uniforme":len(mu)})
            arbol.cache_clear();S.cache_clear();w.cache_clear()
    return resultados

def verificar():
    return [x for n in (4,5,6) for x in comprobar(n)]
