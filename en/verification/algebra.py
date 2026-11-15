"""Polynomial identities and rational arithmetic, without parameter fitting."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
from exacto import Pol, Coc, exigir


def pivotes():
    p = Pol(0, 1)
    q = 1-p
    tau = lambda d: Coc(p*q, 1-d*p)
    b = lambda d: Coc(1-d*p, q**d)
    for d in (3, 4):
        piv = Coc(q) + tau(d)
        exigir(piv == Coc(q*(1-(d-1)*p), 1-d*p), f"pivot {d}")
        exigir(tau(d) - tau(d)*tau(d)/piv == tau(d-1), f"Schur {d}")
        exigir(b(d)*piv == b(d-1), f"local factor {d}")
    return (3, 4)


def motivos():
    # Interpolate the mask expansion in four Boolean markers.
    bits = range(16)
    pop = lambda x: bin(x).count("1")
    u = (2, 3, 5, 7)
    v = (11, 13, 17, 19)
    def mult(xs):
        a = 1
        for x in xs:
            a *= x
        return a
    valores = {s: mult((u[i] if (s >> i) & 1 else 0)-v[i]
                        for i in range(4)) for s in bits}
    for s in bits:
        coeff = sum((-1)**(pop(s)-pop(t))*valores[t]
                    for t in bits if t & s == t)
        term = (-1)**(4-pop(s))*mult(u[i] if (s >> i) & 1 else v[i] for i in range(4))
        exigir(coeff == term, f"labeled motif {s:04b}")
    # Polynomial identity, including repeated indices.
    # First expand the entries of the Gram matrix, then square them.
    gram2, rect = Counter(), Counter()
    for i, k in product(range(2), repeat=2):
        gram = Counter()
        for j in range(3):
            for a, b in product((0, 1), repeat=2):
                gram[tuple(sorted(((a,i,j), (b,k,j))))] += (-1)**(a+b)
        for l, x in gram.items():
            for r, y in gram.items():
                gram2[tuple(sorted(l+r))] += x*y
        for j, l in product(range(3), repeat=2):
            sites = ((i,j), (k,j), (k,l), (i,l))
            for s in bits:
                mon = tuple(sorted((((s >> m) & 1), *e) for m,e in enumerate(sites)))
                rect[mon] += (-1)**pop(s)
    exigir(dict(gram2) == dict(rect), "trace and rectangle polynomials differ")
    return len(bits)


def prefactor():
    # Homogeneous model with two single-square lines per edge. t=1/k.
    # Rational coefficients of degrees 1 and 2 in log(1-u*t).
    def loguno(u, j):
        return -F(u**j, j) if j > 0 else F(0)
    def logr(j):
        return loguno(2,j)-loguno(4,j)
    def constante(mult, serie):
        return sum(coef*serie(-pot) for pot, coef in mult.items())
    local = constante({-2:1}, lambda j: loguno(4,j)-loguno(2,j)-2*loguno(1,j))
    filas = constante({-1:2, 0:-1}, logr)
    diagonal = (constante({-2:2}, lambda j: loguno(1,j)) +
                constante({-2:1,-1:-2,0:1}, logr))
    exigir((local, filas, diagonal) == (-5,4,1), "individual prefactor coefficients")
    exigir(local+filas+diagonal == 0, "sum of prefactor contributions")
    # Also check the determinant and all its finite powers.
    for k in (5,6,8):
        p = F(1,k)
        q = 1-p
        tau = lambda d: p*q/(1-d*p)
        b = lambda d: (1-d*p)/q**d
        rank = 2*k-1
        U = q**(k*k+rank)*(q+2*tau(4))**(k*k-rank)
        exigir((b(4)/b(2))**(k*k)*(tau(4)/tau(2))**rank*U == 1,
               f"finite product for k={k}")
    return [int(local), int(filas), int(diagonal)]


def verificar():
    return {"pivotes": list(pivotes()), "motivos": motivos(), "prefactor": prefactor()}
