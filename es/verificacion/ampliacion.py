"""Controles exactos del revelado y del escalado. Sólo biblioteca estándar."""
from fractions import Fraction as F
from itertools import permutations, combinations
from math import factorial
from exacto import exigir, soluciones
from matriz import determinante


def permanente(a):
    n=len(a)
    def producto(seq):
        x=F(1)
        for y in seq:x*=y
        return x
    return sum((producto(a[i][j] for i,j in enumerate(p)) for p in permutations(range(n))),F(0))


def generador():
    """Contar directamente las elecciones que borran cada casilla disponible."""
    casos=0; aristas=0
    for n in (4,5,6):
        sol=soluciones(n);estados=set()
        for s in sol:
            for h in range(n):
                for I in combinations(range(n),h):
                    estados.add(tuple((i,s[i]) for i in I))
        for B in sorted(estados):
            M=[p for p in sol if all(p[i]==j for i,j in B)]
            R=set(range(n))-{i for i,_ in B};k=len(R)
            C=set(range(n))-{j for _,j in B}
            # Mezcla no uniforme de completaciones, usada sólo para producir
            # sumas de filas y columnas iguales a uno. La identidad no requiere estacionariedad.
            e={(i,j) for i in R for j in C if all(abs(i-u)!=abs(j-v) for u,v in B)}
            W=sum(range(1,len(M)+1))
            p={(i,j):F(sum(t for t,s in enumerate(M,1) if s[i]==j),W) for i,j in e}
            for i,j in e:
                pd=sum(v for (a,b),v in p.items() if a-b==i-j)
                pa=sum(v for (a,b),v in p.items() if a+b==i+j)
                total=sum(v for (a,b),v in p.items() if a==i or b==j or abs(a-i)==abs(b-j))
                exigir(total/k==(2+pd+pa-3*p[i,j])/k,"generador de casillas")
                aristas+=1
            casos+=1
    return {"residuales":casos,"casillas_comprobadas":aristas}


def espectro():
    """Comparar cofactor y determinante de Gram sin calcular autovalores."""
    salida=[]
    for n in (5,6,7):
        coef=[0]+list(range(1,n))
        P=[[F(coef[(j-i)%n],sum(coef)) for j in range(n)] for i in range(n)]
        A=[[F(0) for _ in range(2*n)] for _ in range(2*n)]
        for i in range(n):
            for j in range(n):
                p=P[i][j]
                A[i][i]+=p;A[n+j][n+j]+=p;A[i][n+j]+=p;A[n+j][i]+=p
        B=[[p-F(1,n) for p in r] for r in P]
        U=[[F(i==j)-sum(row[i]*row[j] for row in B) for j in range(n)] for i in range(n)]
        z=determinante(U)
        cof=determinante([row[:-1] for row in A[:-1]])
        exigir(2*n*cof==2*z and z>0,"cofactor RC y determinante de Gram")
        # Covolumen comprobado también por un desplazamiento del modo cero.
        g=[1]*n+[-1]*n
        shift=[[A[i][j]+F(g[i]*g[j],2*n) for j in range(2*n)] for i in range(2*n)]
        exigir(determinante(shift)==2*z,"modo cero y proyector")
        W=[[p*(1-p) for p in r] for r in P]
        a=[F(i+1,i+2) for i in range(n)];b=[F(i+3,2) for i in range(n)]
        D=[[a[i]*b[j]*W[i][j] for j in range(n)] for i in range(n)]
        mult=F(1)
        for x,y in zip(a,b):mult*=x*y
        exigir(permanente(D)==mult*permanente(W),"escalado diagonal con ceros")
        salida.append({"K":n,"determinante":str(z)})
    return salida


def auxiliares():
    """Multiplicidades virtuales por construcción independiente."""
    pruebas=[]
    for h in (1,2,3):
        P=list(permutations(range(h)))
        objetos={tuple((r,b[r],d[r],a[r]) for r in range(h)) for b in P for d in P for a in P}
        exigir(len(objetos)==factorial(h)**3,"completaciones virtuales")
        pruebas.append(len(objetos))
    return pruebas


def verificar():
    return {"generador":generador(),"determinantes_y_escalado":espectro(),
            "multiplicidades_virtuales":auxiliares()}
