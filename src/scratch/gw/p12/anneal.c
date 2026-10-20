/* Hard-constraint Kunz annealing for REST. Usage: anneal m starts steps seed. */
#include "rest.h"
#include <math.h>
static uint64_t state=UINT64_C(983257325);
static uint64_t rand64(void){state^=state<<13;state^=state>>7;state^=state<<17;return state;}
static unsigned rn(unsigned n){return rand64()%n;}
static double unif(void){return (rand64()>>11)*0x1.0p-53;}
static int valid_change(int m,ll *w,int t) {
    if(w[t]<m+t)return 0;
    for(int j=1;j<m;j++){
        if(w[t]+w[j]<w[(t+j)%m])return 0;
        int k=(t-j+m)%m;
        if(w[j]+w[k]<w[t])return 0;
    }return 1;
}
int main(int argc,char **argv){
    int m=argc>1?atoi(argv[1]):60, starts=argc>2?atoi(argv[2]):40, steps=argc>3?atoi(argv[3]):100000;
    if(argc>4)state=strtoull(argv[4],0,10);
    ll w[MM],bw[MM],g[MM];Stats s,cs,bs;ll best=LLONG_MIN;unsigned long long tested=0,valid=0,inclass=0,accepted=0;
    for(int run=0;run<starts;run++){
        int ready=0;
        for(int tries=0;!ready&&tries<10000;tries++){
            int ng=2+rn(8);g[0]=m+1+rn(m/4+1);
            for(int j=1;j<ng;j++)g[j]=(1+rn(4))*m+1+rn(m-1);
            if(run%3==0){int K=(3+rn(3))*m;for(int j=0;j<m;j++)g[j+ng]=K+j;ng+=m;}
            if(apery(m,ng,g,w)&&stats(m,w,&s)&&s.d>=2&&s.M>=3*s.n1)ready=1;
        }
        if(!ready){fprintf(stderr,"NO SEED\n");return 3;}
        for(int it=0;it<steps;it++){
            tested++;int t=1+rn(m-1);ll old=w[t];int jump=(rn(20)==0?2:1)*(rn(2)?1:-1);w[t]+=(ll)jump*m;
            if(w[t]>100LL*m||!valid_change(m,w,t)){w[t]=old;continue;}valid++;
            if(!stats(m,w,&cs)||cs.d<2||cs.M<3*cs.n1){w[t]=old;continue;}inclass++;
            double temp=(.00003+.03*pow(1.0-(double)it/steps,2))*m*(m-1)/2;
            ll diff=cs.rest-s.rest;
            if(diff>=0||unif()<exp((double)diff/temp)){s=cs;accepted++;}else {w[t]=old;continue;}
            if(s.rest>best){best=s.rest;bs=s;memcpy(bw,w,m*sizeof(ll));dump("RECORD",&s,w);}
            if(s.rest>0){dump("COUNTEREXAMPLE",&s,w);return 2;}
        }
        fprintf(stderr,"RUN %d tested=%llu valid=%llu class=%llu accepted=%llu best=%lld ratio=%.12f\n",run+1,tested,valid,inclass,accepted,best,(double)best/s.C2);fflush(stderr);
    }
    printf("SUMMARY m=%d starts=%d steps=%d tested=%llu valid=%llu class=%llu accepted=%llu\n",m,starts,steps,tested,valid,inclass,accepted);dump("BEST",&bs,bw);
}
