"""Exact determinant of a complete example, computed without using its multiplicities."""
from fractions import Fraction as F
from math import lcm
from exacto import exigir

def inversa(A):
    n=len(A);T=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        i=next(i for i in range(j,n) if T[i][j]);T[i],T[j]=T[j],T[i]
        s=T[j][j];T[j]=[x/s for x in T[j]]
        for i in range(n):
            if i!=j and T[i][j]:
                a=T[i][j];T[i]=[x-a*y for x,y in zip(T[i],T[j])]
    return [row[n:] for row in T]

def determinante(A):
    n=len(A);d=lcm(*(x.denominator for row in A for x in row))
    T=[[int(x*d) for x in row] for row in A];anterior=1;signo=1
    for j in range(n-1):
        i=next((i for i in range(j,n) if T[i][j]),None)
        if i is None:return F(0)
        if i!=j:T[i],T[j]=T[j],T[i];signo=-signo
        piv=T[j][j]
        for i in range(j+1,n):
            for z in range(j+1,n):
                num=T[i][z]*piv-T[i][j]*T[j][z]
                coc,resto=divmod(num,anterior)
                exigir(resto==0,"exact division in the Bareiss algorithm");T[i][z]=coc
        anterior=piv
    return F(signo*T[-1][-1],d**n)

def verificar():
    k=5;p=F(1,k);q=1-p;t=p*q/(1-4*p);r=2*k-1
    filas=[(i,)+( (k+j,) if j<k-1 else () ) for i in range(k) for j in range(k)]
    gram=[[sum(a in f and b in f for f in filas) for b in range(r)] for a in range(r)]
    inv=inversa(gram);proj=[[sum(inv[a][b] for a in i for b in j) for j in filas] for i in filas]
    n=k*k
    U=[[q*(a==b)+t*((a//2==b//2)-proj[a//2][b//2]) for b in range(2*n)] for a in range(2*n)]
    valor=determinante(U)
    exigir(valor==q**(n+r)*(q+2*t)**(n-r),"direct determinant of the diagonal block")
    return {"k":k,"dimension":2*n,"determinante":str(valor)}
