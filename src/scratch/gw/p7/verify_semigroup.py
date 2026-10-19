"""Verify the phase-adjusted semigroup realization using its full Apéry table.

For every core generator, test all m shortest-path inequalities with integers.
For spike generators, inequalities at nonzero residues follow from the checked
global weight bound; the zero-residue equalities are checked individually.
Also check every generator is irreducible, conductor, genus and Wilf slack.
Usage: python verify_semigroup.py results/sidon_counter2.json
"""
import json
import sys
import numpy as np


def main():
    with open(sys.argv[1]) as f:z=json.load(f)
    m=z['m'];P=np.array(z['P'],dtype=np.int64);k=len(P)
    theta=z['theta'];c=3*m+theta
    n=P+m
    ap=np.full(m,-1,dtype=np.int64)
    ap[0]=0
    for g in n:ap[g%m]=g
    for i in range(k):
        for j in range(i,k):
            g=int(n[i]+n[j]);assert ap[g%m]<0;ap[g%m]=g
    for inds in z['triple_indices']:
        g=sum(int(n[a]) for a in inds);assert ap[g%m]<0;ap[g%m]=g
    missing=np.array(z['spike_labels'],dtype=np.int64)
    spikes=np.where(missing<theta,4*m+missing,3*m+missing)
    assert np.all(ap[missing]<0)
    ap[missing]=spikes
    assert np.all(ap>=0)
    assert np.all(ap%m==np.arange(m,dtype=np.int64))
    assert int(ap.max())==c+m-1
    assert int(ap[(c-1)%m])==c+m-1
    # Every proposed value has the displayed factorization.  The inequalities
    # below prove all words in the generators are at least their proposed value.
    idx=np.arange(m,dtype=np.int64)
    checks=0
    min_slack=None
    for g in n:
        slack=ap+g-ap[(idx+g)%m]
        assert np.all(slack>=0)
        min_slack=int(slack.min()) if min_slack is None else min(min_slack,int(slack.min()))
        checks+=m
    nonzero_min=int(ap[1:].min())
    assert int(spikes.min())+nonzero_min>int(ap.max())
    assert np.all(ap[spikes%m]==spikes)
    checks+=len(spikes)*m
    # Irreducibility: m and the core generators are below 2m.  For a spike,
    # subtraction of m fails; subtraction of every core generator is checked.
    # Two distinct spikes differ by less than m, so no other spike divides it.
    assert int(n.min())>m and int(n.max())<2*m
    assert int(spikes.max()-spikes.min())<m
    assert np.all(spikes-m<ap[(spikes-m)%m])
    irred=0
    for g in n:
        diff=spikes-g
        assert np.all(diff<ap[diff%m])
        irred+=len(spikes)
    genus=int(np.sum(ap//m))
    ell=c-genus
    embedding=1+k+len(spikes)
    wilf=embedding*ell-c
    rho=(-c)%m
    assert rho==z['rho']
    print(json.dumps(dict(verified=True,m=m,embedding_dimension=embedding,
        conductor=c,conductor_mod_m=c%m,rho=rho,genus=genus,ell=ell,
        Wilf_slack=wilf,max_apery=int(ap.max()),min_nonzero_apery=nonzero_min,
        min_spike=int(spikes.min()),max_spike=int(spikes.max()),
        core_shortest_path_checks=k*m,spike_shortest_path_checks_by_bound=len(spikes)*m,
        minimal_generator_checks=irred,phase_matches_counter=True,
        apery_height=3,wrapmax=True),sort_keys=True))


if __name__=='__main__':main()
