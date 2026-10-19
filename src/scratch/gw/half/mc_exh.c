/* Exhaustive down-sets D in N^d of size exactly m (reverse search: parent = remove lex-largest corner).
   For every weight vector n in (m, WMAX]^d: check MC_i (top-min(d,t) corners) for i=1..IMAX (residue-free),
   and, if v is residue-complete mod m, MC_i for all i<=K.  Report only instances with t > d (else implied).
   usage: mc_exh d m WMAX IMAX */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXC 32
static int d,m,WMAX,IMAX; static int C[MAXC][4]; static int nc;
static long cnt_ds=0, rf_tests[16], rf_fail[16], rc_tests=0, rc_fail=0, gw_rf_fail=0;
static int incell(int*x){ for(int c=0;c<nc;c++){ int ok=1; for(int a=0;a<d;a++) if(C[c][a]!=x[a]){ok=0;break;} if(ok) return 1;} return 0; }
static int lexcmp(int*x,int*y){ for(int a=0;a<d;a++){ if(x[a]!=y[a]) return x[a]<y[a]?-1:1; } return 0; }
static int iscorner(int c){ for(int a=0;a<d;a++){ int x[4]; memcpy(x,C[c],sizeof x); x[a]++; if(incell(x)) return 0; } return 1; }
static int cmpd(const void*a,const void*b){ long x=*(long*)a,y=*(long*)b; return x>y?-1:x<y; }
static long fl(long a,long b){ return a>=0? a/b : -((-a+b-1)/b); }
static void evaluate(void){
  cnt_ds++;
  int cor[MAXC], t=0; for(int c=0;c<nc;c++) if(iscorner(c)) cor[t++]=c;
  if(t<=d) return;
  int n[4]; for(int a=0;a<d;a++) n[a]=m+1;
  while(1){
    long v[MAXC]; long M=0; for(int c=0;c<nc;c++){ long s=0; for(int a=0;a<d;a++) s+=(long)C[c][a]*n[a]; v[c]=s; if(s>M) M=s; }
    long V[MAXC]; for(int k=0;k<t;k++) V[k]=v[cor[k]]; qsort(V,t,sizeof(long),cmpd);
    int K=M/m;
    char seen[64]={0}; int rc=1; for(int c=0;c<nc;c++){ if(seen[v[c]%m]) {rc=0;break;} seen[v[c]%m]=1; }
    int imax=rc?K:(IMAX<K?IMAX:K);
    for(int i=1;i<=imax;i++){ long L=0,R=0; for(int c=0;c<nc;c++){ long k1=v[c]/m; L+=k1<i?k1:i; for(int k=0;k<d;k++){ long l1=fl(V[k]-v[c],m); if(l1<0) l1=0; R+=l1<i?l1:i; } }
      if(rc){ if(i==K){ rc_tests++; } if(L>R){ rc_fail++; if(rc_fail<=5){ printf("RC FAIL i=%d m=%d n=",i,m); for(int a=0;a<d;a++) printf("%d,",n[a]); printf("\n"); } break; } }
      if(!rc || i<=IMAX){ if(i<16){ rf_tests[i]++; if(L>R){ rf_fail[i]++; if(rf_fail[i]<=3 && i<=2){ printf("RF FAIL i=%d m=%d d=%d t=%d n=",i,m,d,t); for(int a=0;a<d;a++) printf("%d,",n[a]); printf(" cells:"); for(int c=0;c<nc;c++){ printf(" ("); for(int a=0;a<d;a++) printf("%d",C[c][a]); printf(")"); } printf("\n"); } } } }
    }
    { long g=0,l=0; for(int c=0;c<nc;c++){ g+=v[c]/m; l+=(M-v[c])/m; } if(g>(long)d*l) gw_rf_fail++; }
    int a=0; while(a<d && n[a]==WMAX){ n[a]=m+1; a++; } if(a==d) break; n[a]++;
  }
}
static void rec(void){
  if(nc==m){ evaluate(); return; }
  /* candidate addable cells: x = C[c]+e_a not in D, all lower covers in D */
  int cand[MAXC*4][4]; int ncand=0;
  for(int c=0;c<nc;c++) for(int a=0;a<d;a++){ int x[4]={0}; memcpy(x,C[c],sizeof(int)*d); x[a]++; if(incell(x)) continue;
    int ok=1; for(int b=0;b<d&&ok;b++) if(x[b]>0){ x[b]--; if(!incell(x)) ok=0; x[b]++; }
    if(!ok) continue; int dup=0; for(int k=0;k<ncand;k++) if(!lexcmp(cand[k],x)) dup=1; if(dup) continue; memcpy(cand[ncand++],x,sizeof x); }
  for(int k=0;k<ncand;k++){ int*x=cand[k];
    /* x must be lex-largest corner of D+x: corners of D not below x */
    memcpy(C[nc],x,sizeof(int)*4); nc++;
    int ok=1; for(int c=0;c<nc-1&&ok;c++) if(iscorner(c) && lexcmp(C[c],x)>0) ok=0;
    if(ok) rec();
    nc--; }
}
int main(int argc,char**argv){ d=atoi(argv[1]); m=atoi(argv[2]); WMAX=atoi(argv[3]); IMAX=atoi(argv[4]);
  memset(C,0,sizeof C); nc=1; rec();
  printf("d=%d m=%d WMAX=%d: down-sets %ld | residue-free MC_i fails/tests (i=1..6):",d,m,WMAX,cnt_ds);
  for(int i=1;i<=6;i++) printf(" %ld/%ld",rf_fail[i],rf_tests[i]);
  printf(" | GW rf fails %ld | residue-complete (t>d) instances %ld, MC fails %ld\n",gw_rf_fail,rc_tests,rc_fail);
  return 0; }
