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

def audit_cone(D,out):
    m,q=D['m'],D['q'];C=D['cone'];mu=D['mu'];gr={g%m for g in D['generators'] if g!=m}
    mode=C.get('mode','cone');target=C.get('target',0);capped=mode!='cone'
    assert mode in ('cone','capped','coordinate') and (0<target<m if mode=='coordinate' else target==0)
    b=[0]*m;b[0]=q
    for s in sorted(range(1,m),key=lambda s:D['w'][s]):
        b[s]=mu[s] if s in gr else max([0]+[b[i]+b[j]-q-u for i,j,t,J,tau,l,u in D['pairs'] if not J and t==s])
    assert b==C['baseline'];delta=[u-v for u,v in zip(mu,b)]
    fixed={s for s in range(m) if not delta[s]}
    while True:
        old=fixed.copy()
        for i,j,s,J,tau,l,u in D['pairs']:
            if J:continue
            if tau+l==0 and s in fixed:fixed.update((i,j))
            if u-tau==0 and i in fixed and j in fixed:fixed.add(s)
        if old==fixed:break
    assert C['rigid']==[int(s in fixed) for s in range(m)]
    core=[s for s in range(1,m) if s not in fixed];assert C['core_size']==len(core)
    # Independent integer envelope for all real capped unpaid vectors. The
    # repeated-parent upper rule is deliberately weakened, never rounded.
    envelope=delta.copy()
    while True:
        old=envelope.copy()
        for i,j,s,J,tau,l,u in D['pairs']:
            if J:continue
            envelope[i]=min(envelope[i],envelope[s]+tau+l)
            envelope[j]=min(envelope[j],envelope[s]+tau+l)
            envelope[s]=min(envelope[s],envelope[i]+envelope[j]+u-tau)
        if old==envelope:break
    assert {s for s,v in enumerate(envelope) if not v}==fixed
    upper=[F(0 if s in fixed else delta[s] if capped else 1) for s in range(1,m)]+[F(bool(core) and not capped)]
    assert list(map(rat,C['ub']))==upper
    expected=[]
    for p,(i,j,s,J,tau,l,u) in enumerate(D['pairs']):
        if J:continue
        coeff=defaultdict(int)
        for k,v in ((i,1),(j,1),(s,-1)):coeff[k]+=v
        if capped or tau+l==0:expected.append((p,0,'<',tau+l if capped else 0,dict(coeff)))
        if capped or u-tau==0:expected.append((p,0,'>',tau-u if capped else 0,dict(coeff)))
    if not capped:expected.extend((-1,2,'>',0,{s:1,m:-1}) for s in core)
    assert len(expected)==len(C['rows'])
    x=[F(0)]+list(map(rat,C['x']));rc=list(map(rat,C['rc']));load=[F(0)]*(m+1)
    assert len(x)==m+1 and len(rc)==m and all(0<=x[s]<=upper[s-1] for s in range(1,m+1))
    used=[];dual=F(0)
    for (p,kind,sense,rhs,coeff),R in zip(expected,C['rows']):
        assert (R['pair'],R['kind'],R['sense'],rat(R['b']),dict(R['a']))==(p,kind,sense,rhs,coeff)
        value=sum(v*x[s] for s,v in coeff.items());pi=rat(R['pi'])
        assert value<=rhs if sense=='<' else value>=rhs
        assert pi<=0 if sense=='<' else pi>=0
        for s,v in coeff.items():load[s]+=pi*v
        dual+=pi*rhs
        if pi:used.append({'pair':p,'kind':kind,'sense':sense,'pi':str(pi)})
    for s in range(1,m+1):
        coefficient=-int(s==m) if not capped else -int(s<m and (mode=='capped' or s==target))
        assert F(coefficient)-load[s]==rc[s-1]
        if rc[s-1]<0:dual+=rc[s-1]*upper[s-1]
    primal=-x[m] if not capped else -sum(x[1:m]) if mode=='capped' else -x[target]
    assert primal==dual and abs(float(dual)-C['value'])<1e-6
    if capped:
        assert all(x[s]<=envelope[s] for s in range(m))
        for i,j,s,J,tau,l,u in D['pairs']:
            if not J:assert -(u-tau)<=x[i]+x[j]-x[s]<=tau+l
        out['cone']={'mode':mode,'target':target,'core':core,'optimum':str(primal),'unpaid':[str(v) for v in x[:m]],'capped_objective':str(F(D['W'])-D['e']*sum(x[:m])),'dual_nonzero':used}
        return out
    for s in core:assert x[s]>=x[m]
    ray=x[:m];finite=[v/2 for v in ray]
    assert all(0<=finite[s]<=delta[s] for s in range(m))
    for i,j,s,J,tau,l,u in D['pairs']:
        if not J:assert -(u-tau)<=finite[i]+finite[j]-finite[s]<=tau+l
    scales=[F(delta[s])/ray[s] for s in range(m) if ray[s]>0]
    for i,j,s,J,tau,l,u in D['pairs']:
        if J:continue
        value=ray[i]+ray[j]-ray[s]
        if value>0:scales.append(F(tau+l)/value)
        elif value<0:scales.append(F(u-tau)/(-value))
    scale=min(scales) if scales else F(0);scaled=[scale*v for v in ray]
    assert all(scaled[s]<=envelope[s] for s in range(m))
    assert all(0<=scaled[s]<=delta[s] for s in range(m))
    for i,j,s,J,tau,l,u in D['pairs']:
        if not J:assert -(u-tau)<=scaled[i]+scaled[j]-scaled[s]<=tau+l
    out['cone']={'epsilon':str(x[m]),'core':core,'ray':[str(v) for v in ray],'finite_unpaid':[str(v) for v in finite],'max_ray_scale':str(scale),'scaled_unpaid':[str(v) for v in scaled],'capped_objective_upper':str(F(D['W'])-D['e']*sum(scaled)),'dual_nonzero':used}
    return out

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
    if 'cone' in D:return audit_cone(D,out)
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
        if 'cone' in R:
            C=R['cone']
            if 'mode' in C:
                print('CORE-LP G=%s mode=%s target=%d core=%d optimum=%s max_unpaid=%s capped_witness=%s'%(R['generators'],C['mode'],C['target'],len(C['core']),C['optimum'],max(map(F,C['unpaid'])),C['capped_objective']))
            else:print('CONE G=%s core=%d epsilon=%s ray_scale=%s max_unpaid=%s capped_upper=%s'%(R['generators'],len(C['core']),C['epsilon'],C['max_ray_scale'],max(map(F,C['scaled_unpaid'])),C['capped_objective_upper']))
            continue
        print('G=%s q=%s h=%s W=%s | '%(R['generators'],R['q'],R['h'],R['W'])+' '.join('%s=%s[nontight:%d,tighterror:%d]'%(name,V['optimum'],len(V['non_tight_violations']),len(V['tight_errors'])) for name,V in R['models'].items()))
    print('EXACTLY CERTIFIED',len(results),'semigroups;',sum(len(R['models'])+int('cone' in R) for R in results),'primal/dual optima')
