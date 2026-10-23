"""Independent membership reconstruction and rational primal/dual audit of certprobe JSONL.
Uses only Python stdlib; floats are discovery data until every constraint and objective passes exactly.
usage: python3 verify_probe.py probe.jsonl summary.json
"""
import json, sys, gzip
from math import gcd
from fractions import Fraction as F
from collections import defaultdict

def open_text(path):
    return gzip.open(path,'rt') if str(path).endswith('.gz') else open(path)

def rat(v):
    return F(str(v)).limit_denominator(1000000)

def unique_apery_factorizations(D):
    counts=[0]*(max(D['w'])+1);counts[0]=1
    for g in D['generators']:
        if g==D['m']:continue
        for v in range(g,len(counts)):counts[v]+=counts[v-g]
    return all(counts[w]==1 for w in D['w'])

def factor_basis(D):
    m,e,r=D['m'],D['e'],D['r'];d=e-1
    gr=sorted(g%m for g in D['generators'] if g!=m)
    z={0:(0,)*d}
    for s in sorted(range(1,m),key=lambda s:D['w'][s]):
        candidates=[]
        for j,g in enumerate(gr):
            t=(s-g)%m
            if D['w'][t]+D['w'][g]==D['w'][s]:
                v=list(z[t]);v[j]+=1;candidates.append(tuple(v))
        assert candidates
        z[s]=min(candidates)  # lex-least factorization, a monomial order
    return gr,z

def support_geometry(D):
    """Independent column enumeration for the proved SUPP-WILF filter."""
    m,e,r=D['m'],D['e'],D['r'];gr,z=factor_basis(D);d=e-1
    inv={v:s for s,v in z.items()};assert len(inv)==m
    gamma=[0]*m;nonmax=set();inversions=0
    for j in range(d):
        columns=defaultdict(list)
        for v in inv:columns[v[:j]+v[j+1:]].append(v)
        for col in columns.values():
            top=max(col,key=lambda v:v[j]);assert sorted(v[j] for v in col)==list(range(len(col)))
            gamma[inv[top]]+=len(col)
            for v in col:
                u=list(v);u[j]+=1
                if tuple(u) in inv:nonmax.add(inv[v])
                if v!=top and (inv[v]+D['rho'])%m>(inv[top]+D['rho'])%m:inversions+=1
    support=sum(max(0,sum(a>0 for a in v)-1) for v in inv)
    edges=sum(sum(a>0 for a in v) for v in inv)
    assert support==edges-m+1  # connected Hasse graph cycle rank
    kappa=sum(sum((v[j]*gr[j])%m for j in range(d))//m for v in inv)
    credit=sum(gamma[s]*D['mu'][s] for s in range(m))
    dep=sum(gamma[s] for s in nonmax)
    R=inversions-kappa;C=(e-2)*m*(m-1)//2
    assert sum(gamma)==d*m
    assert sum(gamma[s]*((r-s)%m) for s in range(m))-C==m*R
    assert D['W']==R+credit
    assert kappa<=support and D['W']>=dep-kappa+inversions>=dep-support
    return {'m':m,'e':e,'c':D['c'],'g':D['g'],'W':D['W'],
            'canonical_height':max(map(sum,inv)), 'Dep':dep,'support_sum':support,
            'kappa':kappa,'gamma_mu':credit,'low_maximal':sum(s not in nonmax and D['mu'][s]>0 for s in range(m)),
            'G':D['generators'],'gamma':gamma,'inversions':inversions,
            'shape_excluded':dep>=support,'residue_excluded':dep>=kappa,
            'phase_support_bound':dep-kappa+inversions,'phase_excluded':dep-kappa+inversions>=0,
            'flat_excluded':max(map(sum,inv))<=2,
            'weighted_budget':credit-support}

def upper_baseline(D):
    m=D['m'];gr={g%m for g in D['generators'] if g!=m};b=[0]*m;b[0]=D['q']
    for s in sorted(range(1,m),key=lambda s:D['w'][s]):
        b[s]=D['mu'][s] if s in gr else max([0]+[b[i]+b[j]-D['q']-up for i,j,t,J,tau,lo,up in D['pairs'] if not J and t==s])
    return b

def primitive_cycle_budget(D,known_zero):
    """Exact funding of unit primitive-row allowances, NOT arbitrary row weights."""
    m=D['m'];gr,z=factor_basis(D);inv={v:s for s,v in z.items()};out=[]
    # alpha+kappa=lo+up; the two oriented allowances together cost at most1.
    fees={(i,j):lo+up for i,j,s,J,tau,lo,up in D['pairs'] if not J}
    for j,g in enumerate(gr):
        p=D['w'][g];h=gcd(m,g);columns=defaultdict(list)
        for v in inv:columns[v[:j]+v[j+1:]].append(v)
        next_base={};length={};exit_gap={};cell_length={}
        for col in columns.values():
            base=min(col,key=lambda v:v[j]);top=max(col,key=lambda v:v[j]);s=inv[top];t=(s+g)%m
            assert base[j]==z[t][j]==0
            next_base[base]=z[t];length[base]=len(col)
            for v in col:cell_length[inv[v]]=len(col)
            gap,rem=divmod(D['w'][s]+p-D['w'][t],m);assert not rem and gap>=0
            exit_gap[base]=gap
        assert set(next_base)==set(next_base.values())
        unseen=set(next_base);column_cycles=0
        while unseen:
            a=min(unseen);v=a;cells=gap=0
            while True:
                assert v in unseen;unseen.remove(v);cells+=length[v];gap+=exit_gap[v];v=next_base[v]
                if v==a:break
            assert cells==m//h and gap==p//h;column_cycles+=1
        assert column_cycles==h
        seen=set();cycles=[]
        for start in range(m):
            if start in seen:continue
            vertices=[];resources=[];fund=charge=free=weighted_fund=weighted_charge=0;s=start
            while s not in seen:
                seen.add(s);vertices.append(s);t=(s+g)%m;J,rem=divmod(D['w'][s]+p-D['w'][t],m)
                assert not rem and J>=0
                if J:
                    fund+=J-1;resources.append(J-1);weighted_fund+=cell_length[s]*(J-1)
                else:
                    fee=fees[min(s,g),max(s,g)] if s else 0
                    assert fee in (0,1);charge+=fee;free+=fee==0;resources.append(-fee)
                    if not(s in known_zero and t in known_zero):weighted_charge+=cell_length[s]*fee
                s=t
            assert s==start and len(vertices)==m//h
            assert fund-charge==(p-m)//h+free>0
            # Cut just after a minimum prefix: all rotated balances stay >=0.
            total=minimum=cut=0
            for k,v in enumerate(resources):
                total+=v
                if total<minimum:minimum=total;cut=k+1
            balance=0
            for v in resources[cut:]+resources[:cut]:balance+=v;assert balance>=0
            assert balance==fund-charge
            cycles.append({'orbit':start,'start':vertices[cut%len(vertices)],'length':len(vertices),
                           'strict_excess':fund,'unit_allowance_cost':charge,'free_tight_edges':free,'surplus':balance,
                           'column_weighted_strict_excess':weighted_fund,'column_weighted_active_allowance':weighted_charge})
        out.append({'primitive':p,'residue':g,'column_cycles':h,'cycles':cycles})
    return out

def axis_transport_network(D,zero_aware=False,known_override=None):
    """Column reflections and a global network of axis-adding decompositions."""
    m=D['m'];gr,z=factor_basis(D);d=len(gr);inv={v:s for s,v in z.items()}
    pair={(i,j):p for p,(i,j,s,J,*_) in enumerate(D['pairs']) if not J}
    reflection=[0]*len(D['pairs']);gamma=[0]*m
    def pair_id(a,b):
        assert a and b
        return pair[min(a,b),max(a,b)]
    for j in range(d):
        columns=defaultdict(list)
        for v in z.values():columns[v[:j]+v[j+1:]].append(v)
        for key in sorted(columns):
            column=columns[key];top=max(column,key=lambda v:v[j]);gamma[inv[top]]+=len(column)
            for v in column:
                axis=tuple(top[j]-v[j] if k==j else 0 for k in range(d))
                if inv[v] and inv[axis]:reflection[pair_id(inv[v],inv[axis])]+=1
    known=set()
    if zero_aware:
        b=upper_baseline(D);known={s for s in range(m) if b[s]==D['mu'][s]}
        while True:
            old=known.copy()
            for i,j,s,J,tau,lo,up in D['pairs']:
                if J:continue
                if tau+lo==0 and s in known:known.update((i,j))
                if up-tau==0 and i in known and j in known:known.add(s)
            if known==old:break
        if known_override is not None:
            assert set(known_override)<=known
            known=set(known_override)
        for p,R in enumerate(reflection):
            if not R:continue
            i,j,s,*_=D['pairs'][p];coeff=defaultdict(int)
            for a,v in ((i,1),(j,1),(s,-1)):
                if a not in known:coeff[a]+=v
            if all(v<=0 for v in coeff.values()):reflection[p]=0
    mixed=[v for v in sorted(inv) if sum(a>0 for a in v)>=2]
    need=sum(inv[v] not in known for v in mixed);source=m;sink=m+1;arcs=[];arc_pairs=[]
    def merge(u,v,p):
        i,j,s,J,tau,lo,up=D['pairs'][p];assert not J
        low,high=(tau+lo,up-tau) if zero_aware else (lo,up)
        if reflection[p]:arcs.append([u,v,reflection[p],-low]);arc_pairs.append(p)
        arcs.append([u,v,need,high]);arc_pairs.append(p)
    for v in mixed:
        support=[j for j in range(d) if v[j]];target=inv[v]
        if len(support)==2:
            a,b=support;va=tuple(v[a] if j==a else 0 for j in range(d));vb=tuple(v[b] if j==b else 0 for j in range(d))
            merge(source,target,pair_id(inv[va],inv[vb]))
        else:
            for j in support:
                parent=tuple(0 if k==j else v[k] for k in range(d));axis=tuple(v[j] if k==j else 0 for k in range(d))
                merge(inv[parent],target,pair_id(inv[parent],inv[axis]))
        if target not in known:arcs.append([target,sink,1,0]);arc_pairs.append(-1)
    constant=sum(a*(D['pairs'][p][4]+D['pairs'][p][5] if zero_aware else D['pairs'][p][5]) for p,a in enumerate(reflection))
    return {'nodes':m+2,'source':source,'sink':sink,'demand':need,'arcs':arcs,
            'arc_pairs':arc_pairs,'reflection':reflection,'gamma':gamma,'constant':constant,'known_zero':sorted(known)}

def audit_integer_flow(N,R):
    assert (R['nodes'],R['arcs'],R['flow'])==(N['nodes'],len(N['arcs']),N['demand'])
    flows=R['flows'];potential=R['potential']
    assert len(flows)==len(N['arcs']) and len(potential)==N['nodes']
    assert all(type(v) is int for v in flows+potential)
    balance=[0]*N['nodes'];cost=0;dual=N['demand']*(potential[N['sink']]-potential[N['source']])
    merges=[0]*len(N['reflection'])
    for (u,v,cap,price),f,p in zip(N['arcs'],flows,N['arc_pairs']):
        assert 0<=f<=cap;balance[u]-=f;balance[v]+=f;cost+=f*price
        reduced=price+potential[u]-potential[v]
        if f<cap:assert reduced>=0
        if f:assert reduced<=0
        dual+=cap*min(0,reduced)
        if p>=0:merges[p]+=f
    expected=[0]*N['nodes'];expected[N['source']]=-N['demand'];expected[N['sink']]=N['demand']
    assert balance==expected and cost==dual==R['cost']
    return merges,cost

def audit_axis_transport(C):
    D=C['seed'];audit(D)  # independent membership/minimal generators/Apéry audit
    zero_aware=C.get('zero_aware',False);N=axis_transport_network(D,zero_aware);R=C['flow'];m,e,r=D['m'],D['e'],D['r']
    full_known=set(N['known_zero'] if zero_aware else axis_transport_network(D,True)['known_zero'])
    primitive_cycles=primitive_cycle_budget(D,full_known)
    merges,cost=audit_integer_flow(N,R)
    net=[a-b for a,b in zip(N['reflection'],merges)];load=[0]*m;unpaid_cost=old_cost=0
    for p,v in enumerate(net):
        if not v:continue
        i,j,s,J,tau,lo,up=D['pairs'][p];assert not J
        load[i]+=v;load[j]+=v;load[s]-=v
        unpaid_cost+=v*(tau+lo) if v>0 else -v*(up-tau)
        old_cost+=v*lo if v>0 else -v*up
    gamma=N['gamma'];known=set(N['known_zero'])
    if zero_aware:
        assert all(load[s]>=e-gamma[s] for s in range(1,m) if s not in known)
        assert unpaid_cost==N['constant']+cost
    else:
        assert load[1:]==[e-gamma[s] for s in range(1,m)]
        assert sum(net)==m-e and old_cost==N['constant']+cost
    correction=(e-2)*m*(m-1)//2;dist_credit=sum(gamma[s]*((r-s)%m) for s in range(m))
    if not zero_aware:assert dist_credit-correction-m*unpaid_cost==m*(D['rho']-old_cost)
    assert (dist_credit-correction)%m==0
    constant=(dist_credit-correction)//m;b=upper_baseline(D)
    lower=[D['mu'][s] if s in known else b[s] for s in range(m)]
    baseline=constant+sum(a*v for a,v in zip(gamma,lower))-unpaid_cost
    actual=constant+sum(a*v for a,v in zip(gamma,D['mu']))-unpaid_cost
    assert actual+unpaid_cost==D['W'] and baseline<=actual
    return {'generators':D['generators'],'zero_aware':zero_aware,'known_zero':len(known),'mixed_cells':N['demand'],'flow_cost':cost,
            'reflection_cost':N['constant'],'allowance_cost':old_cost,'unpaid_cost':unpaid_cost,
            'transport_cost':unpaid_cost if zero_aware else old_cost,
            'baseline_bound':baseline,'actual_bound':actual,'gamma':gamma,
            'net_rows':[[p,v] for p,v in enumerate(net) if v], 'primitive_cycles':primitive_cycles}

def axis_face_model(D,penalty,epsilon=F(0)):
    """Integer matrix for m*Omega using only profile-forced zero anchors."""
    m,e,r=D['m'],D['e'],D['r'];gr,z=factor_basis(D);d=len(gr);M=max(D['w'])
    # Scaling is used only to identify the chamber's structural known-zero set.
    view={**D,'q':F(2*M-r,m),'mu':[F(2*M-r,m)]+[F(2*(M-D['w'][s])-(r-s)%m,m) for s in range(1,m)]}
    N=axis_transport_network(view,True);K=set(N['known_zero']);gamma=N['gamma']
    depth=[0]*m
    for s in sorted(range(1,m),key=lambda s:D['w'][s]):
        depth[s]=0 if s in gr else min(depth[i]+depth[j]+up-tau for i,j,t,J,tau,lo,up in D['pairs'] if not J and t==s)
    variables=[s for s in range(1,m) if s not in K and gamma[s]];ix={s:d+k for k,s in enumerate(variables)};nv=d+len(variables)
    obj=[0]*nv;constant=-(e-2)*m*(m-1)//2-m*penalty;rows=[];tags=[]
    def row(sense,rhs,co,tag):
        co={k:v for k,v in co.items() if v}
        if co:rows.append((sense,rhs,co));tags.append(tag)
        else:assert (rhs==0 if sense=='=' else rhs<=0 if sense=='>' else rhs>=0)
    for pair,(i,j,s,J,tau,lo,up) in enumerate(D['pairs']):
        if i in gr or j in gr:row('>' if J else '=',m if J else 0,{k:z[i][k]+z[j][k]-z[s][k] for k in range(d)},('strict' if J else 'trade',pair))
    for k,g in enumerate(gr):row('>',m+g,{k:1},('primitive',k))
    row('>',5*m+r,{k:z[r][k] for k in range(d)},('depth',r))
    for s in range(1,m):
        dist=(r-s)%m;v=[z[r][k]-z[s][k] for k in range(d)]
        if s!=r:row('>',epsilon.denominator*dist+m*epsilon.numerator,{k:epsilon.denominator*v[k] for k in range(d)},('residue',s))
        if s in K:
            for k in range(d):obj[k]+=gamma[s]*v[k]
        else:
            constant+=gamma[s]*dist
            if s in ix:
                obj[ix[s]]=m*gamma[s];co={k:-v[k] for k in range(d)};co[ix[s]]=m
                row('>',-dist-m*depth[s],co,('baseline',s))
    return {'network':N,'gr':gr,'z':z,'known':K,'gamma':gamma,'depth':depth,'variables':variables,
            'objective':obj,'constant':constant,'rows':rows,'tags':tags,'nv':nv}

def audit_axis_face(C):
    D=C['seed'];audit(D);epsilon=F(C.get('epsilon','0'));assert epsilon>=0
    zero=axis_face_model(D,0,epsilon);merges,cost=audit_integer_flow(zero['network'],C['flow'])
    penalty=zero['network']['constant']+cost;A=axis_face_model(D,penalty,epsilon);R=C['axis_face'];assert R['status']==2
    load_rows=[0]*D['m'];paid=0
    for p,v in enumerate(a-b for a,b in zip(A['network']['reflection'],merges)):
        i,j,s,J,tau,lo,up=D['pairs'][p]
        load_rows[i]+=v;load_rows[j]+=v;load_rows[s]-=v
        paid+=v*(tau+lo) if v>=0 else -v*(up-tau)
    assert paid==penalty and all(load_rows[s]>=D['e']-A['gamma'][s] for s in range(1,D['m']) if s not in A['known'])
    x=list(map(rat,R['x']));rc=list(map(rat,R['rc']));pi=list(map(rat,R['pi']));nv=A['nv'];assert len(x)==len(rc)==nv and len(pi)==len(A['rows']) and min(x)>=0 and min(rc)>=0
    load=[F(0)]*nv;dual=F(A['constant'])
    for (sense,rhs,co),weight in zip(A['rows'],pi):
        value=sum(v*x[k] for k,v in co.items())
        assert value==rhs if sense=='=' else value>=rhs if sense=='>' else value<=rhs
        assert weight>=0 if sense=='>' else weight<=0 if sense=='<' else True
        dual+=weight*rhs
        for k,v in co.items():load[k]+=weight*v
    assert all(load[k]+rc[k]==A['objective'][k] for k in range(nv))
    primal=F(A['constant'])+sum(v*t for v,t in zip(A['objective'],x));assert primal==dual and abs(float(primal)-R['value'])<1e-5
    m,e,r=D['m'],D['e'],D['r'];d=len(A['gr']);p=x[:d];w=[sum(a*b for a,b in zip(A['z'][s],p)) for s in range(m)]
    q=(w[r]-r)/m;mu=[q]+[(w[r]-w[s]-(r-s)%m)/m for s in range(1,m)]
    assert q>=5 and mu[r]==0 and all(mu[s]>=epsilon for s in range(1,m) if s!=r)
    assert all(w[s]>=m+s for s in range(1,m))
    for i,j,s,J,*_ in D['pairs']:
        gap=w[i]+w[j]-w[s];assert gap==0 if not J else gap>=m
    view={**D,'q':q,'mu':mu};N=axis_transport_network(view,True,known_override=A['known']);assert N==A['network']
    baseline=upper_baseline(view);K=A['known'];gamma=A['gamma'];omega=F(sum(gamma[s]*((r-s)%m) for s in range(m))-(e-2)*m*(m-1)//2,m)+sum(gamma[s]*(mu[s] if s in K else baseline[s]) for s in range(m))-penalty
    assert m*omega==primal
    budget=defaultdict(F);theta={s:F(A['gamma'][s]) for s in A['known']};active=[]
    for (sense,rhs,co),(kind,key),weight in zip(A['rows'],A['tags'],pi):
        if kind=='baseline':
            assert 0<=weight<=gamma[key];theta[key]=weight;budget['tree_cost']+=m*weight*A['depth'][key]
        elif kind!='trade':budget[kind]+=weight*rhs
        if weight:active.append([kind,key,str(weight)])
    budget['residue']+=sum((gamma[s]-theta.get(s,0))*((r-s)%m) for s in range(1,m) if s not in K)
    budget['correction']=F((e-2)*m*(m-1),2);budget['transport_cost']=m*penalty
    assert budget['strict']+budget['primitive']+budget['depth']+budget['residue']-budget['tree_cost']-budget['correction']-budget['transport_cost']==primal
    integral=all(p[k].denominator==1 and (p[k]-g)%m==0 for k,g in enumerate(A['gr']))
    witness=None
    if integral:
        wi=list(map(int,w));ci=wi[r]-m+1;gi=sum((wi[s]-s)//m for s in range(m));pairs=[]
        for i,j,s,J,tau,lo,up in D['pairs']:pairs.append([i,j,s,(wi[i]+wi[j]-wi[s])//m,tau,lo,up])
        actual_seed={**D,'generators':sorted([m]+list(map(int,p))),'w':wi,'mu':list(map(int,mu)),
                     'c':ci,'g':gi,'W':e*(ci-gi)-ci,'q':int(q),'pairs':pairs,'models':{}}
        audit(actual_seed)
        witness={k:actual_seed[k] for k in ('generators','c','g','W')}
    return {'generators':D['generators'],'epsilon':str(epsilon),'minimum':str(omega),'primitive_values':list(map(str,p)),
            'q':str(q),'transport_cost':penalty,'known_zero':len(K),'genuine_congruences':integral,
            'actual_objective_at_point':str(F(m-r-1)+(e-m)*q+e*sum(mu[1:])),
            'finite_budget':{k:str(F(v,m)) for k,v in budget.items()},'active_dual_rows':active,
            'partially_used_baselines':sum(0<v<gamma[s] for s,v in theta.items() if s not in K),'genuine_witness':witness}

def interior_sources(D):
    """Residue injection from interior column bases to distinct boundary cells."""
    m=D['m'];gr,z=factor_basis(D);d=len(gr);cells=set(z.values())
    interior={v for v in cells if all(tuple(a+int(k==j) for k,a in enumerate(v)) in cells for j in range(d))}
    weights=[0]*m;images=set();matches=[];budget=0
    pairs={(i,j,s):(u-tau) for i,j,s,J,tau,l,u in D['pairs'] if not J}
    for v in sorted(interior):
        s=sum(a*g for a,g in zip(v,gr))%m
        for j,g in enumerate(gr):
            if v[j]:continue
            parent=(s-g)%m
            assert z[parent] not in interior and parent not in images
            images.add(parent);weights[s]+=1;weights[parent]-=1
            gap=D['w'][parent]+D['w'][g]-D['w'][s]
            J,rem=divmod(gap,m);assert not rem and J>=0
            kappa=0 if J else pairs[min(parent,g),max(parent,g),s]
            budget+=J-1 if J else kappa
            matches.append([parent,g,s,J,kappa])
    assert len(images)+len(interior)<=m
    weights[0]=0  # unpaid residue0 is fixed to zero
    return interior,weights,budget,matches

def primitive_projection(D,x,value,full_certificate):
    """Audit primitive trades, the column objective, and residue/cap distances.

    x is the one-based (actual a,q,certificate y) vector. Its actual entries
    may be rational: this calculation does not assert they are a semigroup.
    """
    m,e,r=D['m'],D['e'],D['r'];d=e-1;gr,z=factor_basis(D)
    cells=set(z.values());assert len(cells)==m
    for v in cells:
        for j in range(d):
            if v[j]:
                u=list(v);u[j]-=1;assert tuple(u) in cells
    p=[m*(x[m]-x[g]-int(g>r))+g for g in gr]
    assert all(v>=m+g for v,g in zip(p,gr))
    w=[sum(a*b for a,b in zip(z[s],p)) for s in range(m)]
    unpaid=[F(0)]+[x[s]-x[m+s] for s in range(1,m)]
    for s in range(1,m):
        assert w[s]==m*(x[m]-x[s]-int(s>r))+s
        dist=(r-s)%m
        assert w[r]-w[s]==m*x[s]+dist
        assert w[r]-w[s]>=dist+m*unpaid[s]
    for i,j,s,J,tau,lo,up in D['pairs']:
        gap=w[i]+w[j]-w[s]
        assert gap==0 if not J else gap>=m
    # Minimal excluded words of the canonical down-set give affine boundary
    # rows. Verify a rewriting certificate for every primitive translation.
    inverse={v:s for s,v in z.items()};corners={}
    for v in cells:
        for j in range(d):
            b=list(v);b[j]+=1;b=tuple(b)
            if b in cells or b in corners:continue
            if not all(tuple(t-int(k==j) for k,t in enumerate(b)) in cells for j in range(d) if b[j]):continue
            s=sum(t*g for t,g in zip(b,gr))%m
            gap=sum(t*D['w'][g] for t,g in zip(b,gr))-D['w'][s]
            assert gap>=0 and gap%m==0
            newgap=sum(t*v for t,v in zip(b,p))-w[s]
            assert newgap==0 if not gap else newgap>=m
            corners[b]=(s,bool(gap))
    rewrites=0
    for v in cells:
        for j in range(d):
            start=list(v);start[j]+=1;start=tuple(start);word=start
            seedgap=sum(t*D['w'][g] for t,g in zip(start,gr))
            target=sum(t*g for t,g in zip(start,gr))%m
            seedgap-=D['w'][target];strict=0;balance=[0]*d
            while word not in cells:
                b=next(b for b in sorted(corners) if all(t<=u for t,u in zip(b,word)))
                s,is_strict=corners[b];strict+=is_strict;rewrites+=1
                nextword=tuple(u-t+a for u,t,a in zip(word,b,z[s]))
                oldweight=sum(t*D['w'][g] for t,g in zip(word,gr))
                newweight=sum(t*D['w'][g] for t,g in zip(nextword,gr))
                assert (newweight,nextword)<(oldweight,word)
                for k in range(d):balance[k]+=b[k]-z[s][k]
                word=nextword
            assert inverse[word]==target and balance==[t-u for t,u in zip(start,word)]
            assert strict==0 if seedgap==0 else strict>=1
            gap=sum(t*v for t,v in zip(balance,p))
            assert gap==0 if seedgap==0 else gap>=strict*m
    H=[d*m*z[r][j]-e*sum(v[j] for v in cells) for j in range(d)]
    C=F((e-2)*m*(m-1),2);surplus=sum(a*b for a,b in zip(H,p))
    column_surplus=F(0)
    for j in range(d):
        columns=defaultdict(list)
        for v in cells:columns[v[:j]+v[j+1:]].append(v)
        for column in columns.values():
            top=max(column,key=lambda v:v[j])
            deficit=w[r]-sum(a*b for a,b in zip(top,p));assert deficit>=0
            column_surplus+=len(column)*deficit
    assert column_surplus==surplus
    assert (surplus-C-e*m*sum(unpaid))/m==value
    if full_certificate:
        hmin={0:0}
        for s in sorted(range(1,m),key=lambda s:D['w'][s]):
            hmin[s]=1+min(hmin[(s-g)%m] for g in gr if D['w'][(s-g)%m]+D['w'][g]==D['w'][s])
            assert unpaid[s]<=hmin[s]-1
    interior,_,_,matches=interior_sources(D)
    image={parent for parent,_,_,_,_ in matches};L=len(image)
    distance_credit=sum((r-s)%m for s in image)
    headroom=sum(w[r]-w[s] for s in image)
    image_unpaid=sum(unpaid[s] for s in image)
    assert distance_credit>=L*(L-1)//2
    assert headroom>=distance_credit+m*image_unpaid
    assert surplus>=headroom
    gamma={s:sum(v[j]+1 for j in range(d) if tuple(t+int(k==j) for k,t in enumerate(v)) not in cells) for s,v in z.items()}
    assert all(gamma[s]>=1 for s in image)
    weighted_headroom=sum(gamma[s]*(w[r]-w[s]) for s in image)
    weighted_distance=sum(gamma[s]*((r-s)%m) for s in image)
    weighted_unpaid=sum(gamma[s]*unpaid[s] for s in image)
    rank_credit=sum(k*a for k,a in enumerate(sorted((gamma[s] for s in image),reverse=True)))
    assert weighted_distance>=rank_credit
    assert surplus>=weighted_headroom>=weighted_distance+m*weighted_unpaid
    return {'primitive_residues':gr,'objective_coefficients':H,'correction':str(C),
            'column_surplus':str(surplus),'unpaid_sum':str(sum(unpaid)),
            'actual_objective_at_joint_point':str((surplus-C)/m),
            'affine_boundary_rows':len(corners),'strict_boundary_rows':sum(t for _,t in corners.values()),
            'primitive_translation_rewrite_steps':rewrites,
            'interior_cells':len(interior),'injected_sources':len(matches),
            'zero_gap_injected_sources':sum(J==0 for _,_,_,J,_ in matches),
            'injected_distance_credit':distance_credit,'uniform_injected_credit':L*(L-1)//2,
            'injected_headroom':str(headroom),'injected_unpaid_mass':str(image_unpaid),
            'injected_rank_credit':rank_credit,'injected_weighted_distance':weighted_distance,
            'injected_weighted_unpaid':str(weighted_unpaid),
            'interior_unpaid':[[s,str(unpaid[s])] for s in range(m) if z[s] in interior and unpaid[s]]}

def primitive_dual_budget(D,C,value):
    """Exact affine substitution of a complete a,q,y dual into p,unpaid x.

    Unlike sign restrictions on individual old RHS contributions, this keeps
    all zero-RHS trade loads. No assertion that the resulting budget is
    nonnegative without its verified dual certificate is made.
    """
    m,e,r=D['m'],D['e'],D['r'];d=e-1;gr,z=factor_basis(D);nv=d+m-1
    jac={};constant={}
    for s in range(1,m):
        v=[F(a-b,m) for a,b in zip(z[r],z[s])]+[F(0)]*(m-1)
        jac[s]=v;constant[s]=-F((r-s)%m,m)
        v=v.copy();v[d+s-1]=-1
        jac[m+s]=v;constant[m+s]=constant[s]
    jac[m]=[F(a,m) for a in z[r]]+[F(0)]*(m-1);constant[m]=-F(r,m)
    obj=[F(0)]*nv;objconst=F(m-r-1)
    for a,c in [(m,e-m)]+[(m+s,e) for s in range(1,m)]:
        objconst+=c*constant[a]
        for j,t in enumerate(jac[a]):obj[j]+=c*t
    correction=F((e-2)*(m-1),2);assert objconst==-correction
    H=[(e-1)*m*z[r][j]-e*sum(v[j] for v in z.values()) for j in range(d)]
    assert obj==[F(v,m) for v in H]+[F(-e)]*(m-1)
    costs=defaultdict(F);load=[F(0)]*nv
    for R in C['rows']:
        pi=rat(R['pi']);rhs=rat(R['b'])-sum(v*constant[a] for a,v in R['a'])
        kind=R['kind'];key=R['pair']
        if kind==0:
            assert rhs==(-1 if D['pairs'][key][3] else 0)
            category='strict_boundaries' if rhs else 'zero_rhs_trades'
        elif kind==1:
            i,j,s,J,tau,lo,up=D['pairs'][key]
            assert rhs==(-(tau+lo) if R['sense']=='>' else up-tau)
            category='allowances'
        elif kind==3:
            assert rhs==-F(m+key,m);category='primitive_bounds' if key in gr else 'positive_apery_bounds'
        else:
            assert rhs==0;category='zero_rhs_links'
        costs[category]+=pi*rhs
        if pi:
            for a,v in R['a']:
                if v:
                    for j,t in enumerate(jac[a]):
                        if t:load[j]+=pi*v*t
    for a,rc in enumerate(map(rat,C['rc']),1):
        rhs=(5 if a==m else 0)-constant[a]
        category='depth' if a==m else 'actual_cap' if a<m else 'certificate_cap'
        costs[category]+=rc*rhs
        if rc:
            for j,t in enumerate(jac[a]):
                if t:load[j]+=rc*t
    assert load==obj
    costs['correction']=-correction
    assert sum(costs.values())==value
    assert all(v>=0 for k,v in costs.items() if k not in ('allowances','correction'))
    assert costs['allowances']<=0
    return {k:str(v) for k,v in costs.items()}

def actual_dual_transfer(D,C,x,joint_value):
    """Restrict y=a and tighten certificate rows to actual tight equalities."""
    m,e,r=D['m'],D['e'],D['r'];rc=[F(0)]+list(map(rat,C['rc']))
    load=[F(0)]*(m+1);dual=F(m-r-1);gain=F(0)
    for R in C['rows']:
        pi=rat(R['pi']);rhs=rat(R['b']);coeff=defaultdict(F)
        for a,v in R['a']:coeff[a-m if a>m else a]+=rat(v)
        if R['kind']==1:
            i,j,s,J,tau,lo,up=D['pairs'][R['pair']];assert not J
            gain+=pi*(tau-rhs);rhs=F(tau)
        dual+=pi*rhs
        for a,v in coeff.items():load[a]+=pi*v
    for s in range(1,m):
        load[s]+=rc[s]+rc[m+s];assert load[s]==e
    load[m]+=rc[m];assert load[m]==e-m
    dual+=5*rc[m]
    actual=F(m-r-1)+(e-m)*x[m]+e*sum(x[1:m])
    gap=sum(rc[m+s]*x[s] for s in range(1,m))
    assert gain>=0 and gap>=0 and dual==joint_value+gain and actual-dual==gap
    assert gap==sum(rc[m+s]*(x[s]-x[m+s]) for s in range(1,m))
    return {'lower_bound':str(dual),'value_at_joint_point':str(actual),
            'allowance_gain':str(gain),'primal_dual_gap':str(gap),
            'certified_optimum':str(dual) if not gap else None}

def audit_face(D,out):
    m,e,r=D['m'],D['e'],D['r'];C=D['face'];nv=2*m-1
    assert C['variables']==nv and C['status'] in (2,5)
    actual=C.get('actual_constraints','all_pairs')
    assert actual in ('all_pairs','primitive_edges','oriented_primitive_edges')
    oriented=actual=='oriented_primitive_edges'
    primitive=actual!='all_pairs'
    coverage=C.get('certificate_constraints','full')
    assert coverage in ('full','zero_rhs_only','zero_unpaid_sides')
    expected=[];gr={g%m for g in D['generators'] if g!=m}
    for p,(i,j,s,J,tau,lo,up) in enumerate(D['pairs']):
        coeff=defaultdict(int)
        for a,v in ((i,1),(j,1),(s,-1)):coeff[a]+=v
        A=dict(coeff);A[m]=-1
        sense='<' if J else ('>' if tau>0 else '<') if oriented and tau else '='
        if not primitive or i in gr or j in gr:expected.append((p,0,sense,tau-int(bool(J)),A))
        if not J:
            B={m+a:v for a,v in coeff.items()};B[m]=-1
            if coverage=='full' or coverage=='zero_rhs_only' and not lo or coverage=='zero_unpaid_sides' and tau+lo==0:expected.append((p,1,'>',-lo,B))
            if coverage=='full' or coverage=='zero_rhs_only' and not up or coverage=='zero_unpaid_sides' and up-tau==0:expected.append((p,1,'<',up,B))
    for s in range(1,m):
        if not primitive or s in gr:expected.append((s,3,'<',-1-int(s>r),{s:1,m:-1}))
        expected.append((s,4,'<',0,{m+s:1,s:-1}))
        if s in gr:expected.append((s,2,'=',0,{m+s:1,s:-1}))
    expected.append((r,5,'=',0,{r:1}))
    obj=[F(0)]*(nv+1);obj[m]=e-m
    for s in range(1,m):obj[m+s]=e
    lower=[F(0)]*(nv+1);lower[m]=5
    def feasible(x,ray=False):
        assert len(x)==nv+1 and all(x[a]>= (0 if ray else lower[a]) for a in range(1,nv+1))
        for _,_,sense,rhs,A in expected:
            val=sum(v*x[a] for a,v in A.items());b=0 if ray else rhs
            assert val==b if sense=='=' else val<=b if sense=='<' else val>=b
        # Also audit every omitted actual-side constraint independently. These
        # are implied by primitive paths, not omitted from the claimed domain.
        if primitive and not oriented:
            for s in range(1,m):assert x[s]-x[m]<= (0 if ray else -1-int(s>r))
            for i,j,s,J,tau,lo,up in D['pairs']:
                val=x[i]+x[j]-x[s]-x[m];b=0 if ray else tau-int(bool(J))
                assert val==b if not J else val<=b
        if not ray and not oriented and coverage=='full':
            for i,j,s,J,tau,lo,up in D['pairs']:
                if J:continue
                if i in gr:assert x[m+j]-x[m+s]>=1
                if j in gr:assert x[m+i]-x[m+s]>=1
    seed=[F(0)]+list(map(F,D['mu'][1:]))+[F(D['q'])]+list(map(F,D['mu'][1:]))
    feasible(seed);rho=m-r-1
    assert rho+sum(obj[a]*seed[a] for a in range(1,nv+1))==D['W']
    if C['status']==2:
        x=[F(0)]+list(map(rat,C['x']));feasible(x)
        rc=list(map(rat,C['rc']));load=[F(0)]*(nv+1);dual=F(rho);costs=defaultdict(F)
        assert len(C['rows'])==len(expected) and len(rc)==nv and min(rc)>=0
        for (p,kind,sense,rhs,A),R in zip(expected,C['rows']):
            assert (R['pair'],R['kind'],R['sense'],rat(R['b']),dict(R['a']))==(p,kind,sense,rhs,A)
            pi=rat(R['pi']);assert pi<=0 if sense=='<' else pi>=0 if sense=='>' else True
            dual+=pi*rhs
            category=('actual_nontight' if D['pairs'][p][3] else 'actual_tight') if kind==0 else ('certificate_lower' if sense=='>' else 'certificate_upper') if kind==1 else 'positive_kunz' if kind==3 else 'zero_rhs'
            costs[category]+=pi*rhs
            for a,v in A.items():load[a]+=pi*v
        for a in range(1,nv+1):
            assert obj[a]-load[a]==rc[a-1];dual+=rc[a-1]*lower[a]
        value=F(rho)+sum(obj[a]*x[a] for a in range(1,nv+1))
        assert value==dual and abs(float(value)-C['value'])<1e-6
        costs['conductor_shift']=F(rho);costs['depth_lower_bound']=5*rc[m-1]
        assert sum(costs.values())==value
        result={'status':'optimal','optimum':str(value),'q':str(x[m]),'actual_constraints':actual,'dual_costs':{k:str(v) for k,v in costs.items()}}
        if oriented:assert all(v>=0 for v in costs.values()) and value>=rho
    else:
        import math
        ray=[F(0)]+list(map(rat,C['ray']));feasible(ray,True)
        slope=sum(obj[a]*ray[a] for a in range(1,nv+1));assert slope<0
        scale=math.lcm(*(v.denominator for v in ray))
        step=max(1,int(F(D['W'])/(-slope*scale))+1)
        x=[a+step*scale*b for a,b in zip(seed,ray)];feasible(x)
        value=F(rho)+sum(obj[a]*x[a] for a in range(1,nv+1));assert value<0
        result={'status':'unbounded','slope':str(slope),'integer_ray_scale':scale,'steps':step,'negative_witness_value':str(value)}
    result['certificate_constraints']=coverage
    result['actual_constraints']=actual
    if not oriented:
        result['primitive_projection']=primitive_projection(D,x,value,coverage=='full')
        if C['status']==2:
            result['primitive_dual_budget']=primitive_dual_budget(D,C,value)
            result['actual_dual_transfer']=actual_dual_transfer(D,C,x,value)
    # If the actual point is integral, reconstruct S independently from its
    # resulting positive generators, rather than accepting Kunz inequalities alone.
    if not oriented and all(x[a].denominator==1 for a in range(1,m+1)):
        q=int(x[m]);mu=[q]+[int(x[s]) for s in range(1,m)]
        w=[0]+[m*(q-mu[s]-int(s>r))+s for s in range(1,m)]
        G=sorted([m]+[w[s] for s in gr]);c=q*m-rho;N=m*max(G)+m
        member=bytearray(N+1);member[0]=1
        for v in range(1,N+1):member[v]=any(v>=g and member[v-g] for g in G)
        assert max(v for v in range(N+1) if not member[v])+1==c
        assert [next(v for v in range(s,N+1,m) if member[v]) for s in range(m)]==w
        assert [v for v in G if not any(v>a and member[v-a] for a in G)]==G
        genus=sum(not member[v] for v in range(c));assert sum(mu)==c-genus
        result['witness']={'generators':G,'c':c,'g':genus,'W':e*(c-genus)-c,'y':[str(x[m+s]) for s in range(1,m)],'certificate_value':str(value),'integer_certificate':all(x[m+s].denominator==1 for s in range(1,m))}
    out['face']=result
    return out

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
    if C.get('integer_witness'):
        assert mode=='coordinate' and 'rc' not in C
        x=[F(0)]+list(map(rat,C['x']))
        assert len(x)==m+1 and all(v.denominator==1 for v in x)
        assert all(0<=x[s]<=upper[s-1] for s in range(1,m+1))
        for (p,kind,sense,rhs,coeff),R in zip(expected,C['rows']):
            assert (R['pair'],R['kind'],R['sense'],rat(R['b']),dict(R['a']))==(p,kind,sense,rhs,coeff) and 'pi' not in R
            value=sum(v*x[s] for s,v in coeff.items())
            assert value<=rhs if sense=='<' else value>=rhs
        for i,j,s,J,tau,l,u in D['pairs']:
            if not J:assert -(u-tau)<=x[i]+x[j]-x[s]<=tau+l
        assert -x[target]==rat(C['value'])
        out['cone']={'mode':mode,'target':target,'core':core,'integer_witness':True,'target_value':str(x[target]),'unpaid':[str(v) for v in x[:m]],'capped_objective':str(F(D['W'])-D['e']*sum(x[:m])),
                     'fully_extendible':all(D['w'][target]+g==D['w'][(target+g)%m] for g in D['generators'] if g!=m),
                     'unique_apery_factorizations':unique_apery_factorizations(D)}
        return out
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
        if mode=='coordinate':out['cone']['fully_extendible']=all(D['w'][target]+g==D['w'][(target+g)%m] for g in D['generators'] if g!=m)
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
    if 'face' in D:return audit_face(D,out)
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
    if sys.argv[1]=='--lo-only-check':
        count=0
        for line in open_text(sys.argv[2]):
            C=json.loads(line);D=C['seed'];audit(D)
            N=axis_transport_network(D,False)
            N['arcs']=[[*a[:3],min(a[3],0)] for a in N['arcs']]
            _,cost=audit_integer_flow(N,C['flow']);value=N['constant']+cost
            assert value==C['lo_cost']>D['rho'];count+=1
            print('LO-ONLY OBSTRUCTION',sorted(D['generators']),value,'>',D['rho'])
        print('EXACTLY CERTIFIED',count,'lo-only payment obstructions')
        sys.exit(0)
    if sys.argv[1]=='--support-audit':
        import subprocess
        results=[];obstructions=[]
        for line in open_text(sys.argv[2]):
            if not line.strip():continue
            C=json.loads(line);D=C.get('seed',C)
            audit({**{k:v for k,v in D.items() if k not in ('face','cone')},'models':{}})
            R=support_geometry(D)
            if len(sys.argv)>4:
                V=json.loads(subprocess.check_output([sys.argv[4],'--supp-audit',*map(str,[D['m']]+[g for g in D['generators'] if g!=D['m']])],text=True))
                for key,value in V.items():assert sorted(value)==sorted(R[key]) if key=='G' else value==R[key],(key,value,R[key])
            results.append(R)
            b=upper_baseline(D);A=axis_face_model(D,0);K=A['known']
            for name,y in [('raw',b),('profile_zero',[D['mu'][s] if s in K else b[s] for s in range(D['m'])])]:
                for g in A['gr']:
                    for s in range(1,D['m']):
                        t=(s+g)%D['m']
                        if D['w'][s]+D['w'][g]==D['w'][t] and y[s]<y[t]:
                            obstructions.append({'G':D['generators'],'baseline':name,'parent':s,'primitive':g,'target':t,'values':[y[s],y[t]]})
        report={'records':results,'shape_excluded':sum(R['shape_excluded'] for R in results),
                'baseline_order_obstructions':obstructions}
        with open(sys.argv[3],'w') as out:json.dump(report,out,indent=2)
        print('SUPPORT-AUDIT records=%d shape_excluded=%d baseline_order_obstructions=%d'%(len(results),report['shape_excluded'],len(obstructions)))
        sys.exit(0)
    if sys.argv[1]=='--axis-face':
        results=[audit_axis_face(json.loads(line)) for line in open_text(sys.argv[2]) if line.strip()]
        with open(sys.argv[3],'w') as out:json.dump(results,out,indent=2)
        for R in results:print('AXIS-FACE',R)
        print('EXACTLY CERTIFIED',len(results),'fixed-column continuous regional minima; fractional points are not semigroups')
        sys.exit(0)
    if sys.argv[1]=='--axis-transport':
        results=[audit_axis_transport(json.loads(line)) for line in open_text(sys.argv[2]) if line.strip()]
        with open(sys.argv[3],'w') as f:json.dump(results,f,indent=2)
        for R in results:print('AXIS-TRANSPORT G=%s zero_aware=%s mixed=%d cost=%d baseline=%d actual=%d'%(sorted(R['generators']),R['zero_aware'],R['mixed_cells'],R['transport_cost'],R['baseline_bound'],R['actual_bound']))
        print('EXACTLY CERTIFIED',len(results),'integer transport flows and signed row certificates')
        sys.exit(0)
    results=[]
    for line in open_text(sys.argv[1]):
        if not line.strip(): continue
        results.append(audit(json.loads(line)))
    coordinate_bounds={}
    for R in results:
        C=R.get('cone',{})
        if C.get('mode')=='coordinate' and not C.get('integer_witness'):
            key=(tuple(sorted(R['generators'])),C['target'])
            coordinate_bounds[key]=min(coordinate_bounds.get(key,F(10)**100),-F(C['optimum']))
    for R in results:
        C=R.get('cone',{})
        if not C.get('integer_witness'):continue
        upper=coordinate_bounds.get((tuple(sorted(R['generators'])),C['target']))
        if upper is not None:
            C['real_upper_bound']=str(upper)
            assert F(C['target_value'])<=upper//1
            if F(C['target_value'])==upper//1:C['integer_optimum']=C['target_value']
    with open(sys.argv[2],'w') as f: json.dump(results,f,indent=2)
    for R in results:
        if 'face' in R:
            C=R['face'];print('JOINT-FACE seed=%s status=%s value=%s q=%s witness=%s actual_W=%s'%(R['generators'],C['status'],C.get('optimum',C.get('negative_witness_value')),C.get('q'),C.get('witness',{}).get('generators'),C.get('witness',{}).get('W')))
            if C.get('witness',{}).get('W',0)<0:print('GENUINE WILF FAILURE: independent membership reconstruction passed',C['witness'])
            continue
        if 'cone' in R:
            C=R['cone']
            if C.get('integer_witness'):
                print('INTEGER-REPAIR G=%s target=%d value=%s fully_extendible=%s integer_optimum=%s (from separate real bound %s)'%(R['generators'],C['target'],C['target_value'],C['fully_extendible'],C.get('integer_optimum','not asserted'),C.get('real_upper_bound','absent')))
                continue
            if 'mode' in C:
                print('CORE-LP G=%s mode=%s target=%d core=%d optimum=%s max_unpaid=%s capped_witness=%s'%(R['generators'],C['mode'],C['target'],len(C['core']),C['optimum'],max(map(F,C['unpaid'])),C['capped_objective']))
            else:print('CONE G=%s core=%d epsilon=%s ray_scale=%s max_unpaid=%s capped_upper=%s'%(R['generators'],len(C['core']),C['epsilon'],C['max_ray_scale'],max(map(F,C['scaled_unpaid'])),C['capped_objective_upper']))
            continue
        print('G=%s q=%s h=%s W=%s | '%(R['generators'],R['q'],R['h'],R['W'])+' '.join('%s=%s[nontight:%d,tighterror:%d]'%(name,V['optimum'],len(V['non_tight_violations']),len(V['tight_errors'])) for name,V in R['models'].items()))
    print('EXACTLY CERTIFIED',len(results),'semigroups;',sum(len(R['models'])+int('cone' in R and not R['cone'].get('integer_witness'))+int(R.get('face',{}).get('status')=='optimal') for R in results),'primal/dual optima')
    witnesses=sum(bool(R.get('cone',{}).get('integer_witness')) for R in results)
    if witnesses:print('EXACTLY FEASIBLE',witnesses,'integer repair witnesses; optimality requires a separate bound')
    rays=sum(R.get('face',{}).get('status')=='unbounded' for R in results)
    if rays:print('EXACTLY CERTIFIED',rays,'unbounded rays and negative integer model points; numerical semigroups only when independently reconstructed')
