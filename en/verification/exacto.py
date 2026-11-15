"""Small utilities for exact arithmetic using only the standard library."""
from fractions import Fraction
from itertools import permutations


def exigir(condicion, mensaje):
    if not condicion:
        raise ValueError(mensaje)


def soluciones(n):
    """Column permutations, counting symmetry-equivalent solutions separately."""
    return [p for p in permutations(range(n))
            if len({i-c for i, c in enumerate(p)}) == n
            and len({i+c for i, c in enumerate(p)}) == n]


class Pol:
    """Univariate polynomial with rational coefficients in ascending order of degree."""
    def __init__(self, *a):
        a = list(map(Fraction, a)) or [Fraction(0)]
        while len(a) > 1 and not a[-1]:
            a.pop()
        self.a = tuple(a)

    @staticmethod
    def cast(x):
        return x if isinstance(x, Pol) else Pol(x)

    def __add__(self, b):
        b = self.cast(b)
        return Pol(*(self[i]+b[i] for i in range(max(len(self.a), len(b.a)))))

    __radd__ = __add__

    def __getitem__(self, i):
        return self.a[i] if 0 <= i < len(self.a) else Fraction(0)

    def __neg__(self):
        return Pol(*(-x for x in self.a))

    def __sub__(self, b):
        return self + (-self.cast(b))

    def __rsub__(self, a):
        return self.cast(a) + (-self)

    def __mul__(self, b):
        b = self.cast(b)
        v = [Fraction(0)]*(len(self.a)+len(b.a)-1)
        for i, x in enumerate(self.a):
            for j, y in enumerate(b.a):
                v[i+j] += x*y
        return Pol(*v)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            raise ValueError("negative exponent")
        ans = Pol(1)
        for _ in range(n):
            ans = ans*self
        return ans

    def __eq__(self, b):
        return self.a == self.cast(b).a


class Coc:
    """Quotient of polynomials with equality tested by cross multiplication."""
    def __init__(self, num, den=1):
        self.num, self.den = Pol.cast(num), Pol.cast(den)
        exigir(self.den != 0, "zero polynomial denominator")

    @staticmethod
    def cast(x):
        return x if isinstance(x, Coc) else Coc(x)

    def __add__(self, b):
        b = self.cast(b)
        return Coc(self.num*b.den+b.num*self.den, self.den*b.den)

    __radd__ = __add__

    def __sub__(self, b):
        b = self.cast(b)
        return self+Coc(-b.num, b.den)

    def __mul__(self, b):
        b = self.cast(b)
        return Coc(self.num*b.num, self.den*b.den)

    __rmul__ = __mul__

    def __truediv__(self, b):
        b = self.cast(b)
        return self*Coc(b.den, b.num)

    def __eq__(self, b):
        b = self.cast(b)
        return self.num*b.den == b.num*self.den
