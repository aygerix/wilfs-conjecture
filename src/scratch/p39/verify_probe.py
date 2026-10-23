"""Independent membership reconstruction and rational primal/dual audit of certprobe JSONL.
Uses only Python stdlib; floats are discovery data until every constraint and objective passes exactly.
usage: python3 verify_probe.py probe.jsonl summary.json
"""
import json, sys, gzip
from fractions import Fraction as F
from collections import defaultdict

def open_text(path):
    return gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)

def rat(v):
    return F(str(v)).limit_denominator(1000000)

def audit(D):
    m, e, c, q, rho, r = (D[k] for k in ('m','e','c','q','rho','r'))
    G = D['generators']
    # Independently reconstruct membership, minimal generators, conductor, genus and Apéry.
    N = m * max(G) + m
    member = bytearray(N+1); member[0] = 1
    for x in range(1,N+1):
        member[x] = any(x>=g and member[x-g] for g in G)
    lastgap = max(x for x in range(N+1) if not member[x])
    assert N-lastgap >= m
    ci = lastgap+1; gi = sum(not member[x] for x in range(ci))
    minimal = [x for x in range(1,max(G)+1) if member[x] and not any(member[a] and member[x-a] for a in range(1,x))]
    wi = [next(x for x in range(s,N+1,m) if member[x]) for s in range(m)]
    assert ci==c and gi==D['g'] and minimal==sorted(G) and len(minimal)==e and wi==D['w']
    assert D['W']==e*(c-gi)-c and q==(c+m-1)//m and rho==q*m-c
    assert r==wi.index(max(wi))
    mui=[max(0,(c-w+m-1)//m) for w in wi]; assert mui==D['mu']
    rp=[(w-c)%m for w in wi]
    pairs=[]
    for i in range(1,m):
        for j in range(i,m):
            s=(i+j)%m
            if not s: continue
            J,rem=divmod(wi[i]+wi[j]-wi[s],m); assert not rem and J>=0
            tau=(rp[i]+rp[j]-rp[s]-rho)//m
            lo=int(rp[s]>=m-rho and rp[i]<rho and rp[j]<rho)
            up=int(rp[s]<=m-rho-2 and rp[i]>rho and rp[j]>rho)
            pairs.append([i,j,s,J,tau,lo,up])
    assert pairs==D['pairs']
    gr={g%m for g in G if g!=m}
    height=[0]*m
    for s in sorted(range(1,m),key=lambda x:wi[x]):
        height[s]=max([height[i]+height[j] for i,j,t,J,*_ in pairs if t==s and J==0],default=1)
    assert height==D['height']
    out={'generators':G,'m':m,'e':e,'c':c,'q':q,'rho':rho,'h':max(D['height']),'W':D['W'],'models':{}}
    for name,M in D['models'].items():
        fixed=name in ('UA3','AM3'); exact=name in ('TX','FACE'); full=name in ('AM3','FACE')
        expected=[]
        for p,(i,j,s,J,tau,lo,up) in enumerate(pairs):
            a=defaultdict(int)
            for x,v in ((i,1),(j,1),(s,-1)): a[x]+=v
            a=dict(a)
            if J==0:
                if exact: expected.append((p,0,'=',q+tau,a))
                else: expected.extend(((p,0,'>',q-lo,a),(p,0,'<',q+up,a)))
            elif full: expected.append((p,0,'<',q-1+tau,a))
        if fixed:
            expected.extend((-1,1,'=',mui[g],{g:1}) for g in sorted(gr))
        assert len(expected)==len(M['rows'])
        y=[F(q)]+list(map(rat,M['y'])); rc=list(map(rat,M['rc'])); ub=list(map(rat,M['ub']))
        upper=[F(q-1-(s>r)) if name=='FACE' else F(10)**100 for s in range(1,m)]
        assert all(0<=y[s]<=upper[s-1] for s in range(1,m))
        constant=(e-m)*q+rho; dual=F(constant); load=[F(0)]*m; used=[]
        for (p,kind,sense,b,a),R in zip(expected,M['rows']):
            assert (R['pair'],R['kind'],R['sense'],rat(R['b']),dict(R['a']))==(p,kind,sense,F(b),a)
            value=sum(v*y[x] for x,v in a.items()); pi=rat(R['pi'])
            assert value>=b if sense=='>' else (value<=b if sense=='<' else value==b)
            assert pi>=0 if sense=='>' else (pi<=0 if sense=='<' else True)
            dual+=pi*b
            for x,v in a.items(): load[x]+=pi*v
            if pi:
                used.append({'pair':p,'kind':kind,'sense':sense,'pi':str(pi),'b':b})
        for s in range(1,m):
            assert F(e)-load[s]==rc[s-1]
            if rc[s-1]<0:
                assert name=='FACE' and ub[s-1]==upper[s-1]
                dual+=rc[s-1]*upper[s-1]
        primal=constant+e*sum(y[1:]); assert primal==dual,(name,primal,dual)
        assert abs(float(primal)-M['value'])<1e-6
        assert primal<=D['W']
        non_tight=[]; tight_errors=[]
        for p,(i,j,s,J,tau,lo,up) in enumerate(pairs):
            fakeJ=q+tau-y[i]-y[j]+y[s]
            if J and fakeJ<1:
                non_tight.append({'p':p,'actual_J':J,'fake_J':str(fakeJ),'pair':[i,j,s]})
            if not J and fakeJ:
                tight_errors.append({'p':p,'fake_J':str(fakeJ),'pair':[i,j,s]})
        out['models'][name]={'optimum':str(primal),'dual_nonzero':used,'non_tight_violations':non_tight,'tight_errors':tight_errors,'y':[str(x) for x in y]}
    return out

if __name__=='__main__':
    results=[]
    for line in open_text(sys.argv[1]):
        if not line.strip(): continue
        results.append(audit(json.loads(line)))
    with open(sys.argv[2],'w') as f: json.dump(results,f,indent=2)
    for R in results:
        print('G=%s q=%s h=%s W=%s | '%(R['generators'],R['q'],R['h'],R['W'])+' '.join('%s=%s[nontight:%d,tighterror:%d]'%(name,V['optimum'],len(V['non_tight_violations']),len(V['tight_errors'])) for name,V in R['models'].items()))
    print('EXACTLY CERTIFIED',len(results),'semigroups;',sum(len(R['models']) for R in results),'primal/dual optima')
