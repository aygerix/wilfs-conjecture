/* Exact Apéry-chain statistics. Research computations run on fejer only. */
#ifndef P12_REST_H
#define P12_REST_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#define MM 1024
typedef long long ll;
typedef struct { int m,d; ll M,n1,ellp,rest,con0,delta,C2; ll n[MM],N[MM]; } Stats;
static ll Wsort[MM];
static int cmp_ll(const void *a,const void *b) { ll x=*(const ll*)a,y=*(const ll*)b;return (x>y)-(x<y); }
static int kg[MM];
static int chain_k(int i,int m,ll n,const ll *w) {
    if(kg[i]>=0)return kg[i];
    int j=(i+n)%m;
    return kg[i]=(w[j]==w[i]+n ? 1+chain_k(j,m,n,w):0);
}
static int stats(int m,const ll *w,Stats *s) {
    memset(s,0,sizeof(*s));s->m=m;s->C2=(ll)m*(m-1)/2;
    for(int i=0;i<m;i++){Wsort[i]=w[i];if(w[i]>s->M)s->M=w[i];}
    qsort(Wsort,m,sizeof(ll),cmp_ll);
    for(int i=1;i<m;i++) {
        ll x=Wsort[i]; int comp=0;
        for(int j=0;j<s->d;j++) {
            ll y=x-s->n[j];
            if(y>=0 && w[y%m]==y){comp=1;break;}
        }
        if(!comp)s->n[s->d++]=x;
    }
    if(!s->d)return 0;s->n1=s->n[0];
    for(int i=1;i<m;i++)s->ellp+=(s->M-w[i])/m;
    for(int a=0;a<s->d;a++) {
        ll n=s->n[a];for(int i=0;i<m;i++)kg[i]=-1;
        ll nn=0;for(int i=1;i<m;i++)nn+=chain_k(i,m,n,w);
        s->N[a]=nn;s->rest+=n*nn;
        s->con0+=(ll)chain_k(0,m,n,w)*n-m*(s->M/m);
    }
    s->rest-=(ll)m*s->d*s->ellp;s->delta=s->rest+s->con0;
    return 1;
}
static int apery(int m,int ng,const ll *g,ll *w) {
    int used[MM]={0};if(m>=MM)return 0;
    for(int i=0;i<m;i++)w[i]=LLONG_MAX/8;w[0]=0;
    for(int j=0;j<m;j++) {
        int r=-1;for(int i=0;i<m;i++)if(!used[i]&&(r<0||w[i]<w[r]))r=i;
        if(r<0||w[r]==LLONG_MAX/8)return 0;used[r]=1;
        for(int a=0;a<ng;a++){int t=(r+g[a])%m;if(w[t]>w[r]+g[a])w[t]=w[r]+g[a];}
    }
    return 1;
}
static void dump(const char *tag,const Stats *s,const ll *w) {
    printf("%s m=%d e=%d M=%lld n1=%lld REST=%lld con0=%lld Delta=%lld C2=%lld ellp=%lld gens=[%d",tag,s->m,s->d+1,s->M,s->n1,s->rest,s->con0,s->delta,s->C2,s->ellp,s->m);
    for(int a=0;a<s->d;a++)printf(",%lld",s->n[a]);printf("] N=[");
    for(int a=0;a<s->d;a++)printf("%s%lld",a?",":"",s->N[a]);printf("] Ap=[");
    for(int i=0;i<s->m;i++)printf("%s%lld",i?",":"",w[i]);puts("]");fflush(stdout);
}
#endif
