"""P11 independent actual-tile checks. Execute only on fejer.

Canonical factors minimize (degree, sorted generator-index word). This is
a translation-invariant monomial order, so its selected factors are a
down-set. All exact inequalities are integer; no LP is used.
"""
import sys,random,heapq,itertools,collections,json,re,math
from fractions import Fraction as F
from math import comb

def apery(m,gg,K=None):
    inf=10**30;w=[inf]*m;w[0]=0;pq=[(0,0)]
    while pq:
        v,r=heapq.heappop(pq)
        if v!=w[r]:continue
        for g in gg:
            j=(r+g)%m;vv=v+g
            if vv<w[j]:w[j]=vv;heapq.heappush(pq,(vv,j))
    if K is not None:
        w=[min(x,K+(i-K)%m) if i else 0 for i,x in enumerate(w)]
    return w if max(w)<inf else None

def primitive(w,m):
    ap=set(w);gg=[];left=[];c=max(w)-m+1
    for x in sorted(ap-{0}):
        if not any(x-g in ap for g in left):
            gg.append(x)
            if x<c:left.append(x)
    return gg

counts=collections.Counter();mins={};failures=[];examples={}
def check(name,slack,meta):
    counts[name]+=1
    mins[name]=min(mins.get(name,slack),slack)
    if slack<0:
        failures.append({'name':name,'slack':slack,**meta})
        json.dump(failures,open('instance_fail.json','w'),indent=2)
        raise AssertionError(failures[-1])

def tilecheck(m,w,tag):
    M=max(w);c=M-m+1
    if not 3*m<c<=4*m:return
    gg=primitive(w,m);d=len(gg)
    if d<2:return
    ell=sum((M-x)//m for x in w);W=(d+1)*ell-c
    meta=dict(m=m,c=c,gens=[m]+gg,tag=tag)
    if W<0:
        json.dump({'W':W,'apery':w,**meta},open('WILF_COUNTER.json','w'),indent=2)
        raise RuntimeError('WILF COUNTEREXAMPLE: stop')
    counts['tiles']+=1;counts['sparse']+=3*(d+1)<m
    h=c-3*m;theta=(3*h+1)//2
    Ac=[i for i,g in enumerate(gg) if g<m+h];aset=set(Ac);a=len(Ac)
    Bc=[i for i,g in enumerate(gg) if m+h<=g<2*m+h];b=len(Bc)
    Cc=[i for i,g in enumerate(gg) if 2*m+h<=g<3*m+h];cc=len(Cc)
    ec=d-a-b-cc
    low={i for i in Ac if 2*(gg[i]-m)<h};A=len(low)
    counts['alpha_ge6']+=A>=6
    counts['numeric_residual']+=(A>=6 and a>=19 and a<5*A*(A+1) and 3*(d+1)<m and m>=211)
    if not A:return
    L=min(gg[i]-m for i in Ac);delta=h-2*L
    Lidx=min(Ac,key=lambda i:gg[i]);high=aset-low
    ap=set(w);factors={0:()};units={g:i for i,g in enumerate(gg)}
    left=[(i,g) for i,g in enumerate(gg) if g<c]
    for x in sorted(ap-{0}):
        if x in units:
            factors[x]=(units[x],);continue
        cand=[tuple(sorted(factors[x-g]+(i,))) for i,g in left if x-g in factors]
        assert cand,(x,meta)
        factors[x]=min(cand,key=lambda z:(len(z),z))
    cells=set(factors.values())
    for z in cells:
        for i in set(z):
            p=list(z);p.remove(i);assert tuple(p) in cells
    pairs={z for z in cells if len(z)==2 and set(z)<=aset}
    cubics={z for z in cells if len(z)==3 and set(z)<=aset}
    quarts={z for z in cells if len(z)==4}
    missing=set(itertools.combinations_with_replacement(Ac,2))-pairs
    r=len(missing);Q=A*(A+1)//2;U=comb(A+2,3)
    rLL=sum(set(z)<=low for z in missing);n0=Q-rLL
    q2=sum(sum(gg[i]-m for i in z)<h for z in pairs)
    u3=sum(sum(gg[i]-m for i in z)<h for z in cubics)
    u0=sum(set(z)<=low and sum(gg[i]-m for i in z)<h for z in cubics)
    u1=u3-u0;c0=sum(set(z)<=low for z in cubics)
    k0=sum(set(z)<=low for z in quarts);k1=len(quarts)-k0
    lstar=collections.Counter()
    for z in pairs:
        if len(set(z)&low)==1 and len(set(z)&high)==1 and sum(gg[i]-m for i in z)<h:
            lstar[next(iter(set(z)&low))]+=1
    ll=sum(lstar.values());S=sum(x*(a+2-x) for x in lstar.values())
    check('q2=n0+l',-abs(q2-n0-ll),meta)
    check('quartics_have_at_most_one_high',sum(sum(i in high for i in z)<=1 for z in quarts)-len(quarts),meta)
    beta=sum(set(z)<=low and sum(gg[i]-m for i in z)<(h+1)//2 for z in pairs)
    betaH=sum(set(z)<=low and sum(gg[i]-m for i in z)<h-L for z in pairs)
    legal=0
    for z in itertools.combinations_with_replacement(Ac,3):
        if all(tuple(z[:j]+z[j+1:]) in pairs for j in range(3)):legal+=1
    ep=legal-len(cubics);D3=(a+2)*len(pairs)-3*len(cubics)
    check('D3_ge_3_legal_defect',D3-3*ep,meta)
    LC=(a+1)*(q2+u3)-4*len(quarts)
    check('LC_nonnegative',LC,meta)
    WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(len(pairs)-q2+u3)-4*(len(cubics)-u3+len(quarts))
    counts['WA_negative']+=WA<0
    if WA<0 and a>=4:check('q_gt_2a_if_WA_negative',len(pairs)-2*a-1,meta)
    Y=set(range(h,min(theta,m)))|set(range(1,max(1,theta-m)))
    H0=h-L;YH=set(range(h,min(h+H0,m)))|set(range(1,max(1,h+H0-m)))
    def allowed(z,val):
        if len(z)==1:return z[0] not in aset
        if len(z)!=2:return False
        cls=[0 if i in aset else 1 if i in Bc else 2 for i in z]
        tau=val-2*m
        return (cls==[0,0] and tau>=h) or (sorted(cls) in ([0,1],[1,1]) and tau>=m+h)
    JA=sum((x%m in Y) and set(z)<=aset and not allowed(z,x) for x,z in factors.items())
    JH=sum((x%m in YH) and set(z)<=aset and not allowed(z,x) for x,z in factors.items())
    R=sum(gg[i]-m<theta-2*L for i in high)
    jL=sum(tuple(sorted((Lidx,j))) in missing for j in high)
    E=min(a-A,ll+jL)
    check('localized_exception_bound',E-sum(gg[i]-m<H0 for i in high),meta)
    CH=A+n0+c0+ll+E+comb(E+2,3)+(n0+A*E)*(a-A)
    check('H0_intruders',CH+len(quarts)-JH,meta)
    if A>=3 and (A+2)*(4*a-5*A-11)>=24:
        P=a-1+LC+2*q2+len(quarts)-2*JA
        lower=D3+a-1-2*A-2*U+(a+3)*n0+S-2*n0*R
        check('COLD_FIXED_payment',P+D3-lower,meta)
    Bf=a-1+q2+u3-2*A-2*beta
    BH=a-1+q2+u3-2*(A+E+ll+betaH)
    if a>=3*A:
        check('Bf_crude',Bf+Q,meta)
        check('BH_crude',BH+Q+2*E+ll,meta)
    # One endpoint of every uncovered missing pair, favoring high degree.
    rem=set(missing);cover=set()
    while rem:
        deg=collections.Counter(i for z in rem for i in set(z));i=max(deg,key=lambda x:(deg[x],-x))
        cover.add(i);rem={z for z in rem if i not in z}
    check('cover_size',r-len(cover),meta)
    X=[gg[i]-m for i in Ac if i not in cover and (i in low or gg[i]-m<theta-2*L)]
    nn=len(X)
    check('joint_size',nn-(A+R-len(cover)),meta)
    sums=collections.Counter(sum(z) for z in itertools.combinations_with_replacement(X,3))
    epsX=sum(v-1 for v in sums.values())
    check('localized_legal_defect',ep-epsX,meta)
    fs=collections.Counter(sum(z) for z in itertools.combinations(X,3));heavy=sum(v>=11 for v in fs.values())
    cap=3*((3*delta+1)//2)-2
    if nn:
        bound=F(nn*(nn*(nn-1)//2+1))-45*epsX-F(126+heavy,2)*nn*nn+3*nn
        check('SF_M_joint',cap-bound,meta)
    D=max(ll+jL,b,(len(cover)+rLL+b+1)//2)
    counts['D_le_alpha']+=D<=A
    if a>=3*A:
        raw=2*E*(1+A*(a-A))+2*comb(E+2,3)+b*(Q+2*E+ll)
        Jbound=3*D*A*a+F(D**3,3)+4*D*D+F(8*D,3)
        check('coarse_delta_error',Jbound-raw,meta)
    if A>=6 and n0*2>=Q and a>=13*(A+D+heavy+22):
        counts['linear_theorem_hypotheses']+=1
        check('linear_theorem_W',W,meta)
    if r==ll==b==0 and A>=1140+9*heavy:
        counts['middle_theorem_hypotheses']+=1
        check('middle_theorem_W',W,meta)
    if A>=1280*(D+heavy+1) and a>=3*A:
        counts['stable_theorem_hypotheses']+=1
        check('stable_theorem_W',W,meta)
    if A>=6 and a>=19 and len(examples)<8:examples[tag]=dict(alpha=A,a=a,b=b,r=r,l=ll,n0=n0,D=D,heavy=heavy,**meta)

seed=int(sys.argv[1]) if len(sys.argv)>1 else 71
trials=int(sys.argv[2]) if len(sys.argv)>2 else 2500
targeted=int(sys.argv[3]) if len(sys.argv)>3 else 0
output_name=sys.argv[4] if len(sys.argv)>4 else 'instances'
rng=random.Random(seed)
# Independent small named failures and interval/per-direction stress.
for gg in ([3,11,13],[4,9,10],[5,9,12],[14,22,23,57,61,62,63]):
    tilecheck(gg[0],apery(gg[0],gg[1:]),'named'+str(gg))
for k in range(2,61):
    m=4*k+1;tilecheck(m,apery(m,range(m+1,m+k+1)),'interval'+str(k))
# Include every best residual Kunz state, read as exact Apéry tables.
for filename in ('kunz85b.log','kunz257b.log','kunz503b.log','kunz320high_nice.log'):
    last=None
    for line in open(filename):
        if line.startswith(' w='):
            ww=list(map(int,line.strip()[2:].split(',')));tilecheck(len(ww),ww,filename)
for it in range(trials):
    m=rng.randint(20,700)
    style=it%4;ng=rng.randint(6,35)
    if style==0:gg=rng.sample(range(m+1,2*m),min(ng,m-1))
    elif style==1:gg=[rng.randint(m+1,m+max(2,m//2)) for _ in range(ng)]
    elif style==2:
        step=rng.randint(2,max(3,m//12));gg=[m+rng.randint(1,max(1,m//step))*step+rng.randrange(3) for _ in range(ng)]
    else:gg=[rng.randint(m+1,4*m) for _ in range(ng)]
    K=rng.randint(3*m+1,4*m) if it%3 else None
    w=apery(m,gg,K)
    if w:tilecheck(m,w,'random'+str(it))
    if (it+1)%250==0:print('PROGRESS',it+1,dict(counts),flush=True)
for it in range(targeted):
    Al=rng.randint(3,8);aa=3*Al+rng.randrange(4)
    m=rng.randint(8000,40000);h=rng.randint(m//4,m//2)
    L=rng.randint(h//4,max(h//4,h//3));lohi=(h-1)//2
    tt=[];pairs=set();used={0}
    def add(t):
        if t in used:return False
        new=[t+x for x in tt]+[2*t]
        if len(set(new))<len(new) or set(new)&pairs or set(new)&used or t in pairs:return False
        tt.append(t);used.add(t);pairs.update(new);return True
    add(L)
    for _ in range(20000):
        if len(tt)>=Al:break
        add(rng.randint(L,lohi))
    for _ in range(20000):
        if len(tt)>=aa:break
        add(rng.randint(h-L,h-1))
    if len(tt)!=aa:continue
    w=apery(m,[m+t for t in tt],3*m+h)
    tilecheck(m,w,'targeted'+str(it))
    if (it+1)%10==0:print('TARGETED_PROGRESS',it+1,dict(counts),flush=True)
out={'status':'PASS','seed':seed,'trials':trials,'targeted_trials':targeted,'counts':dict(counts),
     'minimum_slacks':{k:str(v) for k,v in mins.items()},'examples':examples}
json.dump(out,open(output_name+'.json','w'),indent=2);print(json.dumps(out,sort_keys=True))
