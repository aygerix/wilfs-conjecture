/* Near-covers with holes (lead, 2026-10-20): anneal k-subsets A of Z/m containing 0 to maximize |A + A| (sums with
   repetition).  Prints every distinct A reaching |A+A| >= TARGET, with its holes and which holes are 3a (a in A\0).
   usage: nearcover m k ITERS RESTARTS SEED TARGET */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
static int m, k, A[64]; static unsigned long long rs;
static unsigned rnd(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (unsigned)(rs >> 11); }
static int cnt[512];
static int cover(void){ memset(cnt,0,sizeof(int)*m); int c=0;
  for(int i=0;i<k;i++) for(int j=i;j<k;j++){ int r=(A[i]+A[j])%m; if(!cnt[r]++) c++; } return c; }
int main(int argc,char**argv){
  m=atoi(argv[1]); k=atoi(argv[2]); long it=atol(argv[3]); int R=atoi(argv[4]); rs=atoll(argv[5])*0x9E3779B97F4A7C15ULL+7; int TG=atoi(argv[6]);
  static unsigned long long seen[100000]; int ns=0, best=0;
  for(int rr=0; rr<R; rr++){
    int used[512]; memset(used,0,sizeof(int)*m); A[0]=0; used[0]=1;
    for(int i=1;i<k;i++){ int v; do v=rnd()%m; while(used[v]); used[v]=1; A[i]=v; }
    int cur=cover();
    for(long t=0;t<it;t++){
      double T = 2.0*(1.0-(double)t/it)+0.02;
      int i=1+rnd()%(k-1), v; do v=rnd()%m; while(used[v]);
      int old=A[i]; A[i]=v; int s=cover();
      if(s>=cur || exp((s-cur)/T) > (rnd()%1000000)/1e6){ used[old]=0; used[v]=1; cur=s; if(cur>best) best=cur;
        if(cur>=TG){ int srt[64]; memcpy(srt,A,sizeof(int)*k);
          for(int a=0;a<k;a++) for(int b=a+1;b<k;b++) if(srt[b]<srt[a]){int z=srt[a];srt[a]=srt[b];srt[b]=z;}
          unsigned long long h=1469598103934665603ULL; for(int a=0;a<k;a++){h^=srt[a]; h*=1099511628211ULL;}
          int dup=0; for(int a=0;a<ns;a++) if(seen[a]==h){dup=1;break;}
          if(!dup && ns<100000){ seen[ns++]=h; cover();
            printf("cov=%d A=",cur); for(int a=0;a<k;a++) printf("%d%s",srt[a],a<k-1?",":"");
            printf(" holes="); for(int r=0;r<m;r++) if(!cnt[r]){ int cube=0; for(int a=1;a<k;a++) if((3*srt[a])%m==r) cube=1; printf("%d%s ",r,cube?"*":""); }
            printf("\n"); fflush(stdout); } } }
      else A[i]=old;
    }
  }
  fprintf(stderr,"m=%d k=%d best cover %d, printed %d\n",m,k,best,ns); return 0;
}
