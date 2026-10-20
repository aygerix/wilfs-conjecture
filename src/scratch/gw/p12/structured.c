/* P12 adversarial structured search. Usage: structured mlo mhi mode. */
#include "rest.h"
static unsigned long long nall,nclass,neq,nsparse;static double best=-1e100;static Stats bs;static ll bw[MM];
static void test(int m,int ng,ll *g,const char *tag) {
    ll w[MM];Stats s;nall++;
    if(!apery(m,ng,g,w)||!stats(m,w,&s)||s.d<2||s.M<3*s.n1)return;
    nclass++;if(3*(s.d+1)<m)nsparse++;
    double x=(double)s.rest/s.C2;
    if(x>best){best=x;bs=s;memcpy(bw,w,m*sizeof(ll));dump(tag,&s,w);}
    if(s.rest>0){dump("COUNTEREXAMPLE",&s,w);exit(2);}if(!s.rest)neq++;
}
static uint64_t rng=UINT64_C(918276521);
static unsigned rnd(unsigned n){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng%n;}
int main(int argc,char **argv) {
    int lo=argc>1?atoi(argv[1]):4, hi=argc>2?atoi(argv[2]):100, mode=argc>3?atoi(argv[3]):0;
    ll g[MM];
    for(int m=lo;m<=hi;m++){
        if(mode==0) { /* Dense interval cores plus a small generator: directed grid. */
            for(int lev=1;lev<=4;lev++)for(int a=1;a<m;a++)for(int width=1;width<m-a;width++){
                int b=a+width;if(width>8 && (width%3))continue;
                int ng=0;for(int j=a;j<=b;j++)g[ng++]=(ll)lev*m+j;
                for(int z=1;z<=m/3;z++){
                    if(z>8 && z%5)continue;g[ng]=(ll)m+z;test(m,ng+1,g,"INTERVAL");
                }
            }
        } else if(mode==1) { /* All three-generator choices in an explicit box. */
            for(ll a=m+1;a<=4*m;a++)for(ll b=a+1;b<=6*m;b++){
                g[0]=a;g[1]=b;test(m,2,g,"E3");
            }
        } else if(mode==2) { /* Near-T truncations, small low-dimensional cores. */
            for(int lev=3;lev<=7;lev++)for(int z=1;z<m;z++)for(int off=0;off<m;off+=m<30?1:3){
                int K=lev*m+off;int ng=0;g[ng++]=m+z;
                if(z+1<m)g[ng++]=m+z+1;
                for(int i=0;i<m;i++)g[ng++]=K+i;
                test(m,ng,g,"TRUNC");
            }
        } else { /* Projected boxes, near AP with outliers, postage stamps. */
            for(int z=0;z<20000;z++){
                int ng=2+rnd(12);for(int j=0;j<ng;j++)g[j]=m+1+rnd(6*m);
                if(z%3==0){int a=1+rnd(m-1),d=1+rnd(m/4+1),lev=1+rnd(3);for(int j=0;j<ng-1;j++)g[j]=(ll)lev*m+a+j*d;}
                if(z%3==1){int a=1+rnd(m-1),b=1+rnd(m-1);for(int j=0;j<ng-1;j++)g[j]=m+(a*(j%3)+b*(j/3))%m;}
                test(m,ng,g,"RANDOM");
            }
        }
        fprintf(stderr,"DONE m=%d tested=%llu class=%llu sparse=%llu maxREST/C2=%.12f\n",m,nall,nclass,nsparse,best);fflush(stderr);
    }
    printf("SUMMARY tested=%llu class=%llu sparse=%llu equal=%llu maxREST/C2=%.12f\n",nall,nclass,nsparse,neq,best);if(nclass)dump("BEST",&bs,bw);
}
