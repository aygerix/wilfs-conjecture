"""Exact numerical-semigroup toolkit (implementation A: direct membership bitsets).

Conventions (see CLAUDE.md):
  c = conductor (least c with [c, oo) in S), F = c - 1 (Frobenius), g = genus,
  L = S cap [0, c), ell = |L| = c - g, m = multiplicity, P = minimal generators,
  e = |P|.  For S = N: c = 0, g = 0, ell = 0, m = 1, P = {1}, e = 1.
  Wilf defect W = e*ell - c (Wilf: W >= 0).
  Depth q = ceil(c/m), rho = q*m - c, shifted intervals I_j = [j*m - rho, (j+1)*m - rho).
"""
from math import gcd
from functools import reduce
from numbers import Integral


class NS:
    """Numerical semigroup stored by its membership on [0, c + m) (enough for everything)."""

    __slots__ = ("c", "m", "mem", "_P", "_ap")

    def __init__(self, c, m, mem):
        # mem: list/bytes of length >= c + m with mem[x] in {0,1}; everything >= c is in S.
        self.c, self.m, self.mem = c, m, mem
        self._P = None
        self._ap = None

    # ---------- constructors ----------
    @staticmethod
    def from_generators(gens):
        gens = sorted(set(int(a) for a in gens if a > 0))
        if not gens or reduce(gcd, gens) != 1:
            raise ValueError("generators must have gcd 1")
        m = gens[0]
        if m == 1:
            return NS(0, 1, bytearray([1]))
        # Apery set w.r.t. m by Dijkstra-free DP: w[i] = least element = i mod m.
        # simple bounded sieve: Frobenius < (m-1)*(max gen) (Schur bound)
        bound = (m - 1) * gens[-1] + m + 1
        mem = bytearray(bound + 1)
        mem[0] = 1
        for x in range(1, bound + 1):
            for a in gens:
                if a > x:
                    break
                if mem[x - a]:
                    mem[x] = 1
                    break
        # conductor
        c = bound + 1
        while c > 0 and mem[c - 1]:
            c -= 1
        return NS(c, m, bytes(mem[: c + m]))

    @staticmethod
    def from_gapset(gaps):
        gaps = list(gaps)
        if any(isinstance(x, bool) or not isinstance(x, Integral) or x <= 0 for x in gaps):
            raise ValueError("gaps must be positive integers")
        gaps = {int(x) for x in gaps}
        if not gaps:
            return NS(0, 1, bytes([1]))
        c = max(gaps) + 1
        m = min(x for x in range(1, c + 2) if x not in gaps)
        mem = bytes(0 if x in gaps else 1 for x in range(c + m))
        s = NS(c, m, mem)
        s.check_closed()
        return s

    def check_closed(self):
        if not self.mem or not self.mem[0]:
            raise ValueError("numerical semigroup must contain zero")
        S = [x for x in range(self.c + self.m) if self.mem[x]]
        for a in S:
            for b in S:
                if a + b >= self.c + self.m:
                    break
                if not self.mem[a + b]:
                    raise ValueError(f"not closed: {a}+{b}")

    # ---------- basic invariants ----------
    def __contains__(self, x):
        return x >= 0 and (x >= self.c or self.mem[x] == 1)

    @property
    def F(self):
        return self.c - 1

    @property
    def gaps(self):
        return [x for x in range(self.c) if not self.mem[x]]

    @property
    def g(self):
        return self.c - self.ell

    @property
    def L(self):
        return [x for x in range(self.c) if self.mem[x]]

    @property
    def ell(self):
        return sum(self.mem[: self.c])

    @property
    def P(self):
        """Minimal generators: positive elements not a sum of two positive elements.
        All lie in [m, c + m)."""
        if self._P is None and self.m == 1:
            self._P = [1]
        if self._P is None:
            m, c = self.m, self.c
            S = [x for x in range(1, c + m) if x in self]
            P = []
            for x in S:
                dec = False
                for a in S:
                    if 2 * a > x:
                        break
                    if (x - a) in self:
                        dec = True
                        break
                if not dec:
                    P.append(x)
            self._P = P
        return self._P

    @property
    def e(self):
        return len(self.P)

    @property
    def W(self):
        return self.e * self.ell - self.c

    @property
    def q(self):
        return -(-self.c // self.m)

    @property
    def rho(self):
        return self.q * self.m - self.c

    def apery(self):
        """Ap(S, m) as a list indexed by residue: ap[i] = least element of S that is = i mod m."""
        if self._ap is None:
            m = self.m
            ap = [None] * m
            x = 0
            found = 0
            while found < m:
                if x in self and ap[x % m] is None:
                    ap[x % m] = x
                    found += 1
                x += 1
            self._ap = ap
        return self._ap

    def kunz(self):
        m = self.m
        return [(w - i) // m for i, w in enumerate(self.apery())][1:]

    def level(self, x):
        """shifted level: I_j = [j m - rho, (j+1) m - rho)."""
        return (x + self.rho) // self.m

    def PF(self):
        """pseudo-Frobenius numbers."""
        P = self.P
        return [h for h in self.gaps if all((h + p) in self for p in P)]

    def t(self):
        return len(self.PF())

    def W0(self):
        """Eliahou's W_0 = |P cap L| * |L| - q |D_q| + rho, D_q = decomposables in [c, c+m)."""
        c, m = self.c, self.m
        Pset = set(self.P)
        PL = sum(1 for p in Pset if p < c)
        Dq = sum(1 for x in range(c, c + m) if x not in Pset)
        return PL * self.ell - self.q * Dq + self.rho

    def summary(self):
        return dict(m=self.m, e=self.e, c=self.c, g=self.g, ell=self.ell, q=self.q,
                    rho=self.rho, W=self.W, P=self.P)

    def key(self):
        return tuple(self.gaps)

    def __repr__(self):
        return f"NS(P={self.P}, c={self.c}, g={self.g})"


def children(s):
    """Children of s in the semigroup tree: s minus a minimal generator x > F(s)."""
    out = []
    for x in s.P:
        if x > s.F:
            c = x + 1
            m = next(y for y in range(1, c + s.m + 2) if (y in s and y != x))
            mem = bytes(1 if (y in s and y != x) else 0 for y in range(c + m))
            out.append(NS(c, m, mem))
    return out


def all_by_genus(G):
    """yield (g, NS) for all numerical semigroups of genus <= G (tree traversal, by levels)."""
    level = [NS(0, 1, bytes([1]))]
    for g in range(G + 1):
        for s in level:
            yield g, s
        if g == G:
            break
        nxt = []
        for s in level:
            nxt.extend(children(s))
        level = nxt
