/* Abstract Cauchy-Davenport model (prime m).  Layer counts A_0=1 <= A_1 <= ... with
   (CD)  A_{i+j+1} >= min(m, A_i + A_j - 1);
   (GEN) new residues at layer j: A_j - A_{j-1} <= g_j + h_j,  h_j <= max(0, min(m, sum_{i=1}^{floor(j/2)} A_i A_{j-i}) - A_{j-1}),  h_1 = 0;
   (END) A_j <= m-1 for j < K (full layers below c), A_K <= m, A_{K+1} = m.
   d = sum_j g_j (minimal), e = d+1.  Worst conductor: if A_K = m, c = Km, ell = sum_{j<K} A_j;
   else c = (K+1)m - A_K + 1, ell = sum_{j<K} A_j + 1.   Report min (e*ell - c) over models with e < m/3 (when RESTRICT)
   and c > 3m.  usage: acd m Kmax RESTRICT */
#include <stdio.h>
#include <stdlib.h>
static int m, K, R; static int A[64]; static long best; static int bestA[64], bestK, bestd; static long nodes;
static void rec(int j,int used,int dmax){
  nodes++;
  if(j==K+2){ /* evaluate */
    long sum=0; for(int t=0;t<K;t++) sum+=A[t]; long c,ell; if(A[K]==m){ c=(long)K*m; ell=sum; } else { c=(long)(K+1)*m-A[K]+1; ell=sum+1; }
    if(c<=3L*m) return; int e=used+1; if(R && 3*e>=m) return; long W=(long)e*ell-c;
    if(W<best){ best=W; for(int t=0;t<=K+1;t++) bestA[t]=A[t]; bestK=K; bestd=used; }
    return; }
  int lo=A[j-1]; for(int i=0;i<=j-1;i++){ int k=j-1-i; if(k<0||k>j-1) continue; int v=A[i]+A[k]-1; if(v>m) v=m; if(v>lo) lo=v; }
  int hi = (j<K)? m-1 : m; if(j==K+1) lo=hi=m;
  long prod=0; for(int i=1;i<=j/2;i++) prod+=(long)A[i]*A[j-i]; long hmax= (j==1)?0:((prod<m?prod:m)-A[j-1]); if(hmax<0) hmax=0;
  for(int v=lo; v<=hi; v++){ long need=v-A[j-1]-hmax; if(need<0) need=0; if(used+need>dmax) break; A[j]=v; rec(j+1,used+(int)need,dmax); }
}
int main(int argc,char**argv){ m=atoi(argv[1]); int Kmax=atoi(argv[2]); R=atoi(argv[3]); int dmax=R?(m-1)/3-1:m-1; if(dmax<1) dmax=1;
  for(K=3;K<=Kmax;K++){ best=1L<<40; nodes=0; A[0]=1; rec(1,0,dmax);
    if(best<(1L<<40)){ printf("m=%d K=%d: min W = %ld (d=%d) A:",m,K,best,bestd); for(int t=0;t<=bestK+1;t++) printf(" %d",bestA[t]); printf("  nodes=%ld\n",nodes); }
    else printf("m=%d K=%d: no feasible model (nodes=%ld)\n",m,K,nodes); fflush(stdout); }
  return 0; }
