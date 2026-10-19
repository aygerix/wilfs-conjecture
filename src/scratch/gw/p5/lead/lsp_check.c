/* Exhaustive check of the Local SP lemma (LSP), P5_REPORT section 27:
   n distinct integers in an interval of s consecutive integers, all pair sums (with loops) distinct,
   triple collision excess ex = C(n+2,3) - #distinct triple sums.  Claim: 3s-2 >= H(n) - lambda_n*ex,
   H(n)=n(C(n,2)+1).  Enumerates every such set with min 0 and max <= smax-1, where smax is the
   largest s with 3s-2 < H(n) (beyond it the claim is trivial).  Doubled arithmetic for lambda.
   usage: lsp_check nmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, smax, b[16]; static unsigned char ps[512]; static long cnt; static long minsl; static int wit[16], wex, ws;
static long lam2(long k){ if(k<=1) return 0; if(k==2) return 2; if(k==3) return 4; if(k==4) return 8; return (k%3==0)? 3*k : 3*(k-1); }
static long Hn(long k){ return k*(k*(k-1)/2+1); }
static unsigned short ts[2048];
static void leaf(void){ cnt++; int s=b[n-1]+1; static int stamp=0; stamp++; if(stamp==65535){ memset(ts,0,sizeof ts); stamp=1; }
  int distinct=0, tot=0; for(int i=0;i<n;i++) for(int j=i;j<n;j++) for(int k=j;k<n;k++){ int v=b[i]+b[j]+b[k]; tot++; if(ts[v]!=stamp){ ts[v]=stamp; distinct++; } }
  int ex=tot-distinct; long sl=2L*(3*s-2)-(2*Hn(n)-lam2(n)*ex);
  if(sl<minsl){ minsl=sl; memcpy(wit,b,sizeof(int)*n); wex=ex; ws=s; } }
static void rec(int k){ /* b[0..k-1] placed, pair sums marked */
  if(k==n){ leaf(); return; }
  for(int x=b[k-1]+1;x<=smax-1-(n-1-k);x++){ int ok=1; for(int i=0;i<k&&ok;i++) if(ps[b[i]+x]) ok=0; if(ok&&ps[2*x]) ok=0;
    if(!ok) continue; for(int i=0;i<k;i++) ps[b[i]+x]=1; ps[2*x]=1; b[k]=x; rec(k+1); for(int i=0;i<k;i++) ps[b[i]+x]=0; ps[2*x]=0; } }
int main(int argc,char**argv){ int nmax=atoi(argv[1]);
  for(n=2;n<=nmax;n++){ smax=1; while(3*(smax+1)-2<Hn(n)) smax++; /* all s<=smax have 3s-2<H(n) */
    cnt=0; minsl=1L<<40; memset(ps,0,sizeof ps); b[0]=0; ps[0]=1; rec(1);
    printf("n=%d H=%ld lambda=%.1f  s<=%d  sets=%ld  min doubled slack=%ld",n,Hn(n),lam2(n)/2.0,smax,cnt,cnt?minsl:0);
    if(cnt){ printf("  witness s=%d ex=%d:",ws,wex); for(int i=0;i<n;i++) printf(" %d",wit[i]); }
    printf("%s\n", (cnt&&minsl<0)?"  FAIL":""); fflush(stdout); }
  return 0; }
