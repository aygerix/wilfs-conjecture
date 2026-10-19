"""Run on fejer only. Independent exact tests and rational constants for P5g."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb
import json
from pathlib import Path

def packing(B,strict=True):
    n=len(B); assert len(set(B))==n
    pairs=Counter(x+y for x,y in combinations_with_replacement(B,2))
    if strict:assert max(pairs.values())==1
    off=Counter(x+y for x,y in combinations(B,2));assert max(off.values(),default=1)==1
    sf=Counter(sum(t) for t in combinations(B,3))
    repeat=Counter(2*x+y for x in B for y in B)
    trip=sf+repeat
    eps=comb(n+2,3)-len(trip)
    sfex=sum(v-1 for v in sf.values())
    proper=Counter(x+y-z for x,y in combinations(B,2) for z in B if z!=x and z!=y)
    signed=set(proper)|set(B)|{2*x-z for x in B for z in B if x!=z}
    rp=sum(comb(v,2) for v in repeat.values())
    fr=sum(v*repeat[t] for t,v in sf.items())
    fp=sum(comb(v,2) for v in sf.values())
    cp=sum(comb(v,2) for v in proper.values())
    assert rp<=(1 if strict else 2)*comb(n,2) and cp<=9*fp+6*fr+4*rp
    H=n*(comb(n,2)+1); s=max(B)-min(B)+1
    G=max(sf.values(),default=0)
    M=sum(c>=11 for c in sf.values())
    overlap=sum(proper[x] for x in B)
    assert overlap<=n and (not strict or overlap==0)
    assert H-len(signed)<=n*(n-1)+cp+overlap
    if G and strict:
        assert 2*(H-len(signed))<=9*G*sfex+2*(6*G+3)*n*n-6*n
    if G and not strict:
        assert 2*(H-len(signed))<=9*G*sfex+2*(6*G+5)*n*n-8*n
    assert 2*(H-len(signed))<=90*sfex+(130+7*M)*n*n-8*n
    if strict:assert 2*(H-len(signed))<=90*sfex+(126+M)*n*n-6*n
    if M and strict:
        fibres={z:[] for z,c in sf.items() if c>=11}
        for T in combinations_with_replacement(B,3):
            if sum(T) in fibres:fibres[sum(T)].append(set(T))
        for ts in fibres.values():
            assert len(set().union(*ts))==sum(map(len,ts))
            potential=sum(len(A)*len(C) for A,C in combinations(ts,2))
            assert 2*potential<=n*n
    return dict(n=n,s=s,H=H,ex=eps,sfex=sfex,sfmax=G,
                heavy_sf_fibres=M,
                maxfiber=max(trip.values()),repeat_pairs=rp,
                signed=len(signed),holes=3*s-2-len(signed),
                F47=3*s-2-H+47*eps,
                ratio=str(F(H-(3*s-2),eps)) if eps else None)

data=[]
for name in ['planted11','planted16']:
    lines=Path(name+'.log').read_text().splitlines()
    B=list(map(int,lines[-1].split()[1:]))
    result=packing(B)
    g=int(name[7:]); common={sum(B[3*i:3*i+3]) for i in range(g)}
    assert len(common)==1
    result.update(name=name,common=common.pop(),B=B)
    data.append(result)
    print(name,json.dumps(result,sort_keys=True))
small=[0,1,6,15,19,31,58,65,75]
v=packing(small);assert v['ex']==19 and v['H']-(3*v['s']-2)==107
print('LEAD_N9',json.dumps(v,sort_keys=True))
Path('planted_verified.json').write_text(json.dumps(data,indent=2)+'\n')
g=11;R=10**(4*g);V=10**(8*g);E=10**(8*g+2)
weakB=[x for i in range(g) for x in [R+10**(2*i),R+10**(2*i+1),2*R-10**(2*i)-10**(2*i+1)]]
weakB += [V,V+E,V+2*E]
weak=packing(weakB,strict=False)
assert weak['n']==36 and weak['heavy_sf_fibres']==1 and weak['sfmax']==11
Path('weak_heavy_verified.json').write_text(json.dumps(dict(weak,B=weakB),indent=2)+'\n')
print('WEAK_HEAVY',json.dumps(weak,sort_keys=True))

# Complete squarefree B face: b>=max(4a,128), a>=24.
# n=b-2: H(n)-11n^2 >= b^3/2-29b^2/2+53b-52.
assert F(1,2)-F(29,2*128)>F(3,8)
assert F(163,128)**3/6<F(7,20)
assert F(1,3)*(F(5,4)+F(1,128))/128<F(1,256)
assert F(7,20)+F(1,512)+F(1,256)<F(3,8)

# Robust bounded-squarefree-fibre B face: b>=16a, a>=24, n=b-a.
# v_B < F_A/3 < a^3/18; G<=10, weak Sidon.
L=F(1,2)*F(15,16)**3-F(131,2*384)-F(5,2*16**3)
assert L>F(9,40)
assert L-F(7,512)>F(9,40)
assert (F(17,16)+F(3,384))**3/6<F(21,100)
assert F(1,12)*(F(17,16)+F(1,384))/384<F(1,2048)
assert F(21,100)+F(1,8*16**3)+F(1,2048)<F(9,40)
print('B_FACE_RATIONAL_CERTIFICATES',L,'OK')

# Exact polynomial lower bound for BASE and b/l perturbations, N>=480.
# n=49N/20, e=N^3/24, 3s-2=513N^3/200-2.
lead=F(1,2)*F(49,20)**3-F(45,24)-F(513,200)
quad=-F(127,2)*F(49,20)**2
linear=4*F(49,20) # strict P_G has +3n, H includes +n
assert lead>0 and lead*480+quad>0
print('BASE_G10_SLACK',lead,quad,linear,2,'OK')
rare_lead=lead-F(1,4)*F(49,20)**2
assert rare_lead==F(22599,16000) and rare_lead*480+quad>0
print('BASE_RARE_HEAVY_SLACK',rare_lead,quad,linear,2,'OK')
# General matching profile, legal SF multiplicities <=10, absent-pair
# centre multiplicity <=61, r<=N: the same cubic gain dominates all errors.
matching_quad=-F(139,2)*F(49,20)**2-(130+F(9,2)*60)*F(49,20)
assert lead*480+matching_quad>0
print('MATCHING_G10_P61_SLACK',lead,matching_quad,'OK')

# A convenient full-pair B-free uniform certificate for alpha>=1910.
# g(w) >= (1+w^2)/4, exactly, by completing the square.
assert F(44,27)-F(1,4)-F(46,9)**2/19==F(29,6156)
def h(A):return A**3-1908*A*A-2240*A-896
assert h(1909)<0<h(1910)
assert h(1910)==3016904
print('BFREE_G10_THRESHOLD',1910,'shifted_cubic_coefficients',
      [h(1910),3*1910**2-3816*1910-2240,3*1910-1908,1])
def hrare(A):return 19*A**3-68708*A*A-80648*A-32256
assert hrare(3617)<0<hrare(3618)
assert hrare(3618)==153240696
assert 57*3618**2-137416*3618-80648==248873932
assert 57*3618-68708==137518
print('BFREE_RARE_THRESHOLD',3618,'shifted_cubic_coefficients',
      [hrare(3618),248873932,137518,19])
print('ALL_EXACT_CHECKS_PASSED')
