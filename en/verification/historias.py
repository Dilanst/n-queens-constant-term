"""Compare stopped histories without evaluating logarithms."""
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
    exigir(Q(())==len(sols), "root counts differ")

    resultados=[]
    for regla in ("inicio","una","orden","completa"):
        # Compute frequencies independently under the uniform law, without insertion weights.
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
        exigir(sum(mu.values())==total, "missing solution mass")

        for nombre,w0 in familias(n).items():
            w=lru_cache(None)(w0)
            @lru_cache(None)
            def S(B,r):
                return sum((w(h) for h in hijos(B,r)),F(0))

            # Count the leaves, including failures, and certify their total mass by
            # exact induction. The partial board retains the last row and the stopping
            # condition. The sum accounts for multiplicities.
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
                exigir(masa==1,"the reference law loses mass on a partial board")
                return hojas,muertas,masa

            hojas,fallos,masa=arbol((),-1,False)
            exigir(masa==1 and hojas-fallos==len(mu),"incorrect leaf count or mass")
            for pref, multiplicidad in mu.items():
                B=()
                nu=F(1); prod=F(1)
                # On both sides of the formal identity, each board weight and row
                # normalizer is symbolic. Check the constants Q and the row probabilities
                # independently.
                izq=Counter(); der=Counter()
                orden_inv=1
                for d,(r,c) in enumerate(pref):
                    hijo=clave((*B,(r,c)))
                    exigir(hijo in hijos(B,r),"illegal prefix in the uniform sample")
                    normal=S(B,r)
                    nu*=w(hijo)/(normal*(n-d))
                    prod*=normal/w(B)
                    orden_inv*=n-d
                    izq[("s",B,r)]+=1; izq[("w",hijo)]-=1
                    der[("s",B,r)]+=1; der[("w",B)]-=1
                    B=hijo
                der[("w",())]+=1;der[("w",B)]-=1
                exigir(all(izq[t]==der[t] for t in set(izq)|set(der)),
                       "symbolic weights fail to cancel")
                m=F(multiplicidad,total)
                exigir(m*orden_inv==F(Q(B),Q(())),"coefficient of the formal identity")
                exigir(m/nu==prod*Q(B)*w(())/(Q(())*w(B)),
                       "pointwise identity before taking logarithms")
            if n==4 and regla=="una" and nombre=="unidad":
                # Choose the children under the reference law independently of Q.
                mala=sum((w(h)/(4*S((),r)) for r in range(4) for h in hijos((),r)
                          if not Q(h)),F(0))
                exigir(mala==F(1,2), "children without a completion were discarded")
            if n==4 and regla=="completa" and nombre=="unidad":
                B=(); prob=F(1)
                for r,c in ((0,0),(1,2)):
                    h=clave((*B,(r,c)))
                    prob*=w(h)/(len(disponibles(4,B))*S(B,r));B=h
                exigir(not hijos(B,2) and prob/len(disponibles(4,B))==F(1,192),
                       "a blocked row triggered a redraw")
            resultados.append({"n":n,"parada":regla,"pesos":nombre,
                               "historias":hojas,"sin_completacion":fallos,
                               "historias_con_masa_uniforme":len(mu)})
            arbol.cache_clear();S.cache_clear();w.cache_clear()
    return resultados

def verificar():
    return [x for n in (4,5,6) for x in comprobar(n)]
