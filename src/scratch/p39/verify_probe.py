"""Independent membership reconstruction and rational primal/dual audit of certprobe JSONL.
Uses only Python stdlib; floats are discovery data until every constraint and objective passes exactly.
usage: python3 verify_probe.py probe.jsonl summary.json
"""
import json, sys, gzip
from math import comb, gcd
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

def partial_support_geometry(D,kept):
    m=D['m'];gr,z=factor_basis(D);d=len(gr);kept=set(kept);inv={z[s]:s for s in kept}
    assert all(0<=s<m for s in kept)
    nonmax=set();gamma={s:0 for s in kept};N=0
    for v,s in inv.items():
        for j in range(d):
            u=list(v)
            if u[j]:u[j]-=1;assert tuple(u) in inv
            u=list(v);u[j]+=1
            if tuple(u) in inv:nonmax.add(s)
    for j in range(d):
        cols=defaultdict(list)
        for v in inv:cols[v[:j]+v[j+1:]].append(v)
        for col in cols.values():
            t=max(col,key=lambda v:v[j]);assert sorted(v[j] for v in col)==list(range(len(col)))
            gamma[inv[t]]+=len(col)
            N+=sum((inv[v]+D['rho'])%m>(inv[t]+D['rho'])%m for v in col)
    dep=sum(gamma[s] for s in nonmax)
    kappa=sum(sum((z[s][j]*gr[j])%m for j in range(d))//m for s in kept)
    return {'size':len(kept),'missing':m-len(kept),'Dep':dep,'N':N,'kappa':kappa,
            'budget':dep+N-kappa+m-len(kept),'nonmax':nonmax}

def completion_graph(D,pool=False,frozen=False):
    m=D['m'];gr,z=factor_basis(D);d=len(gr);inv={v:s for s,v in z.items()};eta=[0]*m
    for j in range(d):
        cols=defaultdict(list)
        for v in inv:cols[v[:j]+v[j+1:]].append(v)
        for col in cols.values():
            previous=0;prefix=[]
            for v in sorted(col,key=lambda v:v[j]):
                s=inv[v];label=(s+D['rho'])%m
                current=sum((u+D['rho'])%m>label for u in prefix)
                eta[s]+=current-previous;previous=current;prefix.append(s)
    kappa=[sum((z[s][j]*gr[j])%m for j in range(d))//m for s in range(m)]
    co=[eta[s]-kappa[s]-sum(z[s])-1 for s in range(m)]
    beta=[1+sum(z[s][j]*gr[j] for j in range(d))//m+
          sum(z[s][j] for j in range(d) if gr[j]<=(s+D['rho'])%m) for s in range(m)]
    assert co==[-v for v in beta] and all(v>=1 for v in beta)
    omega=[d+sum(z[s]) for s in range(m)];benefit=-sum(v for v in co if v<0)
    original_co=co[:];original_omega=omega[:]
    if frozen:
        assert pool
        co=[-(1+sum(z[s][j]*gr[j] for j in range(d))//m) if s else 0 for s in range(m)]
        for s in range(m):
            for j in range(d):
                v=list(z[s]);v[j]+=1
                if tuple(v) in inv and (s+D['rho'])%m+gr[j]<m:omega[s]-=z[s][j]+1
            assert omega[s]>=0
        benefit=-sum(co)
    source=(3 if pool else 2)*m;sink=source+1;arcs=[]
    for s in range(m):
        if co[s]<0:arcs.append([source,s,-co[s]])
        elif co[s]>0:arcs.append([s,sink,co[s]])
        arcs.append([m+s,sink,omega[s]])
    if pool:
        for s in range(m):arcs.append([2*m+s,sink,int(s!=0)])
    for s in range(m):
        for j in range(d):
            v=list(z[s]);v[j]+=1;t=inv.get(tuple(v))
            if t is not None:
                arcs.extend([[t,s,benefit+1],[t,m+s,benefit+1]])
                if pool:
                    arcs.append([t,2*m+s,benefit+1])
                    if not z[s][j]:arcs.append([t,2*m+(s-gr[j])%m,benefit+1])
    return {'m':m,'gr':gr,'z':z,'eta':eta,'co':co,'beta':beta,'omega':omega,
            'original_co':original_co,'original_omega':original_omega,
            'benefit':benefit,'arcs':arcs,'source':source,'sink':sink}

def audit_completion_cut(C):
    D,R=C['seed'],C['cut'];audit(D);G=completion_graph(D);m=D['m']
    assert all(R[k]==D[k] for k in ('m','e','c','rho'))
    assert [a[:3] for a in R['arcs']]==G['arcs']
    assert R['weights']==G['co'] and R['omega']==G['omega'] and R['negative_mass']==G['benefit']
    cut=set(R['cut']);assert G['source'] in cut and G['sink'] not in cut and all(0<=v<2*m+2 for v in cut)
    balance=[0]*(2*m+2);capacity=0
    for u,v,cap,f in R['arcs']:
        assert all(type(a) is int for a in (u,v,cap,f)) and 0<=f<=cap
        balance[u]-=f;balance[v]+=f
        if u in cut and v not in cut:capacity+=cap
    value=R['cut_capacity'];expected=[0]*(2*m+2);expected[G['source']]=-value;expected[G['sink']]=value
    assert balance==expected and capacity==value
    kept={s for s in range(m) if s in cut};assert kept==set(R['kept']) and R['size']==len(kept)
    P=partial_support_geometry(D,kept)
    assert {s for s in range(m) if m+s in cut}==P['nonmax']
    assert R['budget']==P['budget']==m+value-G['benefit']
    assert sum(G['eta'][s] for s in kept)==P['N']
    assert P['budget']==m+sum(G['co'][s] for s in kept)+sum(G['omega'][s] for s in P['nonmax'])
    # On tiny tiles independently enumerate every mask and its actual columns.
    enumerated=None
    if m<=13:
        lookup={v:s for s,v in G['z'].items()};parents=[0]*m
        for s,v in G['z'].items():
            for j in range(len(G['gr'])):
                if v[j]:
                    u=list(v);u[j]-=1;parents[s]|=1<<lookup[tuple(u)]
        best=m;enumerated=0
        for mask in range(1<<m):
            if any(mask>>s&1 and mask&parents[s]!=parents[s] for s in range(m)):continue
            candidate=partial_support_geometry(D,[s for s in range(m) if mask>>s&1]);enumerated+=1;best=min(best,candidate['budget'])
        assert best==P['budget']
    return {**{k:v for k,v in P.items() if k!='nonmax'},'G':D['generators'],'kept':sorted(kept),'cut_capacity':value,
            'actual_W':D['W'],'genuine_negative_W':D['W']<0,'completion_failure':P['budget']<0,
            'negative_mass':G['benefit'],'maximum_Hall_deficiency':G['benefit']-value,
            'cut_height':max((sum(G['z'][s]) for s in kept),default=0),
            'witness_one_per_cell_shortfall':max(0,G['benefit']-value-len(kept)),
            'independently_enumerated_ideals':enumerated,'global_optimum_over_downsets':True}

def audit_partial_support(C):
    D,R=C['seed'],C['partial'];audit(D);P=partial_support_geometry(D,R['kept'])
    assert all(R[k]==D[k] for k in ('m','e','c','rho'))
    assert all(R[k]==P[k] for k in ('size','missing','Dep','N','kappa','budget'))
    gr,z=factor_basis(D);cut=R['cut_residue']
    if cut<0:expected=set(range(D['m']))
    elif R['cut_kind']=='principal_upset':expected={s for s in range(D['m']) if not all(a>=b for a,b in zip(z[s],z[cut]))}
    else:assert R['cut_kind']=='value_prefix';expected={s for s in range(D['m']) if D['w'][s]<=D['w'][cut]}
    assert expected==set(R['kept'])
    assert 1<=R['checked']<=2*D['m']
    if R['budget']>=0:assert R['checked']==2*D['m']
    return {**{k:v for k,v in P.items() if k!='nonmax'},'G':D['generators'],'actual_W':D['W'],
            'genuine_negative_W':D['W']<0,'tested_patterns':R['checked']}

def frozen_payment_geometry(D,kept):
    """Count residual resources directly as missing and wrapped components."""
    gr,z=factor_basis(D);m=D['m'];d=len(gr);lookup={v:s for s,v in z.items()};E=set(kept)
    P=partial_support_geometry(D,E)['nonmax'];gamma=[0]*m;wrapped=[0]*m;pool={0};starts=[]
    for s in range(m):
        for j,g in enumerate(gr):
            v=list(z[s]);v[j]+=1;t=lookup.get(tuple(v));capacity=z[s][j]+1
            if t is None:gamma[s]+=capacity
            elif (s+D['rho'])%m+g>=m:wrapped[s]+=capacity
            if s in E and t in E:
                pool.add(s)
                if not z[s][j]:starts.append([s,j,(s-g)%m]);pool.add((s-g)%m)
    K=[sum(z[s][j]*gr[j] for j in range(d))//m for s in range(m)]
    residual=[1+K[s] if s else 0 for s in range(m)]
    nonwrap=[sum(z[s][j] for j in range(d) if gr[j]<=(s+D['rho'])%m) for s in range(m)]
    original=completion_graph(D);frozen=completion_graph(D,True,True)
    assert all(original['beta'][s]==1+K[s]+nonwrap[s] for s in range(m))
    assert all(gamma[s]+wrapped[s]==frozen['omega'][s] for s in range(m))
    assert frozen['co']==[-v for v in residual]
    source=sum(residual[s] for s in E);G=sum(gamma[s] for s in P);W=sum(wrapped[s] for s in P)
    leakage=0
    for s in P:
        for j,g in enumerate(gr):
            v=list(z[s]);v[j]+=1;t=lookup.get(tuple(v))
            if t is not None and t not in E and (s+D['rho'])%m+g<m:leakage+=z[s][j]+1
    original_margin=len(pool)-sum(original['beta'][s] for s in E)+sum(original['omega'][s] for s in P)
    residual_margin=G+W+len(pool)-1-source
    assert residual_margin==(original_margin-leakage if E else 0)
    # In a nonempty down-set, the origin is reserved separately. Negative
    # boundary starts cannot have residue0, by primitive residue uniqueness.
    assert all(r!=0 for _,_,r in starts)
    return {'size':len(E),'nonmaximal':len(P),'negative_starts':len(starts),
            'pool_size':len(pool),'pool':sorted(pool),'raw_carry_sum':sum(K[s] for s in E),
            'residual_nonzero_demand':source,'missing_direction_capacity':G,
            'wrapped_capacity':W,'free_nonzero_pool_capacity':len(pool)-1,
            'residual_budget':residual_margin,'original_pool_budget':original_margin,'nonwrap_leakage':leakage,
            'alias_loss':len(P)+len(starts)-len(pool),
            'required_wrapped_usage':max(0,source-G-(len(pool)-1)),
            'capacity_components':{'missing':gamma,'wrapped':wrapped}}

def joint_defect_geometry(D,kept):
    """E435: cancel only aliases with a proved distinct canonical-exit slot."""
    gr,z=factor_basis(D);m=D['m'];d=len(gr);lookup={v:s for s,v in z.items()};E=set(kept)
    assert len(E)>=2
    P=partial_support_geometry(D,E)['nonmax'];maxima=E-P
    starts={};internal=[];used_slots=set();outside=defaultdict(list)
    for v in sorted(E):
        for j,g in enumerate(gr):
            w=list(z[v]);w[j]+=1
            if not z[v][j] and lookup.get(tuple(w)) in E:
                u=(v-g)%m;starts[v,j]=u
                if u in P:
                    exit_word=list(z[u]);exit_word[j]+=1
                    assert tuple(exit_word) not in lookup
                    slot=(u,j,0);assert slot not in used_slots;used_slots.add(slot)
                    internal.append({'start_base':v,'direction':j,'image':u,'slot':list(slot)})
                else:outside[u].append([v,j])
    selected=[]
    for s in sorted(maxima):
        j=next(j for j in range(d) if z[s][j]);base=list(z[s]);base[j]=0
        tag=(lookup[tuple(base)],j);assert tag in starts;selected.append(tag)
    assert len(set(selected))==len(maxima)
    G=frozen_payment_geometry(D,E);inside=len(internal)
    exterior=sum(len(group)-1 for group in outside.values())
    unused=len(starts)-len(maxima);missing=G['missing_direction_capacity']-inside
    assert unused>=0 and missing>=0
    assert inside+exterior==len(P)+len(starts)-G['pool_size']==G['alias_loss']
    debt=G['raw_carry_sum']+exterior
    resources=unused+missing+G['wrapped_capacity']
    assert resources-debt==G['residual_budget']
    zero_raw_carry_interior=G['missing_direction_capacity']==G['raw_carry_sum']==0
    zero_resource=G['missing_direction_capacity']+G['wrapped_capacity']==0
    if zero_raw_carry_interior:
        assert inside==exterior==0 and resources-debt>=0
    if zero_resource:
        assert G['raw_carry_sum']==inside==exterior==0 and resources-debt==unused
    return {'size':len(E),'nonmaximal':len(P),'maximal':len(maxima),'negative_starts':len(starts),
            'internal_aliases':inside,'exterior_alias_debt':exterior,'raw_carry_debt':G['raw_carry_sum'],
            'unused_column_starts':unused,'remaining_missing_capacity':missing,
            'wrapped_capacity':G['wrapped_capacity'],'joint_debt':debt,'joint_resources':resources,
            'joint_margin':resources-debt,'internal_slot_witnesses':internal,
            'selected_maximal_columns':[list(tag) for tag in selected],
            'outside_groups':{str(u):v for u,v in sorted(outside.items())},
            'zero_raw_carry_interior':zero_raw_carry_interior,'zero_resource':zero_resource,
            'raw_carry_excess_over_wrapped':max(0,G['raw_carry_sum']-G['wrapped_capacity'])}

def audit_quotient_descent(executable):
    """E439/E440: four exact descent controls and one failed parity payer.
    Reuses generic C reconstruction; independent checks use membership only.
    No optimizer, sampler or genus enumeration.
    """
    import subprocess
    cache={}
    def read(generators):
        G=sorted(set(generators));key=tuple(G)
        if key in cache:return cache[key]
        m=min(G);limit=m*max(G)+m;member=bytearray(limit+1);member[0]=1
        for x in range(1,limit+1):member[x]=any(x>=p and member[x-p] for p in G)
        last=max((x for x in range(limit+1) if not member[x]),default=-1)
        assert limit-last>=m
        c=last+1;g=sum(not member[x] for x in range(c))
        minimal=[x for x in range(1,max(G)+1) if member[x] and
                 not any(member[a] and member[x-a] for a in range(1,x))]
        w=[next(x for x in range(s,limit+1,m) if member[x]) for s in range(m)]
        assert c==max(w)-m+1
        D={'m':m,'e':len(minimal),'c':c,'g':g,'W':len(minimal)*(c-g)-c,
           'generators':minimal,'w':w,'q':(c+m-1)//m,'r':w.index(max(w))}
        D['rho']=D['q']*m-c;D['mu']=[max(0,(c-x+m-1)//m) for x in w]
        raw=json.loads(subprocess.check_output([executable,'--residue-audit',*map(str,G)],text=True))
        assert all(raw[k]==D[k] for k in ('m','e','c','g','W')) and sorted(raw['G'])==minimal
        cache[key]=(D,member);return cache[key]
    def summary(D):return {k:D[k] for k in ('m','e','c','g','W','generators')}
    fixtures=[([5,6,8],5),([17,18,21,33],17),([18,21,29,33],29),([5,7],5)]
    descents=[]
    for G,n in fixtures:
        S,sm=read(G);other=[p for p in S['generators'] if p!=n];k=0
        for p in other:k=gcd(k,p)
        assert k>1 and gcd(k,n)==1
        T,tm=read([n]+[p//k for p in other]);e=S['e'];ell=T['c']-T['g']
        assert T['e'] in (e,e-1) and {p//k for p in other}<=set(T['generators'])
        def apery(member):return [next(x for x in range(s,len(member),n) if member[x]) for s in range(n)]
        sa,ta=apery(sm),apery(tm)
        assert all(sa[(k*s)%n]==k*ta[s] for s in range(n))
        assert S['c']==k*T['c']+(k-1)*(n-1)
        assert 2*S['g']==2*k*T['g']+(k-1)*(n-1) and T['g']<S['g']
        assert (k-1)*(e-2)*(n-1)%2==0
        parts=[k*T['W'],k*(e-T['e'])*ell,(k-1)*(e-2)*(n-1)//2]
        assert sum(parts)==S['W'] and min(parts[1:])>=0
        descents.append({'S':summary(S),'pivot':n,'factor':k,'T':summary(T),
                         'W_parts':parts,'apery_modulus':n,'all_apery_entries_checked':n,
                         'pivot_is_multiplicity':n==S['m'],'multiplicity_changes':S['m']!=T['m']})
    parity=[]
    for G,expected_w,expected_t,expected_correction in (([17,18,21,33],65,72,-79),([17,18,21,37],60,48,-36)):
        S,sm=read(G);odds=[p for p in S['generators'] if p%2]
        even=[p//2 for p in S['generators'] if not p%2]
        pairs=[(p+q)//2 for j,p in enumerate(odds) for q in odds[j:]]
        T,tm=read(even+pairs)
        assert all(sm[2*x]==tm[x] for x in range(min(len(tm),(len(sm)+1)//2)))
        a=min(odds);b=(a-1)//2;I=[bool(sm[a+2*i]) for i in range((len(sm)-a+1)//2)]
        ci=max((i for i,inside in enumerate(I) if not inside),default=-1)+1
        gi=sum(not inside for inside in I[:ci]);v=T['g']-gi
        assert a+2*len(I)>=S['c'] and S['g']==T['g']+gi+b
        assert S['c']==max(2*T['c']-1,a+2*ci-1)
        ideal_generators=[(p-a)//2 for p in odds]
        for i,inside in enumerate(I):
            assert inside==any(i>=j and (i-j>=len(tm) or tm[i-j]) for j in ideal_generators)
        lost=[p for p in T['generators'] if 2*p not in S['generators']];r=len(odds);q=len(lost)
        witnesses={str(p):next([u,w] for j,u in enumerate(odds) for w in odds[j:] if u+w==2*p) for p in lost}
        assert S['e']==T['e']+r-q and q<=r*(r+1)//2
        t=S['c']-2*T['c'];ell=T['c']-T['g'];e=S['e']
        parts=[2*(r-q)*ell,e*(v-b),(e-1)*t]
        assert S['W']==2*T['W']+sum(parts) and sum(parts)==expected_correction
        assert 3*e<S['m'] and S['c']>4*S['m'] and S['W']==expected_w and T['W']==expected_t
        cofactors=[]
        for p in G:
            k=0
            for other in G:
                if other!=p:k=gcd(k,other)
            cofactors.append(k)
        if G[-1]==37:assert cofactors==[1,1,1,1]
        parity.append({'S':summary(S),'T':summary(T),'least_odd':a,'b':b,
                 'ideal_conductor':ci,'ideal_genus':gi,'filled_gaps':v,'odd_primitive_count':r,
                 'lost_even_primitive_count':q,'lost_even_witnesses':witnesses,
                 'conductor_difference':t,'correction_parts':parts,'correction':sum(parts),
                 'monotone_transfer_false':True,'genuine_negative_W':False,
                 'ideal_generators':ideal_generators,'leave_one_out_gcds':cofactors})
    base,_=read([15,37,39,40]);B=support_geometry(base)
    raw=json.loads(subprocess.check_output([executable,'--supp-audit',*map(str,base['generators'])],text=True))
    assert all(raw[k]==B[k] for k in raw)
    assert B['Dep']==10 and B['support_sum']==7 and B['phase_support_bound']==12
    return {'common_divisor_descents':descents,
            'parity_obstructions':parity,
            'closed_BASE_discriminator':B}

def exterior_forest_geometry(D,kept,all_aliases=False):
    """E437: explicit partial exchange, not an optimizer or positivity test."""
    J=joint_defect_geometry(D,kept);gr,z=factor_basis(D);m=D['m']
    lookup={v:s for s,v in z.items()};P=partial_support_geometry(D,kept)['nonmax']
    reserved=set() if all_aliases else {tuple(W['slot']) for W in J['internal_slot_witnesses']}
    def plus(v,j):
        a=list(v);a[j]+=1;return tuple(a)
    def root_key(start):
        s,j=start;a=list(z[s]);a[j]-=1
        return D['w'][s]-D['w'][gr[j]],tuple(a)
    edges=[];adj=defaultdict(list)
    for image,group in J['outside_groups'].items():
        w,k=min(group,key=root_key)
        for v,j in sorted(group):
            if [v,j]==[w,k]:continue
            a,b=plus(z[v],k),plus(z[w],j)
            assert j!=k and a!=b and a not in lookup
            assert sum(a[t]*gr[t] for t in range(len(gr)))%m==sum(b[t]*gr[t] for t in range(len(gr)))%m
            eid=len(edges);edges.append({'image':int(image),'start':[v,j],'root':[w,k],
                                         'ends':[list(a),list(b)]})
            adj[a].append((b,eid));adj[b].append((a,eid))
    if all_aliases:
        for W in J['internal_slot_witnesses']:
            v,j,u=W['start_base'],W['direction'],W['image']
            a,b=plus(z[u],j),z[v]
            assert a not in lookup and b in lookup and a!=b
            assert sum(a[t]*gr[t] for t in range(len(gr)))%m==v
            eid=len(edges);edges.append({'internal':True,'start':[v,j],'image':u,'ends':[list(a),list(b)]})
            adj[a].append((b,eid));adj[b].append((a,eid))
    assert len(edges)==J['exterior_alias_debt']+(J['internal_aliases'] if all_aliases else 0)
    slots={}
    for n in adj:
        available=[]
        if n not in lookup:
            for j,nj in enumerate(n):
                if not nj:continue
                parent=list(n);parent[j]-=1;u=lookup.get(tuple(parent))
                if u in P:
                    available.extend((u,j,h) for h in range(nj) if (u,j,h) not in reserved)
        slots[n]=available
        if all_aliases:assert n in lookup or available
    assignments=[];unpaid=[];components=[];seen=set();tree_edges=set()
    for first in sorted(adj):
        if first in seen:continue
        todo=[first];seen.add(first);vertices=[];component_edges=set()
        while todo:
            v=todo.pop();vertices.append(v)
            for w,eid in adj[v]:
                component_edges.add(eid)
                if w not in seen:seen.add(w);todo.append(w)
        zeros=[v for v in vertices if not slots[v]]
        if all_aliases:
            assert len(zeros)<=1
            assert len({sum(v[j]*gr[j] for j in range(len(gr)))%m for v in vertices})==1
        root=min(zeros or vertices);visited={root};todo=[root];paid=0;tree_unpaid=[]
        while todo:
            v=todo.pop()
            for w,eid in sorted(adj[v],key=lambda pair:pair[1]):
                if w in visited:continue
                visited.add(w);todo.append(w);tree_edges.add(eid)
                if slots[w]:
                    assignments.append({'edge':eid,'word':list(w),'slot':list(slots[w][0])});paid+=1
                else:tree_unpaid.append(eid)
        assert len(visited)==len(vertices)
        cycles=sorted(component_edges-tree_edges);unpaid.extend(tree_unpaid+cycles)
        beta=len(component_edges)-len(vertices)+1
        assert len(cycles)==beta and len(tree_unpaid)==max(0,len(zeros)-1)
        components.append({'vertices':len(vertices),'edges':len(component_edges),'zero_capacity_vertices':len(zeros),
                           'cycle_rank':beta,'paid':paid,'unpaid':len(tree_unpaid)+len(cycles)})
    used={tuple(W['slot']) for W in assignments}
    assert len(used)==len(assignments) and not used&reserved
    assert len({W['edge'] for W in assignments})==len(assignments)
    assert {W['edge'] for W in assignments}.isdisjoint(unpaid)
    assert len(assignments)+len(unpaid)==len(edges)
    for W in assignments:
        n=tuple(W['word']);u,j,h=W['slot']
        assert n not in lookup and u in P and plus(z[u],j)==n and 0<=h<=z[u][j]
        assert list(n) in edges[W['edge']]['ends']
    paid=len(assignments);remainder=len(unpaid)
    missing=J['remaining_missing_capacity']+(J['internal_aliases'] if all_aliases else 0)
    assert paid<=missing
    debt=J['raw_carry_debt']+remainder
    resources=J['unused_column_starts']+missing-paid+J['wrapped_capacity']
    assert resources-debt==J['joint_margin']
    return {'G':sorted(D['generators']),'cut_size':len(set(kept)),'all_aliases':all_aliases,
            'relation_edges':len(edges),'graph_vertices':len(adj),'components':components,
            'paid':paid,'unpaid':remainder,'cycle_rank':sum(C['cycle_rank'] for C in components),
            'extra_zero_vertex_debt':sum(max(0,C['zero_capacity_vertices']-1) for C in components),
            'remaining_carry_debt':J['raw_carry_debt'],'remaining_missing_capacity':missing-paid,
            'remaining_total_debt':debt,'remaining_total_resources':resources,'joint_margin':resources-debt,
            'edges':edges,'assignments':assignments,'unpaid_edges':sorted(unpaid)}

def audit_mstd_two_edge_exchange(R):
    """Only the saved two-edge collision: no reconstruction of the large tile."""
    H0=[0,2,3,4,7,11,12,14]
    H=sorted(a+29*b+29**2*c for a in H0 for b in H0 for c in H0)
    T=R['shift'];m=R['m'];assert len(H)==512 and T==max(H)+1==12195 and m==97558
    # P={0} union (T+H). Nonzero H-differences and negatives of T+H
    # cannot meet P, so no internal reservation is present in this pair cut.
    assert m>4*T and R['internal_aliases']==0
    def pair(a,b):return tuple(sorted((H.index(a),H.index(b))))
    def lex_key(p):return tuple(int(j in p)+int(p[0]==p[1]==j) for j in range(len(H)))
    def canonical(total):return min((pair(a,total-a) for a in H if total-a in H),key=lex_key)
    assert canonical(14)==pair(7,7)
    for a,b in ((14,12),(2,0),(14,11),(3,0)):
        assert canonical(a+b)==pair(a,b)
    common=pair(14,0);used=set();witnesses=[]
    for image,a,b in ((2,2,12),(3,3,11)):
        alternative=pair(a,b);slot=(T+a,H.index(b),0)
        assert alternative!=canonical(a+b) and a+b==14
        assert canonical(2*a)==pair(a,a)  # its unit parent is nonmaximal in E
        assert slot not in used;used.add(slot)
        assert ((T+14)-(T+b))%m==((T+a)-T)%m==image
        witnesses.append({'image':image,'common_word':list(common),'alternative_word':list(alternative),'slot':list(slot)})
    return {'checked_edges':2,'paid':2,'distinct_slots':2,'internal_reservations':0,
            'method':'root two-edge tree at shared word; use one slot at each other endpoint',
            'witnesses':witnesses,'full_MSTD_graph_audited':False}

def audit_completion_pool_cut(C):
    D,R=C['seed'],C['cut'];audit(D);frozen=R.get('frozen_nonwrap',False)
    G=completion_graph(D,True,frozen);m=D['m'];n=3*m+2
    assert R['pool_mode'] and all(R[k]==D[k] for k in ('m','e','c','rho'))
    assert [a[:3] for a in R['arcs']]==G['arcs']
    assert R['weights']==G['co'] and R['omega']==G['omega'] and R['negative_mass']==G['benefit']
    cut=set(R['cut']);assert G['source'] in cut and G['sink'] not in cut and all(0<=v<n for v in cut)
    balance=[0]*n;capacity=0;residual=defaultdict(list)
    for u,v,cap,f in R['arcs']:
        assert all(type(a) is int for a in (u,v,cap,f)) and 0<=f<=cap
        balance[u]-=f;balance[v]+=f
        if u in cut and v not in cut:capacity+=cap
        if f<cap:residual[u].append(v)
        if f:residual[v].append(u)
    value=R['cut_capacity'];expected=[0]*n;expected[G['source']]=-value;expected[G['sink']]=value
    assert balance==expected and capacity==value
    reachable={G['source']};queue=[G['source']]
    for u in queue:
        for v in residual[u]:
            if v not in reachable:reachable.add(v);queue.append(v)
    assert reachable==cut
    E={s for s in range(m) if s in cut};assert E==set(R['kept']) and len(E)==R['size']
    P=partial_support_geometry(D,E);z=G['z'];lookup={v:s for s,v in z.items()};pool={0}
    for s in E:
        for j,g in enumerate(G['gr']):
            v=list(z[s]);v[j]+=1
            if lookup.get(tuple(v)) in E:
                pool.add(s)
                if not z[s][j]:pool.add((s-g)%m)
    assert {s for s in range(m) if m+s in cut}==P['nonmax']
    assert {0}|{s for s in range(m) if 2*m+s in cut}==pool
    deficiency=sum(G['beta'][s] for s in E)-sum(G['original_omega'][s] for s in P['nonmax'])
    # E432 value at THIS pool-optimal cut, not the separate E432 minimum.
    assert P['budget']==R['global_completion_budget']==m-deficiency
    leakage=0
    for s in P['nonmax']:
        for j,g in enumerate(G['gr']):
            v=list(z[s]);v[j]+=1;t=lookup.get(tuple(v))
            if t is not None and t not in E and (s+D['rho'])%m+g<m:leakage+=z[s][j]+1
    if frozen:
        assert R['budget']==value-G['benefit']
        direct=sum(G['omega'][s] for s in P['nonmax'])+len(pool)-1+sum(G['co'][s] for s in E)
        assert R['budget']==direct==(len(pool)-deficiency-leakage if E else 0)
    else:assert R['budget']==1+value-G['benefit']==len(pool)-deficiency
    report={'G':D['generators'],'m':m,'e':D['e'],'c':D['c'],'actual_W':D['W'],
            'pool_budget':len(pool)-deficiency,'residual_budget':R['budget'],
            'frozen_nonwrap':frozen,'nonwrap_leakage':leakage,
            'pool_size':len(pool),'deficiency':deficiency,
            'global_completion_budget':P['budget'],'size':len(E),'pool':sorted(pool),
            'kept':sorted(E),'pool_payment_failure':len(pool)-deficiency<0,
            'frozen_allocation_failure':frozen and R['budget']<0,
            'completion_failure':P['budget']<0,'genuine_negative_W':D['W']<0,
            'global_optimum_over_downsets':True}
    if frozen:
        direct=frozen_payment_geometry(D,E);assert direct['residual_budget']==R['budget']
        full=frozen_payment_geometry(D,range(m));full.pop('capacity_components')
        report['whole_tile_geometry']=full
        if sorted(D['generators'])==[40,41,42,43]:
            control=frozen_payment_geometry(D,{0,G['gr'][0]});control.pop('capacity_components')
            assert control['nonwrap_leakage']==control['original_pool_budget']==2 and control['residual_budget']==0
            report['nonempty_leak_control']=control
    return report

def audit_completion_structure(C):
    """Audit E433 on an existing C flow, without a new search or optimization."""
    base=audit_completion_cut(C);D,R=C['seed'],C['cut'];G=completion_graph(D)
    m=D['m'];d=len(G['gr']);z=G['z'];lookup={v:s for s,v in z.items()}
    # Residual reachability gives the inclusion-smallest minimum source-side cut.
    residual=defaultdict(list)
    for u,v,cap,f in R['arcs']:
        if f<cap:residual[u].append(v)
        if f:residual[v].append(u)
    reachable={G['source']};queue=[G['source']]
    for u in queue:
        for v in residual[u]:
            if v not in reachable:reachable.add(v);queue.append(v)
    assert reachable==set(R['cut'])
    E=set(R['kept']);P=partial_support_geometry(D,E);children={s:[] for s in E}
    for s in E:
        for j in range(d):
            v=list(z[s]);v[j]+=1;t=lookup.get(tuple(v))
            if t in E:children[s].append(t)
    maxima=E-P['nonmax'];private=[]
    for s in sorted(maxima):
        parents=[u for u in E if children[u]==[s]]
        cost=sum(G['omega'][u] for u in parents);benefit=G['beta'][s]
        assert benefit>cost,(s,benefit,cost)
        if s:
            assert benefit<=2*sum(z[s])
            if d>=2:assert len(parents)<=1
            if parents:
                K=sum(z[s][j]*G['gr'][j] for j in range(d))//m
                wrapped=sum(z[s][j] for j in range(d) if G['gr'][j]>(s+D['rho'])%m)
                assert K-wrapped>=d-1 and sum(z[s])>=d
        private.append({'residue':s,'word':list(z[s]),'degree':sum(z[s]),'beta':benefit,
                        'private_parents':parents,'private_capacity':cost})
    active=[j for j in range(d) if any(z[s][j] for s in E)]
    interior={s for s in E if all(lookup.get(tuple(a+(i==j) for i,a in enumerate(z[s]))) in E
                                 for j in active)}
    difference={z[s] for s in interior}
    for s in interior:
        for j in active:
            v=list(z[s]);v[j]-=1;difference.add(tuple(v))
    residues={sum(v[j]*G['gr'][j] for j in range(d))%m for v in difference}
    assert len(residues)==len(difference)<=m
    assert len(difference)==len(interior)+sum(z[s][j]==0 for s in interior for j in active)
    # Change phase only as a combinatorial diagnostic. The new phases are not
    # asserted to be conductors of genuine semigroups with this tile.
    deficiencies=[];gamma={s:0 for s in E}
    for s in E:
        for j in range(d):
            v=list(z[s]);v[j]+=1
            if lookup.get(tuple(v)) not in E:gamma[s]+=z[s][j]+1
    assert sum(gamma.values())==d*len(E)
    for rho in range(m):
        phase={**D,'rho':rho};T=partial_support_geometry(phase,E)
        beta=[1+sum(z[s][j]*G['gr'][j] for j in range(d))//m+
              sum(z[s][j] for j in range(d) if G['gr'][j]<=(s+rho)%m) for s in E]
        deficiency=sum(beta)-sum(G['omega'][s] for s in P['nonmax'])
        assert m-deficiency==T['budget']
        deficiencies.append(deficiency)
    for rho in range(m):
        top=(m-1-rho)%m
        assert deficiencies[(rho+1)%m]-deficiencies[rho]==(d-gamma[top] if top in E else 0)
    assert sum(deficiencies)==m*(len(E)-P['Dep'])-sum(E)
    return {'G':D['generators'],'actual_W':D['W'],'size':len(E),
            'conductor_phase':D['rho'],'conductor_deficiency':deficiencies[D['rho']],
            'maximum_phase_deficiency':max(deficiencies),'phase_deficiencies':deficiencies,
            'phase_sum':sum(deficiencies),'Dep':P['Dep'],'residue_sum':sum(E),
            'active_directions':active,'interior_words':[list(z[s]) for s in sorted(interior)],
            'difference_size':len(difference),
            'interior_payment_shortfall':max(0,deficiencies[D['rho']]-len(difference)),
            'cut_cells':[{'residue':s,'word':list(z[s]),'beta':G['beta'][s],
                          'omega':G['omega'][s],'nonmaximal':s in P['nonmax']} for s in sorted(E)],
            'inclusion_smallest_optimal_cut':True,'maximal_cells':private,
            'checked_phases':m,'completion_failure_at_actual_phase':base['completion_failure']}

def membership_stats(G,apery_modulus=None):
    """Membership DP independent of the C shortest-path reconstruction."""
    G=sorted(set(G));m=G[0];assert m>0
    common=0
    for g in G:common=gcd(common,g)
    assert common==1
    n=apery_modulus or m;N=max(m,n)*max(G)+max(m,n)
    member=bytearray(N+1);member[0]=1
    for x in range(1,N+1):member[x]=any(x>=g and member[x-g] for g in G)
    lastgap=max((x for x in range(N+1) if not member[x]),default=-1);c=lastgap+1
    assert N-lastgap>=m and member[n]
    genus=sum(not v for v in member[:c])
    minimal=[g for g in G if not any(member[a] and member[g-a] for a in range(1,g//2+1))]
    w=[next(x for x in range(s,N+1,n) if member[x]) for s in range(n)]
    return {'m':m,'e':len(minimal),'c':c,'g':genus,'W':len(minimal)*(c-genus)-c,'G':minimal,'w':w}

def audit_odd_comparison(C):
    """E441: independent membership plus the mixed Apéry-sum identity."""
    source=membership_stats(C['G']);a=min(p for p in source['G'] if p%2)
    S=membership_stats(source['G'],a);odd=[p for p in S['G'] if p%2]
    H=[p//2 for p in S['G'] if not p%2];A=[(p-a)//2 for p in odd]
    U=membership_stats([a]+H+[x for x in A if x],a)
    pairs=[(p+q)//2 for j,p in enumerate(odd) for q in odd[j:]]
    T=membership_stats(H+pairs,a)
    for expected,reported in ((S,C),(U,C['odd_closure'])):
        assert all(expected[k]==reported[k] for k in ('m','e','c','g','W'))
        assert expected['G']==sorted(reported['G'])
    assert C['least_odd']==a and U['e']<=S['e'] and U['g']<=T['g']<S['g']
    iw=[min(x+T['w'][(s-x)%a] for x in A) for s in range(a)]
    gi=sum(w//a for w in iw);ci=max(iw)-a+1
    K=[];L=[]
    for s in range(a):
        k,rem=divmod(T['w'][s]-U['w'][s],a);assert rem==0 and k>=0
        l,rem=divmod(iw[s]-U['w'][s],a);assert rem==0 and 0<=l<=k<=l+1
        assert S['w'][(2*s)%a]==T['w'][s]+iw[s]
        K.append(k);L.append(l)
    b=(a-1)//2;E=S['e'];ellU=U['c']-U['g']
    assert S['g']==T['g']+gi+b and S['c']==max(2*T['c']-1,a+2*ci-1)
    assert sum(K)==T['g']-U['g'] and sum(L)==gi-U['g']
    parts=[2*U['W'],2*(E-U['e'])*ellU,(E-1)*(S['c']-2*U['c']),-E*(b+sum(K)+sum(L))]
    assert S['W']==sum(parts) and C['margin']==S['W']-U['W']
    cofactors=[]
    for p in S['G']:
        common=0
        for q in S['G']:
            if q!=p:common=gcd(common,q)
        cofactors.append(common)
    return {'S':{k:S[k] for k in ('m','e','c','g','W','G')},
            'U':{k:U[k] for k in ('m','e','c','g','W','G')},
            'T':{k:T[k] for k in ('m','e','c','g','W','G')},
            'least_odd':a,'ideal_conductor':ci,'ideal_genus':gi,'ideal_generators':A,
            'apery_modulus':a,'T_lifts':K,'I_lifts':L,'binary_difference':[k-l for k,l in zip(K,L)],
            'W_parts':parts,'margin':C['margin'],'leave_one_out_gcds':cofactors,
            'genuine_negative_W':min(S['W'],T['W'],U['W'])<0}

def audit_parity_credit(C):
    base=audit_odd_comparison(C);a=base['least_odd'];S=membership_stats(base['S']['G'],a)
    M=max(S['w']);q=(S['c']+a-1)//a;rho=(-S['c'])%a
    D={'m':a,'e':S['e'],'c':S['c'],'g':S['g'],'W':S['W'],'generators':S['G'],
       'w':S['w'],'r':S['w'].index(M),'rho':rho,'mu':[(M-v)//a for v in S['w']]}
    gr,z=factor_basis(D);inv={v:s for s,v in z.items()};d=len(gr);gamma=[0]*a;N=0;nonmax=set();depth=[0]*a;zero=[]
    for j,g in enumerate(gr):
        p=S['w'][g];columns=defaultdict(list)
        for word in inv:columns[word[:j]+word[j+1:]].append(word)
        for column in columns.values():
            top=max(column,key=lambda v:v[j]);assert sorted(v[j] for v in column)==list(range(len(column)))
            gamma[inv[top]]+=len(column)
            N+=sum((inv[v]+rho)%a>(inv[top]+rho)%a for v in column)
        for word,s in inv.items():
            child=list(word);child[j]+=1;t=inv.get(tuple(child))
            if t is None:continue
            assert S['w'][s]+p==S['w'][t]
            drop=D['mu'][s]-D['mu'][t]
            assert drop==p//a+int((S['w'][s]+rho)%a+g>=a)
            nonmax.add(s);depth[s]=max(depth[s],p//a)
            if drop==0:zero.append({'parent_value':S['w'][s],'child_value':S['w'][t],'primitive':p,
                                    'parent_mu':D['mu'][s],'child_mu':D['mu'][t]})
    kappa=sum(sum((word[j]*gr[j])%a for j in range(d))//a for word in inv)
    weighted=sum(gamma[s]*depth[s] for s in range(a));unweighted=sum(gamma[s] for s in nonmax)
    exact=sum(gamma[s]*D['mu'][s] for s in range(a))+N-kappa
    assert exact==S['W'] and all(D['mu'][s]>=depth[s] for s in range(a))
    assert S['W']>=weighted+N-kappa
    even={v for v in S['w'] if v%2==0};odd=set(S['w'])-even
    oddprimitives=sorted(p for p in S['G'] if p%2 and p!=a);degree=len(oddprimitives)
    assigned=set();witness=[];max_credit=0;unique=True
    for v in sorted(odd):
        candidates=[p for p in oddprimitives if v-p in even];p=candidates[0];u=v-p
        max_credit+=max(candidates);unique&=len(candidates)==1
        assert (u,p) not in assigned;assigned.add((u,p));witness.append({'child':v,'parent':u,'primitive':p})
    unmatched={(u,p) for u in even for p in oddprimitives}-assigned
    DE=sum(M-v for v in even);DO=sum(M-v for v in odd)
    primitive_credit=sum(W['primitive'] for W in witness);reserve=sum(M-u for u,p in unmatched)
    assert degree*len(even)>=len(odd)==len(witness)
    assert degree*DE-DO==primitive_credit+reserve>=len(odd)*(a+2)
    correction=(S['e']-2)*(a-1)//2
    without=S['e']*(degree+1)*DO+S['e']*primitive_credit-degree*a*(M+correction)
    assert without+S['e']*reserve==degree*a*S['W']
    max_without=without+S['e']*(max_credit-primitive_credit)
    return {'S':base['S'],'a':a,'even_dimension':len(even),'odd_dimension':len(odd),'odd_source_generator_count':degree,
            'parent_witnesses':witness,'unused_parent_copies':len(unmatched),'primitive_credit':primitive_credit,
            'unused_deficit_reserve':reserve,'typed_deficit':degree*DE-DO,
            'even_deficit':DE,'odd_deficit':DO,'maximum_primitive_credit':max_credit,'unique_parents':unique,
            'reserve_free_numerator':without,'best_reserve_free_numerator':max_without,
            'full_scaled_W':without+S['e']*reserve,
            'zero_drop_steps':zero,'unweighted_depth':unweighted,'weighted_depth':weighted,
            'phase_correction':N-kappa,'naive_unweighted_bound':unweighted+N-kappa,
            'corrected_weighted_bound':weighted+N-kappa,'original_exact_W':exact}

def audit_source_parity(C):
    R=audit_odd_comparison(C);layers=audit_odd_layers(C);a=R['least_odd'];h1=layers['Hilbert_function'][1] if layers['power_layers'] else 0
    S=membership_stats(R['S']['G'],a);T=membership_stats(R['T']['G'],a);A=R['ideal_generators']
    iw=[min(x+T['w'][(s-x)%a] for x in A) for s in range(a)]
    contains_T=lambda x:x>=0 and x>=T['w'][x%a]
    contains_I=lambda x:x>=0 and x>=iw[x%a]
    even={n for n in range(a+R['ideal_conductor']) if contains_T(n) and not contains_I(n-a)}
    odd={n for n in range(T['c']) if contains_I(n) and not contains_T(n)}
    values=set(S['w']);assert {2*n for n in even}|{a+2*n for n in odd}==values
    assert len(odd)==h1 and len(even)==a-h1 and len(values)==a
    typed={2*n:(0,n) for n in even};typed.update({a+2*n:(1,n) for n in odd})
    nonzero_odd_products=[]
    for v,(p,x) in typed.items():
        for w,(q,y) in typed.items():
            parity=(p+q)%2;exponent=x+y+(a if p and q else 0)
            target=even if parity==0 else odd
            result=2*exponent+(a if parity else 0) if exponent in target else None
            assert result==(v+w if v+w in values else None)
            if p and q and result is not None:nonzero_odd_products.append([v,w,result])
    generated={0};others=[p for p in S['G'] if p!=a]
    while True:
        nxt=generated|{v+p for v in generated for p in others if v+p in values}
        if nxt==generated:break
        generated=nxt
    assert generated==values and len(others)==S['e']-1
    oddvalues={a+2*x for x in odd};power={0};powers=[];killed=[]
    for n,layer in enumerate(layers['power_layers'],1):
        power={v+w for v in power for w in oddvalues if v+w in values}
        surviving={n*a+2*x for x in layer if n*a+2*x in values}
        assert power==surviving
        if n<=2:assert len(power)==len(layer)
        if n>=3:assert power<=set(powers[n-3])
        powers.append(sorted(power));killed.append([x for x in layer if n*a+2*x not in values])
    mean=F(sum(values),a);maximum=max(values);correction=(S['e']-2)*(a-1)//2
    assert S['W']==(S['e']-1)*maximum-S['e']*mean-correction
    return {'S':R['S'],'a':a,'even_dimension':len(even),'odd_dimension':len(odd),
            'source_algebra_generator_count':len(others),'value_basis':sorted(values),
            'odd_product_dimensions':[len(V) for V in powers],'odd_product_value_bases':powers,
            'scalar_layer_dimensions':layers['Hilbert_function'][1:],'killed_scalar_layers':killed,
            'nonzero_odd_products':nonzero_odd_products,'mean_value':str(mean),'maximum_value':maximum,
            'finite_correction':correction,'all_basis_products_checked':a*a}

def audit_odd_filtration(C):
    """E448: independent monomial ideal powers, preserving value and parity."""
    from collections import Counter
    from itertools import combinations_with_replacement
    source=audit_source_parity(C);layers=audit_odd_layers(C)
    a=source['a'];S=membership_stats(source['S']['G'],a)
    values=set(S['w']);even={v for v in values if v%2==0};odd=values-even
    V=[even,odd]
    while V[-1]:
        V.append({v+w for v in V[-1] for w in odd if v+w in values})
        assert len(V)<=max(values)+3
    getV=lambda n:V[n] if n<len(V) else set()
    ideal=getV(1)|getV(2);powers=[values]
    while powers[-1]:
        powers.append({v+w for v in powers[-1] for w in ideal if v+w in values})
        assert len(powers)<=max(values)+3
    for n,power in enumerate(powers):
        assert not getV(n)&getV(n+1)
        assert power==getV(n)|getV(n+1)
    b=[len(powers[n])-len(powers[n+1]) for n in range(len(powers)-1)]
    graded=[powers[n]-powers[n+1] for n in range(len(b))]
    assert all(b[n]==len(getV(n))-len(getV(n+2)) for n in range(len(b)))
    assert all(v>=0 for v in b) and sum(b)==a
    coefficient=even-getV(2)
    h=layers['Hilbert_function'][1:]
    geth=lambda n:h[n-1] if n<=len(h) else 0
    assert len(getV(1))==geth(1) and len(getV(2))==geth(2)
    assert b[0]==len(coefficient)==a-geth(1)-geth(2)
    oddprimitives=[p for p in S['G'] if p!=a and p%2]
    evenprimitives=[p for p in S['G'] if p%2==0];q=len(oddprimitives)
    assert ideal=={v+p for v in values for p in oddprimitives if v+p in values}
    generated={0}
    while True:
        nxt=generated|{v+p for v in generated for p in evenprimitives if v+p in coefficient}
        if nxt==generated:break
        generated=nxt
    assert generated==coefficient
    for n,block in enumerate(graded):
        free=Counter(sum(word) for word in combinations_with_replacement(oddprimitives,n))
        assert len(block)<=sum(free.values())*len(coefficient)
        if n:assert len(block)<=(comb(q+n-1,n) if q else 0)*b[0]
        for value in block:
            assert sum(count for shift,count in free.items() if value-shift in coefficient)>=1
    assert len(getV(3))>=geth(1)-q*b[0]
    allodd=not evenprimitives
    if allodd:
        assert coefficient=={0} and b[0]==1 and b[1]==q==S['e']-1
        assert geth(1)+geth(2)==a-1 and len(getV(3))==geth(1)-q
        assert geth(1)-geth(3)<=q
    eta=[geth(n)-len(getV(n)) for n in range(1,max(len(h),len(V)-1)+1)]
    assert all(v>=0 for v in eta) and all(v==0 for v in eta[:2])
    moment=sum(n*v for n,v in enumerate(b));death=2*sum(eta[2:])
    assert moment+death==layers['weighted_lift_mass']
    M=max(values);L=a-S['e']+1;correction=(S['e']-2)*a*(a-1)//2
    homogeneous=(S['e']-1)*a*M-S['e']*sum(values)
    assert homogeneous==a*S['W']+correction and homogeneous*L>=M
    result={'S':source['S'],'a':a,'odd_primitive_count':q,'even_primitive_count':len(evenprimitives),
            'coefficient_value_basis':sorted(coefficient),'associated_graded_Hilbert_function':b,
            'associated_graded_value_bases':[sorted(G) for G in graded],
            'V_dimensions_from_n_zero':[len(v) for v in V],
            'scalar_layer_dimensions':h,'killed_layer_counts':eta,
            'graded_degree_moment':moment,'twice_killed_mass':death,
            'weighted_lift_mass':layers['weighted_lift_mass'],'all_original_primitives_odd':allodd,
            'linear_stability_gap':homogeneous,'linear_stability_L':L,'maximum_value':M}
    if sorted(S['G'])==[a,a+2,3*a+8,3*a+10]:
        assert a>=15 and a%2 and S['m']==a and S['e']==4 and 3*S['e']<a and S['c']>=5*a
        assert all(gcd(*[p for p in S['G'] if p!=removed])==1 for removed in S['G'])
        p=a+2
        assert all(n*p in values for n in (1,2,3)) and 4*p not in values
        assert 4*p-a==3*a+8
        for n in range(4,a):
            assert n in layers['power_layers'][n-1] and n*p not in values
        result['shared_first_death']={'parent':3*p,'primitive':p,'formal_target':4*p,
                                     'scalar_descendants':list(range(4,a)),'capacity_needed':a-4}
    return result

def audit_pointwise_death(C):
    """E451/E454: exact columns; one fixed trade calibration, never a search."""
    R=audit_odd_comparison(C);filtration=audit_odd_filtration(C);layers=audit_odd_layers(C)
    a=R['least_odd'];S=membership_stats(R['S']['G'],a);U=membership_stats(R['U']['G'],a)
    values=set(S['w']);birth={}
    for n,layer in enumerate(layers['power_layers'],1):
        for u in layer:
            assert u not in birth;birth[u]=n
    nu_by_value={v:n for n,block in enumerate(filtration['associated_graded_value_bases']) for v in block}
    assert set(nu_by_value)==values
    original=[p for p in S['G'] if p!=a]
    beta=[p//2 if p%2==0 else (p-a)//2 for p in original]
    chi=[p%2 for p in original];assert all(x>0 for x in beta)
    # Original labels are retained even when redundant in U. Optimize odd count,
    # then lexicographic word, only on the exact U-Apéry representatives.
    words={0:(0,)*len(original)};counts={0:0}
    for s in sorted(range(1,a),key=lambda s:U['w'][s]):
        choices=[]
        for j,b in enumerate(beta):
            parent=(s-b)%a
            if U['w'][parent]+b==U['w'][s]:
                word=list(words[parent]);word[j]+=1
                choices.append((counts[parent]+chi[j],tuple(word)))
        assert choices
        counts[s],words[s]=min(choices)
    columns=[];all_positions=set();D=[];nu=[];lambdas=[]
    for s in range(a):
        K,L=R['T_lifts'][s],R['I_lifts'][s];lam=K+L
        v=S['w'][(2*s)%a];degree=nu_by_value[v]
        positions=[];excess=[];deaths=[]
        for k in range(K):
            u=U['w'][s]+k*a;n=birth[u];all_positions.add(u)
            E=n+2*k-lam;assert E>=0
            dead=n*a+2*u not in values;assert dead==(E>0)
            positions.append({'k':k,'u':u,'birth':n,'excess':E,'killed':dead})
            excess.append(E);deaths.append(dead)
        assert all(birth[positions[k+1]['u']]<=positions[k]['birth']-2 for k in range(K-1))
        assert excess==sorted(excess,reverse=True)
        killed=sum(deaths);assert deaths==[True]*killed+[False]*(K-killed)
        assert lam==degree+2*killed and K==(degree+1)//2+killed and L==degree//2+killed
        assert degree%2==K-L
        initial_birth=birth[U['w'][s]] if K else 0
        assert counts[s]==initial_birth and lam+int(killed>0)<=counts[s]
        columns.append({'s':s,'U_value':U['w'][s],'K':K,'L':L,'lambda':lam,'nu':degree,
                        'D':killed,'U_word':list(words[s]),'U_odd_count':counts[s],'positions':positions})
        D.append(killed);nu.append(degree);lambdas.append(lam)
    assert all_positions==set(birth)
    assert sum(D)==sum(filtration['killed_layer_counts'])
    assert sum(nu)==filtration['graded_degree_moment']
    assert sum(lambdas)==sum(nu)+2*sum(D)==layers['weighted_lift_mass']
    positive_alpha=[b for b,c in zip(beta,chi) if c]
    alpha=min(positive_alpha) if positive_alpha else None
    if alpha is not None:
        assert all(alpha*(v+2*d+int(d>0))<=u for v,d,u in zip(nu,D,U['w']))
    J=sum(d>0 for d in D);Aalpha=sum(u//alpha for u in U['w']) if alpha is not None else 0
    zero_refinement=sum(v if d==0 else u//alpha-1 for v,d,u in zip(nu,D,U['w'])) if alpha is not None else 0
    parent=audit_parity_credit(C)
    result={'S':R['S'],'U':R['U'],'a':a,'original_source_labels':original,
            'normalized_labels':beta,'odd_flags':chi,'columns':columns,
            'sum_nu':sum(nu),'sum_D':sum(D),'J':J,'sum_lambda':sum(lambdas),
            'U_odd_moment_Z':sum(counts.values()),'alpha_min':alpha,'A_alpha':Aalpha,
            'alpha_strict_upper':Aalpha-J,'zero_death_column_upper':zero_refinement,
            'full_parent_reserve':parent['unused_deficit_reserve'],
            'parent_primitive_credit':parent['primitive_credit'],
            'full_parent_scaled_W':parent['full_scaled_W'],
            'pointwise_initial_segments_checked':a,'universal_sign_claim':False}
    if S['G']==[31,33,101,103]:
        assert a==31 and U['G']==[1] and beta==[1,35,36] and chi==[1,1,1]
        assert (S['c'],S['g'],S['W'])==(588,312,516)
        assert (sum(nu),sum(D),J,sum(lambdas),Aalpha)==(123,87,27,297,465)
        assert zero_refinement==Aalpha-J==438
        assert 4*33==101+31 and 5*33==103+2*31
        single=[];combined=[];packing=[]
        for s in range(a):
            assert words[s]==(s,0,0) and counts[s]==s
            j,r=divmod(s,5);four=int(r==4);five=j
            assert 4*four+5*five<=s
            credit=four+2*five
            # Independent bounded integer packing for THIS 31-element audit.
            exact=max(x+2*y for x in range(s//4+1) for y in range(s//5+1) if 4*x+5*y<=s)
            assert credit==exact==2*j+int(r==4)
            word=[s-4*four-5*five,four,five]
            constructed=sum(n*p for n,p in zip(word,original))
            assert constructed==2*s+a*(s-credit)==S['w'][(2*s)%a]
            assert lambdas[s]==counts[s]-credit
            assert lambdas[s]<=counts[s]-max(credit,int(D[s]>0))
            single.append(2*j);combined.append(credit)
            packing.append({'s':s,'four_blocks':four,'five_blocks':five,'credit':credit,
                            'replacement_source_word':word,'source_value':constructed})
        assert sum(single)==162 and sum(combined)==168
        b=(a-1)//2;E=S['e'];base=sum(R['W_parts'][:3])
        bounds={'alpha_min_with_strict_dead':base-E*(b+Aalpha-J),
                'zero_death_columns':base-E*(b+zero_refinement),
                'single_trade':base-E*(b+sum(counts.values())-sum(single)),
                'single_trade_max_strict':base-E*(b+sum(counts.values())-sum(max(c,int(d>0)) for c,d in zip(single,D))),
                'combined_disjoint_trades':base-E*(b+sum(counts.values())-sum(combined))}
        assert bounds=={'alpha_min_with_strict_dead':-48,'zero_death_columns':-48,
                        'single_trade':492,'single_trade_max_strict':496,'combined_disjoint_trades':516}
        result['fixed_trade_control']={'single_credit':sum(single),'combined_credit':sum(combined),
            'single_joint_upper':sum(counts.values())-sum(single),'combined_joint_upper':sum(counts.values())-sum(combined),
            'single_twice_killed_upper':sum(counts.values())-sum(single)-sum(nu),
            'combined_twice_killed_upper':sum(counts.values())-sum(combined)-sum(nu),
            'packing':packing,'full_budget_lower_bounds':bounds,'overlap_guard':'disjoint original inputs; strict-death combined by MAX'}
    return result

def constructed_tile_profile(words,P,a,M,require_downset=True):
    """Exact source-word bound; geometry is required only when explicitly used."""
    D=set(map(tuple,words));d=len(P);assert len(D)==a and d>=1
    assert all(len(z)==d and all(n>=0 for n in z) for z in D)
    value=lambda z:sum(p*n for p,n in zip(P,z))
    assert {value(z)%a for z in D}==set(range(a))
    missing=set()
    for z in D:
        for j,n in enumerate(z):
            if n:
                v=list(z);v[j]-=1
                if tuple(v) not in D:missing.add(tuple(v))
    if require_downset:assert not missing
    total=sum(map(value,D));e=d+1
    lower=F((e-1)*M)-F(e*total,a)-F((e-2)*(a-1),2)
    assert lower.denominator==1
    return {'words':[list(z) for z in sorted(D)],'source_value_sum':total,
            'constructed_maximum':max(map(value,D)),'L':int(lower),
            'units_present':[j for j in range(d) if tuple(int(i==j) for i in range(d)) in D],
            'downset':not missing,'missing_immediate_predecessors':[list(z) for z in sorted(missing)]}

def top_cap_profile(words,P,a,M,actual):
    """Arithmetic upper bounds only: capped values need not belong to S."""
    D=set(map(tuple,words));e=len(P)+1
    raw={sum(p*n for p,n in zip(P,z))%a:sum(p*n for p,n in zip(P,z)) for z in D}
    assert len(raw)==a and len(actual)==a and max(actual)==M
    caps={s:min(v,M-(M-s)%a) for s,v in raw.items()}
    assert all(actual[s]%a==s and 0<=actual[s]<=caps[s]<=raw[s]
               and (caps[s]-actual[s])%a==0 for s in raw)
    credit=sum(raw[s]-caps[s] for s in raw)//a
    bound=F((e-1)*M)-F(e*sum(caps.values()),a)-F((e-2)*(a-1),2)
    assert bound.denominator==1
    return {'raw_L':constructed_tile_profile(D,P,a,M,require_downset=False)['L'],
            'free_cap_credit':credit,'Lcap':int(bound),'cap_values_by_source_residue':[caps[s] for s in range(a)],
            'remaining_excess':sum(caps[s]-actual[s] for s in raw)//a,
            'cap_values_are_not_claimed_source_elements':True}

def audit_unit_orbits(paths):
    """E465: exact unit images of cached genuine lex tiles, no source sampling."""
    seeds=[]
    for path in paths:
        if path.endswith('.jsonl'):
            with open(path) as data:rows=[json.loads(line) for line in data if line.strip().startswith('{')]
            row=next(R for R in reversed(rows) if 'w' in R)
            seed=dict(row)
        else:
            with open(path) as data:R=json.load(data)
            S=R['S'];m=R['a'];assert S['m']==m
            w=[0]*m
            for C in R['columns']:w[2*C['s']%m]=2*C['U_value']+m*C['lambda']
            seed=dict(S,m=m,generators=S['G'],w=w,r=w.index(max(w)),rho=(-S['c'])%m,
                      mu=[max(0,(S['c']-v+m-1)//m) for v in w])
        seeds.append((path,seed))
    report={'kind':'cached_unit_orbit_audit','orbits':[],'unit_images':0,
            'explicit_new_sources_reconstructed':0,'universal_positivity_claim':False,
            'realizability_dependency':'E455 strict lex realization plus E462 CRT; scalar dilation alone has cofactor',
            'counts_include_repeated_structures':True}
    promoted=[]
    for path,D in seeds:
        R=support_geometry(D);m=D['m'];d=D['e']-1;gr,z=factor_basis(D)
        P=[D['w'][g] for g in gr]
        deletion_gcds=[gcd(m,*(p for k,p in enumerate(P) if k!=j)) for j in range(d)]
        eligible=3*D['e']<m and R['canonical_height']>=3 and all(g==1 for g in deletion_gcds)
        phi={word:s for s,word in z.items()};gamma=R['gamma'];dep=R['Dep'];top=D['r']
        columns=[]
        for j in range(d):
            groups=defaultdict(list)
            for word in phi:groups[word[:j]+word[j+1:]].append(word)
            for group in groups.values():
                end=max(group,key=lambda word:word[j]);columns.append((group,phi[end]))
        C=(D['e']-2)*m*(m-1)//2;images=[]
        for unit in range(1,m):
            if gcd(unit,m)!=1:continue
            delta=[unit*g%m for g in gr];r=unit*top%m;rho=m-r-1
            labels=[(unit*s+rho)%m for s in range(m)]
            kappa=sum(sum(word[j]*delta[j]%m for j in range(d))//m for word in phi)
            inversions=sum(labels[phi[word]]>labels[end] for group,end in columns for word in group)
            Q=dep+inversions-kappa
            numerator=m*dep+sum(gamma[s]*(unit*(top-s)%m) for s in range(m))-C
            assert numerator==m*Q
            if unit==1:
                assert (Q,kappa,inversions)==(R['Q_full'],R['kappa'],R['inversions'])
            image={'unit':unit,'actual_top_residue':r,'Dep':dep,'kappa':kappa,'N':inversions,
                   'F':kappa-dep,'Q':Q,'exact_column_phase_formula_agreement':True}
            images.append(image)
            if eligible and (Q<0 or image['F']>0):
                promoted.append((Q>=0,Q,-image['F'],m,unit,path,D,image))
        by_unit={T['unit']:T for T in images}
        for unit,T in by_unit.items():
            opposite=by_unit[m-unit]
            assert T['Q']+opposite['Q']==2*dep+m-1-sum(z[top])
            assert T['kappa']+opposite['kappa']==R['support_sum']
        orbit={'input':path,'m':m,'e':D['e'],'source_G':D['generators'],
               'height':R['canonical_height'],'baseline_Q':R['Q_full'],'baseline_F':R['kappa']-dep,
               'support_sum':R['support_sum'],'nonmultiplicity_deletion_gcds':deletion_gcds,
               'normalized_nonflat_sparse_realizable':eligible,'mirror_identities_checked':True,
               'images':images,'minimum_Q':min(T['Q'] for T in images),'maximum_F':max(T['F'] for T in images)}
        report['orbits'].append(orbit);report['unit_images']+=len(images)
    if promoted:
        *_,path,seed,image=min(promoted,key=lambda T:T[:5])
        report['selected_profile']={'input':path,'seed':seed,'image':image,
            'promotion_reason':'negative_Q' if image['Q']<0 else 'nonflat_positive_F',
            'explicit_normalized_source_still_required':True}
    else:report['selected_profile']=None
    report['negative_Q_images']=sum(T['Q']<0 for R in report['orbits'] for T in R['images'])
    report['nonflat_positive_F_images']=sum(T['F']>0 for R in report['orbits'] if R['normalized_nonflat_sparse_realizable'] for T in R['images'])
    return report

def audit_factorization_energy(C):
    """Exact original-word collisions; no floating point or fitted weights."""
    S=membership_stats(C['G']);m=S['m'];e=S['e'];c=S['c'];G=S['G'];w=S['w']
    D=dict(S,generators=G,r=w.index(max(w)),rho=(-c)%m,
           mu=[max(0,(c-v+m-1)//m) for v in w])
    geometry=support_geometry(D)
    for key,value in C.items():
        assert (sorted(value)==sorted(geometry[key]) if key=='G' else value==geometry[key]),key
    counts=[0]*c;counts[0]=1
    for p in G:
        for value in range(p,c):counts[value]+=counts[value-p]
    assert sum(n==0 for n in counts)==S['g']
    mass=sum(counts);energy=sum(n*n for n in counts)
    assert F(mass*mass,energy)<=c-S['g']
    margin=e*mass*mass-c*energy;cutoff=(e-2)*m*(m-1)*(m-e+1)//2
    return {'S':{key:S[key] for key in ('m','e','c','g','W','G')},
            'leave_one_out_gcds':[gcd(*(G[:j]+G[j+1:])) for j in range(e)],
            'Q':geometry['Q_full'],'R':S['W']-geometry['Q_full'],
            'factorization_counts_below_c':counts,'factorization_mass_A':mass,
            'collision_energy_E':energy,'cauchy_left_lower_bound':str(F(mass*mass,energy)),
            'actual_left_count':c-S['g'],'energy_ratio':str(F(energy,mass*mass)),
            'proposed_ratio_upper_e_over_c':str(F(e,c)),
            'exact_margin_eA2_minus_cE':margin,'candidate_failure':margin<0,
            'M':max(w),'E448_M_cutoff':cutoff,'within_E448_cutoff':max(w)<=cutoff,
            'original_generator_count_retained':True,'universal_sign_claim':False}

def audit_top_cap_controls(records,source,trace):
    """E461 fixed countermechanism controls, not a semigroup search."""
    result={'controls':[],'universal_positivity_claim':False,'family_census':False}
    for R in records:
        S=R['S'];a=R['a'];P=R['original_source_labels'];M=S['c']+a-1
        D={tuple(C['U_word']) for C in R['columns']};actual=[0]*a
        for C in R['columns']:actual[2*C['s']%a]=2*C['U_value']+a*C['lambda']
        B=top_cap_profile(D,P,a,M,actual)
        assert B['Lcap']==S['W']-S['e']*B['remaining_excess']
        entry={'S':S,'a':a,**B}
        if S['G']==[201,203,593,595]:
            assert P==[203,593,595] and R['U']['G']==[1]
            assert D=={(s,0,0) for s in range(196)}|{(0,1,0),(0,0,1),(1,0,1),(2,0,1),(3,0,1)}
            q=M//a;assert 74<=q<=78
            assert M//203+(5*M)//593+1>=201
            assert B['Lcap']<0 and B['Lcap']>=2*q*q-179*q-1044
            new_caps=B['cap_values_by_source_residue'][:];returns=[];lambdas=0
            for s in range(160,196):
                n=201-s;t=(n+4)//5;x=5*t-n;word=(x,t,0)
                value=203*x+593*t;lam=(value-2*s)//a;r=2*s%a
                assert (value-2*s)%a==0 and 0<=lam<=29
                oldcap=new_caps[r];assert (oldcap-2*s)//a>=q-2
                assert actual[r]<=value<oldcap
                new_caps[r]=value;lambdas+=lam
                returns.append({'closure_residue':s,'word':list(word),'source_value':value,
                                'lambda':lam,'net_cap_credit':(oldcap-value)//a})
            assert lambdas==554
            net=sum(C['net_cap_credit'] for C in returns)
            improved=B['Lcap']+S['e']*net
            assert net>=36*(q-2)-554 and improved>=4814 and improved<=S['W']
            assert B['Lcap']<=2*q*q-187*q+1172<=-1246
            entry['weighted_returns']={'count':len(returns),'lambda_sum':lambdas,
                'net_cap_credit':net,'improved_L':improved,'words':returns,
                'not_an_apery_reconstruction':True,'paper_only_minimum_improved_bound':4814}
        result['controls'].append(entry)
    assert source['generators']==[38,51,67,120,193]
    a=trace['a'];P=trace['P'];D=set(map(tuple,trace['initial_words']));M=trace['M_actual']
    S=membership_stats(source['generators'],a)
    assert all(S[k]==source[k] for k in ('m','e','c','g','W'))
    B=top_cap_profile(D,P,a,M,S['w']);assert B['Lcap']==S['W']-S['e']*B['remaining_excess']
    shadows=[]
    for trade in positive_tile_borders(D,P,a):
        x,y=trade['x'],trade['y'];out=set();copies=0
        for z in D:
            q=min(z[j]//x[j] for j in range(len(P)) if x[j]);copies+=q
            out.add(tuple(z[j]+q*(y[j]-x[j]) for j in range(len(P))))
        C=top_cap_profile(out,P,a,M,S['w']);rawcredit=trade['sigma']*copies
        net=(C['Lcap']-B['Lcap'])//S['e']
        assert C['Lcap']-B['Lcap']==S['e']*net
        assert net==rawcredit-B['free_cap_credit']+C['free_cap_credit']>=0
        shadows.append({'input':list(x),'output':list(y),'raw_pivot_credit':rawcredit,
                        'net_after_cap_credit':net,'Lcap_after_shadow':C['Lcap']})
    assert (B['raw_L'],B['free_cap_credit'],B['Lcap'])==(-8,54,262)
    result['controls'].append({'S':{k:S[k] for k in ('m','e','c','g','W','G')},'a':a,
                               **B,'support_Q':source['Q'],'shadow_comparisons':shadows})
    return result

def fresh_unit_shadow(words,P,a,k):
    D=set(map(tuple,words));d=len(P);unit=tuple(int(i==k) for i in range(d))
    assert unit not in D and all(z[k]==0 for z in D)
    value=lambda z:sum(p*n for p,n in zip(P,z))
    x=next(z for z in D if value(z)%a==P[k]%a)
    gap=value(x)-P[k];assert gap>0 and gap%a==0
    sigma=gap//a;out=set();copies=0
    for z in D:
        q=min(z[j]//x[j] for j in range(d) if x[j]);copies+=q
        v=tuple(z[j]-q*x[j]+q*int(j==k) for j in range(d))
        assert value(z)-value(v)==q*sigma*a;out.add(v)
    assert len(out)==a
    return out,{'input':list(x),'restored_unit':k,'saving_per_copy':sigma,
                'copies':copies,'pivot_credit':copies*sigma}

def corner_exchange(words,P,a,x,y):
    D=set(map(tuple,words));x=tuple(x);y=tuple(y);d=len(P)
    assert x in D and y not in D
    assert all(tuple(x[i]+int(i==j) for i in range(d)) not in D for j in range(d))
    assert all(tuple(y[i]-int(i==j) for i in range(d)) in D for j in range(d) if y[j])
    assert not any(v and w for v,w in zip(x,y))
    gap=sum(p*(v-w) for p,v,w in zip(P,x,y));assert gap>0 and gap%a==0
    return (D-{x})|{y},{'input':list(x),'output':list(y),'pivot_credit':gap//a}

def audit_advisor_trade_controls(records):
    """E457/E458: ONLY saved31/39/51 audits, no sampling or family enumeration."""
    by_pivot={R['a']:R for R in records};assert set(by_pivot)=={31,39,51}
    states={};result={'controls':{},'universal_sign_claim':False,'search_campaign':False}
    for a,R in sorted(by_pivot.items()):
        P=R['original_source_labels'];S=R['S'];M=S['c']+a-1
        actual=[2*C['U_value']+a*C['lambda'] for C in R['columns']]
        assert max(actual)==M and F(sum(actual),a)-F(a-1,2)==S['g']
        assert (S['e']-1)*S['c']-S['e']*S['g']==S['W']
        D={tuple(C['U_word']) for C in R['columns']}
        profile=constructed_tile_profile(D,P,a,M)
        excess=(profile['source_value_sum']-sum(actual))//a
        assert profile['source_value_sum']-sum(actual)==a*excess>=0
        assert profile['L']==S['W']-S['e']*excess
        states[a]=(D,P,M);result['controls'][str(a)]={'S':S,'actual_maximum':M,
            'initial':profile,'exact_total_excess':excess}
    D,P,M=states[31];assert result['controls']['31']['initial']['L']==-156
    orders=[]
    for order,credits,expected in [([1,2],[105,35],404),([2,1],[162,6],516)]:
        current=set(D);steps=[];previous=-156
        for k,credit in zip(order,credits):
            current,step=fresh_unit_shadow(current,P,31,k)
            profile=constructed_tile_profile(current,P,31,M)
            assert step['pivot_credit']==credit and profile['L']-previous==4*credit
            previous=profile['L'];steps.append({'trade':step,'result':profile})
        assert previous==expected and len(profile['units_present'])==3
        orders.append({'restore_values':[P[k] for k in order],'total_credit':sum(credits),
                       'final_L':previous,'steps':steps})
    result['controls']['31']['restoration_orders']=orders
    D,P,M=states[39];profile=result['controls']['39']['initial']
    assert (M,profile['L'],profile['source_value_sum'])==(906,-144,27534)
    assert len(profile['units_present'])==3 and sum(C['U_odd_count'] for C in by_pivot[39]['columns'])==668
    assert M<=F((39+2)*(3*39-1),5)
    B=22;assert 5*B-3*39+4<2
    result['controls']['39']['bounded_input_obstruction']={'degree_cap':B,
        'twice_upper_saving':5*B-3*39+4,'minimum_necessary_positive_degree':(3*39-2+4)//5}
    D,P,M=states[51];profile=result['controls']['51']['initial'];assert profile['L']==-192
    assert (M,profile['source_value_sum'])==(1590,62628)
    steps=[];previous=profile['L'];current=set(D)
    for x,y,credit,expected in [((48,0,0),(0,1,1),44,-16),((47,0,0),(0,2,0),43,156)]:
        current,step=corner_exchange(current,P,51,x,y)
        profile=constructed_tile_profile(current,P,51,M)
        assert step['pivot_credit']==credit and profile['L']-previous==4*credit
        assert profile['L']==expected and len(profile['units_present'])==3
        previous=profile['L'];steps.append({'trade':step,'result':profile})
    result['controls']['51']['compatible_corner_exchanges']=steps
    out=set();copies=0
    for z in D:
        q=z[0]//47;copies+=q;v=(z[0]-47*q,z[1]+2*q,z[2])
        assert sum(p*(v0-v1) for p,v0,v1 in zip(P,z,v))==43*51*q
        out.add(v)
    scalar=constructed_tile_profile(out,P,51,M,require_downset=False)
    assert copies==2 and scalar['L']==152 and not scalar['downset']
    assert [1,1,0] in scalar['missing_immediate_predecessors']
    result['controls']['51']['scalar_47_shadow']={'pivot_credit':43*copies,'result':scalar}
    return result

def positive_tile_borders(words,P,a):
    D=set(map(tuple,words));d=len(P);value=lambda z:sum(p*n for p,n in zip(P,z))
    residues={value(z)%a:z for z in D};maximal=set();border=set()
    for z in D:
        children=[tuple(z[i]+int(i==j) for i in range(d)) for j in range(d)]
        if not any(y in D for y in children):maximal.add(z)
        for y in children:
            if y not in D and all(tuple(y[i]-int(i==j) for i in range(d)) in D for j in range(d) if y[j]):border.add(y)
    positive=[]
    for y in border:
        x=residues[value(y)%a];gap=value(x)-value(y)
        if gap>0:
            assert gap%a==0
            positive.append({'x':x,'y':y,'sigma':gap//a,'corner':x in maximal})
    return sorted(positive,key=lambda s:(-s['sigma'],s['x'],s['y']))

def audit_trade_policy_trace(source,T,source_verifier):
    independently_checked=source_verifier(source)
    assert T['actual_generators']==source['generators'] and T['m']==source['m']
    if source['W']<0:
        assert T['status']=='negative_W'
        return {'source':independently_checked,'policy_not_evaluated':True,'negative_W':True}
    if not T['accepted']:
        assert T['status']=='rejected'
        return {'source':independently_checked,'policy_not_evaluated':True,'negative_W':False}
    a=min(p for p in source['generators'] if p%2);assert a==T['a']<=256
    P=[p for p in source['generators'] if p!=a];d=len(P);e=d+1
    beta=[(p-a)//2 if p%2 else p//2 for p in P]
    assert T['P']==P and T['beta']==beta
    U=membership_stats([a]+beta,a);assert U['w']==T['closure_apery']
    words={0:(0,)*d};odd={0:0}
    for s in sorted(range(1,a),key=lambda s:U['w'][s]):
        candidates=[]
        for j,b in enumerate(beta):
            parent=(s-b)%a
            if U['w'][parent]+b==U['w'][s]:
                word=list(words[parent]);word[j]+=1
                candidates.append((odd[parent]+P[j]%2,tuple(word)))
        assert candidates
        odd[s],words[s]=min(candidates)
    D=set(words.values());assert D==set(map(tuple,T['initial_words']))
    M=source['c']+a-1;assert M==T['M_actual']
    profile=constructed_tile_profile(D,P,a,M);assert profile['L']==T['initial_L']<=source['W']
    total=0;corners=0;initial=profile['L']
    for step in T['steps']:
        missing=[j for j in range(d) if tuple(int(i==j) for i in range(d)) not in D]
        if step['kind']=='unit':
            choices=[]
            for j in missing:
                candidate,trade=fresh_unit_shadow(D,P,a,j)
                choices.append((-trade['pivot_credit'],j,candidate,trade))
            assert choices
            _,j,next_D,trade=min(choices,key=lambda v:(v[0],v[1]))
            assert step['x']==trade['input'] and step['y']==[int(i==j) for i in range(d)]
            assert step['sigma']==trade['saving_per_copy'] and step['copies']==trade['copies']
            assert step['credit']==trade['pivot_credit']
        else:
            assert step['kind']=='corner' and not missing and profile['L']<0
            choices=[v for v in positive_tile_borders(D,P,a) if v['corner']];assert choices
            best=choices[0]
            assert tuple(step['x'])==best['x'] and tuple(step['y'])==best['y'] and step['sigma']==best['sigma']
            next_D,trade=corner_exchange(D,P,a,step['x'],step['y'])
            assert step['copies']==1 and step['credit']==trade['pivot_credit'];corners+=1
        next_profile=constructed_tile_profile(next_D,P,a,M)
        assert next_profile['L']-profile['L']==e*step['credit'] and next_profile['L']<=source['W']
        assert set(profile['units_present'])<=set(next_profile['units_present'])
        total+=step['credit'];D=next_D;profile=next_profile
    assert D==set(map(tuple,T['final_words'])) and len(profile['units_present'])==d
    assert total==T['total_credit'] and initial+e*total==profile['L']==T['final_L']
    assert corners==T['corner_steps']
    positive=positive_tile_borders(D,P,a);corner_count=sum(v['corner'] for v in positive)
    if T['status']=='negative_L_corner_stall':
        assert profile['L']<0 and corner_count==T['terminal_positive_corners']==0
    elif T['status']=='step_cap_unresolved':
        assert profile['L']<0 and corners==T['step_cap']==1000
    else:assert T['status']=='nonnegative_L' and profile['L']>=0
    result={'source':independently_checked,'a':a,'initial_L':initial,'final_L':profile['L'],
            'total_credit':total,'steps_replayed':len(T['steps']),'corners':corners,
            'terminal_positive_corners':corner_count,'terminal_positive_borders':len(positive),
            'status':T['status'],'exact_initial_U_words':True,'all_states_and_policy_choices_checked':True,
            'universal_sign_claim':False}
    if T['status']=='negative_L_corner_stall':
        shadows=[]
        for move in positive:
            x,y=move['x'],move['y'];out=set();copies=0
            for z in D:
                q=min(z[j]//x[j] for j in range(d) if x[j]);copies+=q
                out.add(tuple(z[j]-q*x[j]+q*y[j] for j in range(d)))
            shadow=constructed_tile_profile(out,P,a,M,require_downset=False)
            credit=copies*move['sigma']
            assert shadow['L']-profile['L']==e*credit
            shadows.append({'x':list(x),'y':list(y),'sigma':move['sigma'],'copies':copies,
                            'pivot_credit':credit,'new_L':shadow['L'],'downset':shadow['downset'],
                            'missing_predecessors':shadow['missing_immediate_predecessors']})
        result['noncorner_shadow_diagnostics']=sorted(shadows,key=lambda v:-v['pivot_credit'])
    return result

def rational_row_rank(rows,width):
    basis={}
    for values in rows:
        row=list(map(F,values));assert len(row)==width
        for k in range(width):
            if not row[k]:continue
            if k in basis:
                q=row[k];row=[a-q*b for a,b in zip(row,basis[k])]
            else:
                q=row[k];basis[k]=[a/q for a in row];break
    return len(basis)

def audit_differential(C):
    """E443: C trade witnesses plus independent factorization DP over Q."""
    G=C['G'];S=membership_stats(G);m=S['m'];e=S['e'];c=S['c'];ell=c-S['g'];cap=c+max(G)
    assert sorted(G)==S['G'] and all(C[k]==S[k] for k in ('c','g','e','W'))
    assert C['ell']==ell and C['free_dimension']==e*ell
    member=[n>=S['w'][n%m] for n in range(cap)]
    facts=[set() for _ in range(cap)];facts[0].add((0,)*e)
    for j,p in enumerate(G):
        for N in range(p,cap):
            for z in facts[N-p]:
                v=list(z);v[j]+=1;facts[N].add(tuple(v))
    blocks={B['N']:B for B in C['blocks']};assert len(blocks)==len(C['blocks'])
    selected=0;total=0;torsion={};dimensions={};degree_ranks={}
    for N in range(1,cap):
        active=[int(0<=N-p<c and member[N-p]) for p in G]
        allfacts=sorted(facts[N]);rows=[]
        if allfacts:
            base=allfacts[0]
            rows=[[a*(z[j]-base[j]) for j,a in enumerate(active)] for z in allfacts[1:]]
        rank=rational_row_rank(rows,e);total+=rank;degree_ranks[N]=rank
        dim=sum(active)-rank;dimensions[N]=dim
        image=int(N<c+m and member[N]);q=dim-image
        assert q>=0
        if q:torsion[N]=q
        if N in blocks:
            B=blocks[N];assert B['active']==active and tuple(B['base']) in facts[N]
            assert all(tuple(z) in facts[N] for z in B['trades'])
            witness=[[a*(z[j]-B['base'][j]) for j,a in enumerate(active)] for z in B['trades']]
            assert rational_row_rank(witness,e)==B['rank']==len(B['trades'])
            selected+=B['rank'];assert B['rank']==rank
        elif not C['stopped_at_failure'] or N<=max(blocks):assert rank==0
    assert selected==C['selected_relation_rank']
    assert C['differential_dimension_upper_bound']==e*ell-selected
    if not C['stopped_at_failure']:assert total==selected
    dim=e*ell-total;q=sum(torsion.values())
    assert dim==sum(dimensions.values())==ell+m-1+q
    assert C['stopped_at_failure']==(selected>C['W'])
    gaps=[n for n in range(m,c) if not member[n]];assert len(gaps)==S['g']-m+1
    shifts=[];failures=[]
    if gaps and torsion:
        lo=max(gaps)+min(torsion);hi=min(gaps)+max(torsion)
        for shift in range(lo,hi+1):
            absent=next((n for n in gaps if not torsion.get(shift-n)),None)
            if absent is None:shifts.append(shift)
            else:failures.append({'shift':shift,'unpaid_gap':absent,'torsion_degree':shift-absent})
    else:lo=hi=None
    return {'S':{k:S[k] for k in ('G','m','e','c','g','W')},'ell':ell,
            'C_selected_rank':selected,'full_rational_relation_rank':total,'differential_dimension':dim,
            'conductor_bound_margin':dim-c,'Euler_image_dimension':ell+m-1,
            'torsion_quotient_dimension':q,'required_gap_rank':len(gaps),'torsion_degrees':torsion,
            'possible_reflection_shift_range':[lo,hi],'admissible_reflection_shifts':shifts,
            'reflection_failure_witnesses':failures,'independently_enumerated_factorizations':sum(map(len,facts)),
            'genuine_negative_W':S['W']<0}

def audit_odd_layers(C):
    """E442: audit ideal powers by independent sets and Apéry convolution."""
    R=audit_odd_comparison(C);a=R['least_odd'];A=R['ideal_generators']
    T=membership_stats(R['T']['G'],a);U=membership_stats(R['U']['G'],a)
    c=T['c'];base={x for x in range(c) if x>=T['w'][x%a]}
    target={x for x in range(c) if x>=U['w'][x%a]}
    sets=[base];tables=[T['w']];layers=[]
    for n in range(1,T['g']+2):
        nxt={x+y for x in A for y in sets[-1] if x+y<c}
        # The finite slice excludes the tail; nonnegative offsets cannot bring it back.
        table=[min(x+tables[-1][(s-x)%a] for x in A) for s in range(a)]
        assert nxt=={x for x in range(c) if x>=table[x%a]}
        assert table==[next(x for x in range(s,c+a,a) if x>=c or x in nxt) for s in range(a)]
        assert sets[-1]<=nxt<=target
        if nxt==sets[-1]:
            assert nxt==target and table==U['w'];break
        layers.append(nxt-sets[-1]);sets.append(nxt);tables.append(table)
    else:raise AssertionError('ideal powers did not stabilize within the exact genus bound')
    assert sum(map(len,layers))==T['g']-U['g']
    assert sum(map(len,layers[1:]))==R['ideal_genus']-U['g']
    mass=sum(R['T_lifts'])+sum(R['I_lifts'])
    assert mass==(len(layers[0])+2*sum(map(len,layers[1:])) if layers else 0)
    degree1=layers[0] if layers else set();products={0}
    for n,layer in enumerate(layers,1):
        products={x+y for x in products for y in degree1 if x+y in layer}
        assert products==layer  # Each graded piece is spanned by degree-one products.
        assert len(layer)<=comb(len(degree1)+n-1,n)
        for x in layer:
            lower=sets[max(0,n-2)]
            assert x+a>=c or x+a in lower  # a+nI subset (n-2)I, with the n=1 boundary.
    paired=sorted({a+x+y for x in A for y in A});action=[]
    for n,layer in enumerate(layers,1):
        for p in paired:
            hit=next((x for x in sorted(layer) if x+p in layer),None)
            if hit is not None:action.append({'degree':n,'paired_T_element':p,'x':hit,'image':hit+p})
    return {'S':R['S'],'U':R['U'],'least_odd':a,'source_embedding_dimension':R['S']['e'],
            'odd_ideal_generator_count':len(A),'Hilbert_function':[1]+[len(L) for L in layers],
            'power_layers':[sorted(L) for L in layers],'stabilization_power':len(layers),
            'weighted_lift_mass':sum(R['T_lifts'])+sum(R['I_lifts']),
            'paired_quotient_actions':action,'all_modulus_entries_and_products_checked':True}

def audit_residue_comparison(C):
    S=membership_stats(C.get('input_G',C['G']));m=S['m']
    T=membership_stats([m]+[g%m for g in S['G'] if g!=m],m)
    for actual,reported in [(S,C),(T,C['residue'])]:
        for key in ('m','e','c','g','W','G'):
            assert actual[key]==(sorted(reported[key]) if key=='G' else reported[key]),(key,actual,reported)
    assert T['e']<=S['e'] and (m==1 or T['m']<m)
    K=[]
    for w,tau in zip(S['w'],T['w']):
        k,rem=divmod(w-tau,m);assert rem==0 and k>=0;K.append(k)
    assert all(k>=1 for k in K[1:])
    cost=S['e']*sum(K)
    credit=(S['e']-1)*(S['c']-T['c'])+(S['e']-T['e'])*(T['c']-T['g'])
    assert C['margin']==S['W']-T['W']==credit-cost
    assert 2*T['W']<=(T['e']-2)*T['c']
    return {'G':S['G'],'residue_G':T['G'],'margin':C['margin'],'shifts':K,'cost':cost,'credit':credit,
            'generic_bound_excludes_failure':2*S['W']>=(T['e']-2)*T['c']}

def audit_primitive_tangent(C):
    D,B,A=C['seed'],C['before'],C['after'];L=C['L'];v=C['v']
    assert type(L) is int and all(type(a) is int for a in v)
    for S in (D,B,A):audit(S)
    m,e,r=D['m'],D['e'],D['r'];gr,z=factor_basis(D);d=e-1
    assert len(v)==d and L>0 and L%m==1
    assert sorted(B['generators'])==sorted([m]+[L*D['w'][g] for g in gr])
    assert sorted(A['generators'])==sorted([m]+[L*D['w'][g]+m*v[j] for j,g in enumerate(gr)])
    h=[sum(z[s][j]*v[j] for j in range(d)) for s in range(m)]
    for i,j,s,J,*_ in D['pairs']:
        if not J:assert h[i]+h[j]==h[s]
    for S in (B,A):
        assert (S['m'],S['e'],S['r'])==(m,e,r)
        assert [(i,j,s,J==0) for i,j,s,J,*_ in S['pairs']]==[(i,j,s,J==0) for i,j,s,J,*_ in D['pairs']]
        assert factor_basis(S)==(gr,z)
    assert B['w']==[L*w for w in D['w']]
    assert A['w']==[L*w+m*h[s] for s,w in enumerate(D['w'])]
    H=[d*m*z[r][j]-e*sum(z[s][j] for s in range(m)) for j in range(d)]
    change=sum(a*b for a,b in zip(H,v));assert A['W']-B['W']==change
    x=list(map(F,C.get('unpaid',[0]*m)));assert len(x)==m and x[0]==0
    for S in (D,B,A):
        assert all(0<=x[s]<=S['mu'][s] for s in range(m))
        assert all(x[g]==0 for g in gr)
        for i,j,s,J,tau,lo,up in S['pairs']:
            if not J:assert -(up-tau)<=x[i]+x[j]-x[s]<=tau+lo
    if L>2*m*(m-1)*max(map(abs,v),default=0):
        assert all(B['mu'][s]>=D['mu'][s] and A['mu'][s]>=D['mu'][s] for s in range(m))
    negative_strict=[p for p,(i,j,s,J,*_) in enumerate(D['pairs']) if J and (i in gr or j in gr) and h[i]+h[j]-h[s]<0]
    return {'seed':sorted(D['generators']),'L':L,'v':v,'H':H,'h':h,'before_W':B['W'],'after_W':A['W'],
            'change':change,'unpaid_mass':str(sum(x)),'before_J':str(B['W']-e*sum(x)),
            'after_J':str(A['W']-e*sum(x)),
            'negative_strict_primitive_rows':negative_strict,
            'negative_cap_residues':[s for s in range(m) if h[s]>h[r]],
            'coarse_bound_applies':L>2*m*(m-1)*max(map(abs,v),default=0)}

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
            'Q_full':dep-kappa+inversions,'phase':inversions-kappa,
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

def audit_mstd_shadow(R):
    """Independent E436 sum/difference and unbounded-coin membership audit."""
    from itertools import product
    seed=(0,2,3,4,7,11,12,14)
    A=sorted({sum(x*29**i for i,x in enumerate(word)) for word in product(seed,repeat=3)})
    sums={a+b for a in A for b in A};diffs={a-b for a in A for b in A}
    T=max(A)+1;B=[T+a for a in A];d=len(B);m=4*max(B)+2;G=[m]+[m+b for b in B]
    assert (len(A),len(sums),len(diffs),max(A))==(512,17576,15625,12194)
    assert all(m<g<2*m for g in G[1:]) and 3*len(G)<m
    common=0
    for g in G:common=gcd(common,g)
    assert common==1
    # Sparse exponent comparison implements lex order directly, independently
    # of the C++ shortcut of maximizing the lesser generator index.
    def word(i,j):
        result={i:1};result[j]=result.get(j,0)+1;return result
    def lex_less(a,b):
        for k in sorted(a.keys()|b.keys()):
            if a.get(k,0)!=b.get(k,0):return a.get(k,0)<b.get(k,0)
        return False
    representatives={}
    for i in range(d):
        for j in range(i,d):
            t=B[i]+B[j];candidate=word(i,j)
            if t not in representatives or lex_less(candidate,representatives[t]):representatives[t]=candidate
    assert len(representatives)==len(sums)
    assert all(representatives[2*B[i]]=={i:2} for i in range(d))
    # Bitset reachability processes binary powers of each generator; it is an
    # exact unbounded-coin DP, independent of residue shortest paths.
    N=max(R['apery'])+m;assert N<=20000000
    mask=(1<<(N+1))-1;member=1
    for g in G:
        shift=g
        while shift<=N:
            member|=member<<shift;member&=mask;shift*=2
    lastgap=(mask^member).bit_length()-1;c=lastgap+1
    assert N-lastgap>=m
    ell=(member&((1<<c)-1)).bit_count();genus=c-ell;W=len(G)*ell-c
    blob=member.to_bytes((N+8)//8,'little');w=[None]*m;found=0
    for n in range(N+1):
        if blob[n//8]>>(n%8)&1 and w[n%m] is None:
            w[n%m]=n;found+=1
            if found==m:break
    assert w==R['apery'] and c>=5*m and not (blob[(5*m-1)//8]>>((5*m-1)%8)&1)
    assert all(w[t]==2*m+t for t in representatives)
    rho=(-c)%m;P={0,*B};F=set()
    cells=[{i:1} for i in range(d)]+list(representatives.values())
    for v in cells:
        raw=sum(B[i]*n for i,n in v.items())
        for j,n in v.items():
            if n==1:F.add((raw-B[j],j))
    images={(v-B[j])%m for v,j in F};assert not (images&P)
    assert len(images)<=d+len(diffs)-1
    Gamma=0;V=sum(rho+b>=m for b in B)
    for i in range(d):
        for j in range(d):
            if representatives[B[i]+B[j]]!=word(i,j):Gamma+=1+(i==j)
            elif (B[i]+rho)%m+B[j]>=m:V+=1+(i==j)
    exterior=len(F)-len(images);unused=len(F)-len(representatives);shortfall=exterior-unused
    expected={'radix':29,'power':3,'A_size':d,'A_max':max(A),'shift':T,
              'sum_count':len(sums),'difference_count':len(diffs),'m':m,'e':len(G),
              'c':c,'g':genus,'ell':ell,'W':W,'rho':rho,'cut_size':1+d+len(representatives),
              'nonmaximal':1+d,'maximal':len(representatives),'negative_starts':len(F),
              'exterior_images':len(images),'internal_aliases':0,'raw_carry':0,
              'exterior_debt':exterior,'unused_starts':unused,'staged_shortfall':shortfall,
              'missing_capacity':Gamma,'wrapped_capacity':V,'joint_margin':Gamma+V-shortfall}
    assert all(R[k]==v for k,v in expected.items())
    assert shortfall>=1440 and Gamma==227504 and expected['joint_margin']>=0
    # Least signed-word roots of differences2 and3 both charge the missing
    # exit e_14+e_0, whose lex normal form is2e_7. Its capacity is only1.
    index={a:i for i,a in enumerate(A)}
    def signed(base,j):
        v={} if base==0 else {B.index(base):1};v[j]=v.get(j,0)-1
        return {i:n for i,n in v.items() if n}
    collisions=[]
    for image,subtrahend in [(2,12),(3,11)]:
        group=[f for f in F if (f[0]-B[f[1]])%m==image]
        assert all(base>0 and base-B[j]==image for base,j in group)
        root=group[0]
        for f in group[1:]:
            if lex_less(signed(*f),signed(*root)):root=f
        assert root==(T+image,index[0])
        chosen=(T+14,index[subtrahend]);assert chosen in group and chosen!=root
        assert representatives[(T+14)+(T+0)]=={index[7]:2}
        collisions.append({'image':image,'start':list(chosen),'root':list(root),
                           'exit_parent':T+14,'exit_direction':index[0],'capacity':1})
    assert len({(V['exit_parent'],V['exit_direction']) for V in collisions})==1
    return {**expected,'staged_claim_false':True,'joint_claim_failure':expected['joint_margin']<0,
            'genuine_negative_W':W<0,'independent_membership_limit':N,
            'all_apery_entries_checked':len(w),'membership_method':'exact unbounded-coin bitset DP',
            'least_root_exit_collision':collisions}

if __name__=='__main__':
    if sys.argv[1]=='--trade-policy-check':
        import importlib.util
        assert len(sys.argv)==5
        spec=importlib.util.spec_from_file_location('independent_scan_audit',sys.argv[2])
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=[];source=None
        with open(sys.argv[3]) as inp:
            for line in inp:
                if not line.startswith('{'):continue
                R=json.loads(line)
                if R.get('kind')=='trade_source':source=R
                elif R.get('kind')=='trade_policy_trace':
                    assert source is not None
                    result.append(audit_trade_policy_trace(source,R,module.verify));source=None
        assert result
        with open(sys.argv[4],'w') as out:json.dump({'results':result,'universal_sign_claim':False},out,indent=2)
        for R in result:print('POLICY-REPLAY',{k:v for k,v in R.items() if k not in ('source','noncorner_shadow_diagnostics')})
        sys.exit(0)
    if sys.argv[1]=='--advisor-trade-check':
        assert len(sys.argv)==6
        records=[]
        for path in sys.argv[2:5]:
            with open(path) as source:records.append(json.load(source))
        result=audit_advisor_trade_controls(records)
        with open(sys.argv[5],'w') as out:json.dump(result,out,indent=2)
        for a,R in result['controls'].items():
            print('TRADE-CONTROL',a,'initialL',R['initial']['L'],'exact_excess',R['exact_total_excess'])
        print('EXACTLY three saved controls; source bounds, both restoration orders, compatible exchanges and non-downset scalar shadow checked')
        sys.exit(0)
    if sys.argv[1]=='--factorization-energy-check':
        assert len(sys.argv)==4, 'raw C support record output'
        with open(sys.argv[2]) as data:C=json.load(data)
        result=audit_factorization_energy(C)
        with open(sys.argv[3],'w') as out:json.dump(result,out,indent=2)
        print('FACTORIZATION-ENERGY',{key:value for key,value in result.items() if key!='factorization_counts_below_c'})
        print('ONE fixed source; global sufficient energy rule only, no family-W claim')
        sys.exit(0)
    if sys.argv[1]=='--unit-orbit-check':
        assert len(sys.argv)>=4, 'cached input paths ... output'
        result=audit_unit_orbits(sys.argv[2:-1])
        with open(sys.argv[-1],'w') as out:json.dump(result,out,indent=2)
        for R in result['orbits']:
            print('UNIT-ORBIT',R['m'],'images',len(R['images']),'minQ',R['minimum_Q'],'maxF',R['maximum_F'])
        print('UNIT-TOTAL',result['unit_images'],'negativeQ',result['negative_Q_images'],
              'nonflat_positiveF',result['nonflat_positive_F_images'])
        if result['selected_profile']:print('SELECTED',result['selected_profile']['image'])
        print('Cached lex tiles only; unit-image scores have proved realizability but no new source invariants are claimed')
        sys.exit(0)
    if sys.argv[1]=='--top-cap-check':
        assert len(sys.argv)==8, 'old31 old39 old51 new201 stall_jsonl output'
        records=[]
        for path in sys.argv[2:6]:
            with open(path) as data:records.append(json.load(data))
        with open(sys.argv[6]) as data:traces=[json.loads(line) for line in data if line.strip()]
        source=next(R for R in traces if R['kind']=='trade_source')
        trace=next(R for R in traces if R['kind']=='trade_policy_trace')
        result=audit_top_cap_controls(records,source,trace)
        with open(sys.argv[7],'w') as out:json.dump(result,out,indent=2)
        for R in result['controls']:
            print('TOP-CAP',R['S']['G'],'rawL',R['raw_L'],'cap_credit',R['free_cap_credit'],'Lcap',R['Lcap'])
            if 'weighted_returns' in R:
                T=R['weighted_returns'];print('WEIGHTED-RETURN','net_credit',T['net_cap_credit'],'improvedL',T['improved_L'])
            if 'shadow_comparisons' in R:print('NET-SHADOWS',R['shadow_comparisons'])
        print('FOUR cached controls plus ONE cap-transfer falsifier; no semigroup search or universal sign claim')
        sys.exit(0)
    if sys.argv[1]=='--pointwise-death-check':
        import subprocess
        G=list(map(int,sys.argv[4:]));assert G
        C=json.loads(subprocess.check_output([sys.argv[2],'--odd-audit',*map(str,G)],text=True))
        result=audit_pointwise_death(C)
        with open(sys.argv[3],'w') as out:json.dump(result,out,indent=2)
        print('POINTWISE-DEATH',{k:v for k,v in result.items() if k not in ('columns','fixed_trade_control')})
        if 'fixed_trade_control' in result:
            print('FIXED-TRADE',{k:v for k,v in result['fixed_trade_control'].items() if k!='packing'})
        print('ONE fixed input; no family census or universal sign claim')
        sys.exit(0)
    if sys.argv[1]=='--advisor-filtration-check':
        import subprocess
        result=[]
        for G in ([13,15,47],[19,39,41,50,52,53],[15,17,53,55]):
            C=json.loads(subprocess.check_output([sys.argv[2],'--odd-audit',*map(str,G)],text=True))
            result.append(audit_odd_filtration(C))
        assert result[0]['associated_graded_Hilbert_function']==[1,2,3,4,2,1]
        assert result[1]['associated_graded_Hilbert_function']==[6,7,6]
        assert result[2]['shared_first_death']['capacity_needed']==11
        with open(sys.argv[3],'w') as out:json.dump(result,out,indent=2)
        for R in result:print('ODD-FILTRATION',{k:v for k,v in R.items() if k!='associated_graded_value_bases'})
        print('EXACTLY AUDITED two old algebra controls and ONE mechanism-family member; no finite-sign theorem')
        sys.exit(0)
    if sys.argv[1]=='--parity-credit-check':
        import subprocess
        result=[]
        for G in ([6,7,11],[19,39,41,50,52,53],[13,15,17,19]):
            C=json.loads(subprocess.check_output([sys.argv[2],'--odd-audit',*map(str,G)],text=True))
            result.append(audit_parity_credit(C))
        control=result[0]
        assert control['naive_unweighted_bound']==6>control['S']['W']==control['corrected_weighted_bound']==4
        assert {'parent_value':17,'child_value':23,'primitive':6,'parent_mu':0,'child_mu':0} in control['zero_drop_steps']
        sharp=result[1]
        assert sharp['unique_parents'] and sharp['primitive_credit']==sharp['maximum_primitive_credit']==319
        assert sharp['best_reserve_free_numerator']==-924 and sharp['full_scaled_W']==3*19*32
        with open(sys.argv[3],'w') as out:json.dump(result,out,indent=2)
        for R in result:print('PARITY-CREDIT',R)
        print('EXACTLY AUDITED three fixed inputs; no universal finite-gain claim')
        sys.exit(0)
    if sys.argv[1]=='--advisor-parity-check':
        import subprocess
        parity=[]
        for G in ([13,15,17,19],[5,7],[19,39,41,50,52,53]):
            C=json.loads(subprocess.check_output([sys.argv[2],'--odd-audit',*map(str,G)],text=True))
            parity.append(audit_source_parity(C))
        source=json.loads(subprocess.check_output([sys.argv[2],'--axis-seed','13','15','17','19'],text=True))
        audit(source);support=support_geometry(source)
        raw_support=json.loads(subprocess.check_output([sys.argv[2],'--supp-audit','13','15','17','19'],text=True))
        assert all(raw_support[k]==support[k] for k in raw_support)
        assert (source['c'],source['g'],source['W'])==(64,36,48)
        assert parity[0]['scalar_layer_dimensions']==[6,6,3,3]
        assert support['Dep']==14 and support['support_sum']==5
        old={tuple(sorted(C['seed']['generators'])):C for C in
             (json.loads(line) for line in open_text(sys.argv[4]) if line.strip())}
        cuts=[]
        for line in open_text(sys.argv[3]):
            if not line.strip():continue
            D=json.loads(line)['seed'];key=tuple(sorted(D['generators']))
            selections=[('whole',list(range(D['m']))),('old_selected',old[key]['cut']['kept'])]
            if key==(40,41,42,43):selections.append(('old_leak_control',[0,factor_basis(D)[0][0]]))
            for label,E in selections:
                if len(E)<2:continue
                Q=partial_support_geometry(D,E);FZ=frozen_payment_geometry(D,E);forest=exterior_forest_geometry(D,E,True)
                reserve=FZ['nonwrap_leakage']+D['m']-FZ['pool_size']
                assert Q['budget']==forest['joint_margin']+reserve
                if label=='whole':assert FZ['nonwrap_leakage']==0
                cuts.append({'G':list(key),'cut':label,'size':len(E),'original_completion_budget':Q['budget'],
                    'frozen_margin':forest['joint_margin'],'leak_reserve':FZ['nonwrap_leakage'],
                    'unused_residue_reserve':D['m']-FZ['pool_size'],'forest_paid':forest['paid'],
                    'cycle_rank':forest['cycle_rank']})
        R={'parity_algebras':parity,'advisor_k2_support':support,'Hall_reserves':cuts}
        with open(sys.argv[5],'w') as out:json.dump(R,out,indent=2)
        for V in parity:print('PARITY-ALGEBRA',{k:v for k,v in V.items() if k not in ('value_basis','odd_product_value_bases','nonzero_odd_products')})
        print('ADVISOR-K2-SUPPORT',support)
        for V in cuts:print('HALL-RESERVES',V)
        print('EXACTLY AUDITED advisor calibration, original-source products and old-cut reserves; no new sign theorem')
        sys.exit(0)
    if sys.argv[1]=='--differential-check':
        result=[]
        for path in sys.argv[2:-1]:
            with open(path) as source:result.append(audit_differential(json.load(source)))
        with open(sys.argv[-1],'w') as out:json.dump(result,out,indent=2)
        for R in result:print('DIFFERENTIAL',R)
        print('EXACTLY AUDITED three fixed semigroups and rational trade ranks; no universal sign claim')
        sys.exit(0)
    if sys.argv[1]=='--odd-layer-check':
        import subprocess
        records=[json.loads(line) for line in open(sys.argv[2]) if line.startswith('{')]
        cases={tuple(sorted(C['G'])) for C in records}
        cases.update(((5,7),(6,7,11),(5,21,22,23,24)))
        result=[]
        for G in sorted(cases):
            C=json.loads(subprocess.check_output([sys.argv[3],'--odd-audit',*map(str,G)],text=True))
            result.append(audit_odd_layers(C))
        with open(sys.argv[4],'w') as out:json.dump(result,out,indent=2)
        for R in result:print('ODD-LAYERS',R)
        control=next(R for R in result if R['S']['G']==[5,7])
        assert control['Hilbert_function']==[1,2,2,1,1]
        assert {'degree':1,'paired_T_element':7,'x':1,'image':8} in control['paired_quotient_actions']
        witness=next(R for R in result if R['S']['G']==[5,21,22,23,24])
        assert witness['S']['W']==0 and witness['U']['W']==2
        print('EXACTLY AUDITED five fixed cases; no new search or universal payment claim')
        sys.exit(0)
    if sys.argv[1]=='--odd-closure-check':
        import subprocess
        records=[]
        for line in open(sys.argv[2]):
            if line.startswith('{'):records.append(json.loads(line))
        unique={tuple(sorted(C['G'])):C for C in records};results=[]
        for G,C in unique.items():
            fresh=json.loads(subprocess.check_output([sys.argv[3],'--odd-audit',*map(str,G)],text=True))
            assert fresh==C
            results.append(audit_odd_comparison(C))
        for G in ([5,7],[6,7,11]):
            C=json.loads(subprocess.check_output([sys.argv[3],'--odd-audit',*map(str,G)],text=True))
            results.append(audit_odd_comparison(C))
        assert len(records)==3 and len(unique)==2
        assert any(R['S']['G']==[19,39,41,50,52,53] and R['S']['W']==32 and R['U']['W']==23 for R in results)
        report={'search_json_records':len(records),'distinct_search_cases':len(unique),
                'controls':2,'records':results,'bounded_search_found_failure':any(R['margin']<0 for R in results[:len(unique)])}
        with open(sys.argv[4],'w') as out:json.dump(report,out,indent=2)
        for R in results:print('ODD-CLOSURE',R)
        print('EXACTLY AUDITED two saved search cases and two boundary controls; no universal monotonicity claim')
        sys.exit(0)
    if sys.argv[1]=='--quotient-descent-check':
        R=audit_quotient_descent(sys.argv[2])
        with open(sys.argv[3],'w') as out:json.dump(R,out,indent=2)
        for V in R['common_divisor_descents']:print('QUOTIENT-DESCENT',V)
        for V in R['parity_obstructions']:print('PARITY-OBSTRUCTION',V)
        print('CLOSED-BASE-DISCRIMINATOR',R['closed_BASE_discriminator']['phase_support_bound'])
        print('EXACTLY AUDITED four descents, two false monotone-payer witnesses and one stopped BASE diagnostic')
        sys.exit(0)
    if sys.argv[1]=='--exterior-forest-check':
        old={tuple(sorted(C['seed']['generators'])):C for C in
             (json.loads(line) for line in open_text(sys.argv[2]) if line.strip())}
        selected=[(19,39,41,50,52,53),(40,41,42,43),(114,305,307,310)];results=[];all_alias_results=[]
        for key in selected:
            C=old[key];audit_completion_cut(C)
            results.append(exterior_forest_geometry(C['seed'],C['cut']['kept']))
            all_alias_results.append(exterior_forest_geometry(C['seed'],C['cut']['kept'],True))
        with open(sys.argv[3]) as source:local=audit_mstd_two_edge_exchange(json.load(source))
        with open(sys.argv[4],'w') as out:json.dump({'cuts':results,'all_alias_cuts':all_alias_results,'MSTD_two_edge_repair':local},out,indent=2)
        for R in results+all_alias_results:print('ALIAS-FOREST',{k:v for k,v in R.items() if k not in ('edges','assignments','unpaid_edges')})
        print('MSTD-TWO-EDGE-REPAIR',local)
        print('EXACTLY AUDITED three saved cuts and one two-edge exchange; no universal sign claim')
        sys.exit(0)
    if sys.argv[1]=='--mstd-shadow-check':
        with open_text(sys.argv[2]) as source:R=audit_mstd_shadow(json.load(source))
        with open(sys.argv[3],'w') as out:json.dump(R,out,indent=2)
        print('MSTD-SHADOW',R)
        if R['genuine_negative_W']:print('GENUINE NEGATIVE W: independent membership audit passed',R)
        print('EXACTLY AUDITED one constructed failure of a staged claim; no Wilf failure inferred')
        sys.exit(0)
    if sys.argv[1]=='--joint-defect-check':
        old={tuple(sorted(C['seed']['generators'])):C for C in
             (json.loads(line) for line in open_text(sys.argv[3]) if line.strip())}
        results=[]
        for line in open_text(sys.argv[2]):
            if not line.strip():continue
            C=json.loads(line);D=C['seed'];key=tuple(sorted(D['generators']))
            assert C['cut']['frozen_nonwrap'];audit_completion_pool_cut(C);audit_completion_cut(old[key])
            R={'G':list(key),'actual_W':D['W'],'whole_tile':joint_defect_geometry(D,range(D['m'])),
               'old_selected_cut':joint_defect_geometry(D,old[key]['cut']['kept'])}
            if list(key)==[40,41,42,43]:
                R['zero_resource_controls']=[joint_defect_geometry(D,{0,1}),joint_defect_geometry(D,{0,1,2,3})]
                assert all(V['zero_resource'] and V['joint_margin']==0 for V in R['zero_resource_controls'])
            results.append(R)
        assert len(results)==3 and {tuple(R['G']) for R in results}=={
            (19,39,41,50,52,53),(40,41,42,43),(114,305,307,310)}
        with open(sys.argv[4],'w') as out:json.dump(results,out,indent=2)
        for R in results:
            for label in ('whole_tile','old_selected_cut'):
                print('JOINT-DEFECT',R['G'],label,{k:v for k,v in R[label].items() if k not in
                      ('internal_slot_witnesses','selected_maximal_columns','outside_groups')})
        print('EXACTLY AUDITED three existing tiles and old cuts; no new optimizer or universal sign claim')
        sys.exit(0)
    if sys.argv[1]=='--completion-pool-check':
        results=[audit_completion_pool_cut(json.loads(line)) for line in open_text(sys.argv[2]) if line.strip()]
        with open(sys.argv[3],'w') as out:json.dump(results,out,indent=2)
        for R in results:
            print('COMPLETION-POOL',R)
            if R['genuine_negative_W']:print('GENUINE NEGATIVE W: independent membership audit passed',R)
        print('EXACTLY CERTIFIED',len(results),'pool / fixed-allocation minima; a negative model budget is not a Wilf failure')
        sys.exit(0)
    if sys.argv[1]=='--completion-structure-check':
        # Reuse the 114 witness, a boundary control and two falsifications of
        # interior-only payment. This does not enlarge the closed fixture list.
        wanted={(114,305,307,310),(13,17),(40,41,42,43),(62,87,88,89)};results=[]
        for line in open_text(sys.argv[2]):
            C=json.loads(line)
            if tuple(sorted(C['seed']['generators'])) in wanted:
                results.append(audit_completion_structure(C))
        assert {tuple(sorted(R['G'])) for R in results}==wanted
        with open(sys.argv[3],'w') as out:json.dump(results,out,indent=2)
        for R in results:
            print('COMPLETION-STRUCTURE', {k:v for k,v in R.items() if k not in ('phase_deficiencies','maximal_cells','cut_cells')})
            print('MAXIMAL-CELL TESTS',R['maximal_cells'])
        print('EXACTLY AUDITED critical-cut and cyclic-phase identities; no universal sign claim')
        sys.exit(0)
    if sys.argv[1] in ('--completion-cut-check','--partial-support-check'):
        check=audit_completion_cut if sys.argv[1]=='--completion-cut-check' else audit_partial_support
        results=[check(json.loads(line)) for line in open_text(sys.argv[2]) if line.strip()]
        with open(sys.argv[3],'w') as out:json.dump(results,out,indent=2)
        for R in results:print(sys.argv[1],R)
        for R in results:
            if R.get('genuine_negative_W'):print('GENUINE NEGATIVE W: independent membership audit passed',R)
        print('EXACTLY CERTIFIED',len(results),'global down-set minima' if sys.argv[1]=='--completion-cut-check' else 'selected partial-tile witnesses','; no universal sign claim')
        sys.exit(0)
    if sys.argv[1] in ('--residue-check','--tangent-check'):
        check=audit_residue_comparison if sys.argv[1]=='--residue-check' else audit_primitive_tangent
        results=[check(json.loads(line)) for line in open_text(sys.argv[2]) if line.strip()]
        with open(sys.argv[3],'w') as out:json.dump(results,out,indent=2)
        for R in results:print(sys.argv[1],R)
        print('EXACTLY AUDITED',len(results),'residue comparisons' if sys.argv[1]=='--residue-check' else 'primitive tangent realizations')
        sys.exit(0)
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
