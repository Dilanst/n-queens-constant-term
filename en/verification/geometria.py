"""Collisions among unordered pairs of empty crossings."""
from itertools import combinations
from math import comb
from exacto import exigir, soluciones

def elegir(n,k):
    return comb(n,k) if 0 <= k <= n else 0

def por_distancias(p):
    n = len(p)
    total = [0]*5
    for d in range(1,n):
        filas = {(i,i+d) for i in range(n-d)}
        cols = {(i,j) for i,j in combinations(range(n),2) if abs(p[i]-p[j])==d}
        iguales = len(filas & cols)
        grados_f = [sum(v in e for e in filas) for v in range(n)]
        grados_c = [sum(v in e for e in cols) for v in range(n)]
        uno = sum(a*b for a,b in zip(grados_f,grados_c))-2*iguales
        separados = len(filas)*len(cols)-iguales-uno
        for m, cantidad in zip((2,3,4),(iguales,uno,separados)):
            total[m] += 2*cantidad  # two diagonals of each geometric square
    return total

def cuenta_directa(p, I):
    # The column indices j are row labels, so the square is (i,p[j]).
    sol = [0]*5
    for (i,j),(u,v) in combinations([(i,j) for i in I for j in I],2):
        dist = abs(i-u)
        if dist and dist == abs(p[j]-p[v]):
            sol[len({i,j,u,v})] += 1
    return sol

CAMPOS = ("n","K","soluciones","subconjuntos","subconjuntos_con_choque",
          "testigos_2","testigos_3","testigos_4",
          "subconjuntos_con_2","subconjuntos_con_3","subconjuntos_con_4")

def verificar(nmax=8):
    filas = []
    for n in range(1,nmax+1):
        perms = soluciones(n)
        exigir(len(perms)==(1,0,0,2,10,4,40,92)[n-1], f"ordinary count for n={n}")
        por_K = [[0]*8 for _ in range(n+1)]
        for p in perms:
            full = por_distancias(p)
            exigir(full[2] == 0, "two-label collision in a solution")
            exigir(sum(full)==2*sum((n-d)**2 for d in range(1,n)), "initial board total")
            for K in range(n+1):
                datos=por_K[K]
                t=[0]*5
                for I in combinations(range(n),K):
                    a=cuenta_directa(p,I)
                    datos[0]+=1
                    datos[1]+=int(any(a))
                    for j in range(2,5):
                        t[j]+=a[j]
                        datos[3+j]+=int(a[j]>0)
                exigir(t[2:]==[full[j]*elegir(n-j,K-j) for j in (2,3,4)],
                       f"methods disagree for n={n}, K={K}, solution={p}")
                for j in range(2,5):
                    datos[j]+=t[j]
                if n==4 and K==4:
                    exigir(t[2:]==[0,24,4], "four-queens test oracle")
                if n==4 and K==3:
                    exigir(t[3]==24 and all(cuenta_directa(p,I)[3]==6
                           for I in combinations(range(n),K)), "three-row test oracle")
        for K, datos in enumerate(por_K):
            exigir(datos[0]==len(perms)*comb(n,K), "total number of subsets")
            filas.append(dict(zip(CAMPOS,(n,K,len(perms),*datos))))
    return filas
