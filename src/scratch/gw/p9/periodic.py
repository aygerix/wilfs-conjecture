"""Exact retained counterexamples and the structured periodic stress family."""
import json
from p18 import profile
from modulus import by_modulus


def main():
    rows = []
    for L in range(3, 51):
        m, A = 2 * L - 1, [1, L, L + 1]
        z = by_modulus(m, A)
        assert z['s'] == 9
        bad = [(H, z['R'][H+2]-z['R'][H]) for H in range(z['D']-2)
               if z['R'][H+2]-z['R'][H] < z['s']-1]
        rows.append(dict(L=L, m=m, D=z['D'], bad=bad))
    C, X = {0, 1, 3, 4}, {0, 3}
    XC = {(x-c) % 6 for x in X for c in C}
    assert XC == {0, 2, 3, 5} and len(XC) < len(X)+len(C)-1
    first = profile(14, [3, 7, 10])
    assert first['theta'][5]-first['theta'][2] == 4 < first['s2']-1
    second = profile(6, [2, 3])
    assert 4 * (second['ell']-second['q']) < second['s2']*second['q']*(second['q']-1)
    print(json.dumps(dict(periodic=rows, abstract=dict(n=6,C=sorted(C),X=sorted(X),XC=sorted(XC)),
                         first=first, second=second), indent=2))


if __name__ == '__main__':
    main()
