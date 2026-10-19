/* Exhaustive check of the ambient packing statement SP_C (codex "Ambient SP12" for C = 12; lead LSP* for C = 13.5):
   for every set B of n integers in an interval of s consecutive integers with all unordered pair sums (loops
   included) distinct,   3s - 2 >= H(n) - C*ex,   H(n) = n(C(n,2)+1),  ex = C(n+2,3) - #distinct triple sums.
   Sets are translated to min 0; only s with 3s-2 < H(n) matter.  DFS adds elements in increasing order; the
   partial excess never decreases and the final s >= b_last + 1 + (elements still to place), so a branch is pruned
   as soon as 3*s_min - 2 >= H - C*ex_partial.  C is given as a rational Cnum/Cden.
   Reports the number of complete sets reached, the minimum slack (3s-2) - (H - C*ex) and a witness.
   usage: sp_c_check n Cnum Cden
   RATIO build (-DRATIO): no pruning by C; over all sets with 3s-2 < H(n) report the maximum of (H-(3s-2))/ex
   (the least constant C for which SP_C holds at this n) and a witness. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, smax, b[24]; static long Cn, Cd, H;
static unsigned char ps[1024]; static int tc[2048]; static long ex; static long leaves, nodes; static long best=1L<<60; static int wit[24], wex, ws;
static long rnum=0, rden=1, zerofail=0;
static long Hn(long k){ return k*(k*(k-1)/2+1); }
static void addx(int k,int x,int sgn){ /* add/remove all triples containing x (x is element k) */
  int v; if(sgn>0){
    v=3*x; if(tc[v]++) ex++;
    for(int i=0;i<k;i++){ v=2*x+b[i]; if(tc[v]++) ex++; }
    for(int i=0;i<k;i++) for(int j=i;j<k;j++){ v=x+b[i]+b[j]; if(tc[v]++) ex++; }
  } else {
    v=3*x; if(--tc[v]) ex--;
    for(int i=0;i<k;i++){ v=2*x+b[i]; if(--tc[v]) ex--; }
    for(int i=0;i<k;i++) for(int j=i;j<k;j++){ v=x+b[i]+b[j]; if(--tc[v]) ex--; }
  } }
static void rec(int k){
  nodes++;
  if(k==n){ leaves++; int s=b[n-1]+1;
#ifdef RATIO
    { long num=H-(3L*s-2); if(ex==0){ if(num>0) zerofail++; } else if(num*rden>rnum*ex){ rnum=num; rden=ex; memcpy(wit,b,sizeof(int)*n); wex=(int)ex; ws=s; } }
#endif
    long sl=Cd*(3L*s-2)-(Cd*H-Cn*ex); if(sl<best){ best=sl; memcpy(wit,b,sizeof(int)*n); wex=(int)ex; ws=s; } return; }
  for(int x=b[k-1]+1;x<=smax-1-(n-1-k);x++){
    int smin=x+1+(n-1-k);
    /* prune: even with no further collisions this branch cannot violate */
    int ok=1; for(int i=0;i<k&&ok;i++) if(ps[b[i]+x]) ok=0; if(ok&&ps[2*x]) ok=0; if(!ok) continue;
    for(int i=0;i<k;i++) ps[b[i]+x]=1; ps[2*x]=1;
    addx(k,x,+1); b[k]=x;
    if(Cd*(3L*smin-2) < Cd*H-Cn*ex || k+1==n) rec(k+1);
    addx(k,x,-1);
    for(int i=0;i<k;i++) ps[b[i]+x]=0; ps[2*x]=0; } }
int main(int argc,char**argv){ n=atoi(argv[1]); Cn=atol(argv[2]); Cd=atol(argv[3]); H=Hn(n);
  smax=1; while(3*(smax+1)-2<H) smax++;   /* largest s with 3s-2 < H */
  memset(ps,0,sizeof ps); memset(tc,0,sizeof tc); ex=0; b[0]=0; ps[0]=1; addx(0,0,+1); rec(1);
  printf("n=%d C=%ld/%ld H=%ld s<=%d  nodes=%ld leaves(complete, unpruned)=%ld  ",n,Cn,Cd,H,smax,nodes,leaves);
  if(leaves){ printf("min slack*Cden=%ld (slack=%.2f) witness s=%d ex=%d:",best,(double)best/Cd,ws,wex); for(int i=0;i<n;i++) printf(" %d",wit[i]); }
#ifdef RATIO
  printf("\n  RATIO: max (H-(3s-2))/ex = %ld/%ld = %.4f  zero-excess violations=%ld  witness s=%d ex=%d:",rnum,rden,(double)rnum/rden,zerofail,ws,wex); for(int i=0;i<n;i++) printf(" %d",wit[i]);
#endif
  printf("%s\n",(leaves&&best<0)?"  FAIL":"  (no violation)"); return 0; }
