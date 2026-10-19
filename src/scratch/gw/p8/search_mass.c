/* Targeted falsification of the deliberately stronger Lplus >= m*t.
   Uses the lead's shape/label mutation machinery unchanged, with a new exact
   cyclic-sum objective. Compile and run only on fejer. K is restricted to 10
   because the included lead enumerator has MAXC=400. */
#define main lead_h3_main
#ifdef P8_REMOTE
#include "lead_anneal_h3.c"
#else
#include "../../h3/anneal_h3.c"
#endif
#undef main

static ll mass(St *st, Ev *ev, int *phase) {
    int dq[12]={0}, psi[MAXC]={0}; ll cf[MAXM]={0};
    for(int i=0;i<nc;i++) if(st->in[i] && deg[i]==2)
        for(int a=0;a<K;a++) dq[a]+=ex[i][a];
    for(int i=0;i<nc;i++) if(st->in[i] && deg[i]==3) {
        int e[12];
        for(int a=0;a<K;a++) if(ex[i][a]) {
            memcpy(e,ex[i],sizeof e);e[a]--;
            int z=find(e);psi[z]+=ex[i][a];
        }
    }
    for(int i=0;i<nc;i++) if(st->in[i]) {
        if(deg[i]==1) {
            int a=0;while(!ex[i][a])a++;
            if(dq[a])cf[st->lab[i]]=ev->d+1-dq[a];
        } else if(deg[i]==2 && psi[i]) cf[st->lab[i]]=ev->d+2-psi[i];
    }
    ll C=0,L=0;for(int r=0;r<m;r++){C+=cf[r];L+=cf[r]*r;}
    ll best=L;*phase=0;
    for(int g=0;g<m;g++){
        if(L<best){best=L;*phase=g;}
        L+=(ll)m*cf[g]-C;
    }
    return best-(ll)m*ev->t;
}

int main(int argc,char **argv){
    if(argc!=6){fprintf(stderr,"usage: search_mass K m seed iters restarts\n");return 1;}
    K=atoi(argv[1]);m=atoi(argv[2]);rs=strtoull(argv[3],0,10)*2654435761ULL+88172645463325252ULL;
    ll iters=atoll(argv[4]);int reps=atoi(argv[5]);
    if(K<3 || K>10 || m<=K || m>=MAXM)return 1;
    build();static St cur,nx,best;Ev ec,en,eb;ll record=1LL<<60;int rphase=0;
    ll evaluations=0;
    for(int rep=0;rep<reps;rep++){
        for(;;){int ok=1;for(int a=0;a<K;a++){
            cur.P[a]=1+rnd()%(m-1);for(int b=0;b<a;b++)if(cur.P[b]==cur.P[a])ok=0;
        }if(ok)break;}
        relabel(&cur);unsigned char old[MAXC];memset(old,0,sizeof old);
        for(int i=0;i<nc;i++)old[i]=(deg[i]<=1)||(urand()<0.8);
        rebuild(&cur,old);ec=eval(&cur);int ph=0;
        if(ec.f<0){dump("STOP-MAXCL-NEGATIVE",&cur,&ec);return 2;}
        ll mc=mass(&cur,&ec,&ph);
        double oc=(double)mc+(double)m*m*((ec.k<5?5-ec.k:0)+(ec.t<2?2-ec.t:0));
        for(ll it=0;it<iters;it++){
            nx=cur;int mv=rnd()%10;
            if(mv<4){int dg=2+rnd()%2,i=byDeg[dg][rnd()%nby[dg]];if(nx.in[i])continue;
                int ok=1;for(int b=0;b<nlo[i];b++)if(!nx.in[lo[i][b]])ok=0;
                if(!ok || nx.own[nx.lab[i]]>=0)continue;nx.in[i]=1;nx.own[nx.lab[i]]=i;
            }else if(mv<8){int dg=2+rnd()%2,i=byDeg[dg][rnd()%nby[dg]];if(!nx.in[i])continue;
                int ok=1;for(int a=0;a<K;a++){int u=up[i][a];if(u>=0 && nx.in[u])ok=0;}
                if(!ok)continue;nx.in[i]=0;nx.own[nx.lab[i]]=-1;
            }else{int a=rnd()%K,lab=1+rnd()%(m-1),ok=1;
                for(int b=0;b<K;b++)if(b!=a && nx.P[b]==lab)ok=0;if(!ok)continue;
                memcpy(old,cur.in,sizeof old);nx.P[a]=lab;relabel(&nx);
                for(int i=0;i<nc;i++)if(ex[i][a] && deg[i]>=2 && urand()<0.5)old[i]=1;
                if(!rebuild(&nx,old))continue;
            }
            en=eval(&nx);evaluations++;int phase;
            if(en.f<0){dump("STOP-MAXCL-NEGATIVE",&nx,&en);return 2;}
            ll mn=mass(&nx,&en,&phase);
            double on=(double)mn+(double)m*m*((en.k<5?5-en.k:0)+(en.t<2?2-en.t:0));
            if(en.k>=5 && en.t>=2 && mn<record){record=mn;best=nx;eb=en;rphase=phase;}
            if(mn<0 && en.k>=5 && en.t>=2){
                printf("MASS-FAIL slack=%lld sigma=%d evaluations=%lld\n",mn,phase,evaluations);
                dump("MASS-WITNESS",&nx,&en);return 0;
            }
            double temp=0.05*m*m*pow(0.3/(0.05*m*m),(double)it/iters);
            if(on<=oc || urand()<exp((oc-on)/temp)){cur=nx;ec=en;mc=mn;oc=on;}
        }
    }
    printf("DONE evaluations=%lld mass_min=%lld mass_sigma=%d\n",evaluations,record,rphase);
    if(record<(1LL<<60))dump("MASS-BEST",&best,&eb);
    return 0;
}
