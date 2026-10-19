/* Residue-free test of H_i: for every down-set D in N^d (all units present, |D| = m0..m1), every scale q in [2,QMAX],
 * every weight vector n in [q+1, WM*q]^d (sorted, n_1<=...<=n_d up to symmetry of the shape is NOT assumed: all
 * vectors), check  sum_D min(i,floor(v/q)) <= d sum_D min(i,floor((M-v)/q))  whenever M >= (2i-2)q - 1.
 * Reports failures and the smallest (M+1)/q among failures with M >= thr.  fejer only.
 * Usage: hi_scan d m0 m1 i QMAX WM */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#define DD 5
#define NN 64
typedef struct {uint64_t z; unsigned char x[DD];} Cell;
static Cell X[NN]; static int d, m, sz, I, QMAX, WM, n[DD]; static uint64_t tests, fails, shapes;
static uint64_t unit(int a){return UINT64_C(1)<<(6*a);}
static int find(uint64_t z){for(int i=0;i<sz;i++)if(X[i].z==z)return i;return -1;}
static int cmp64(const void*a,const void*b){uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b;return(x>y)-(x<y);}
static int F(long t,int q){long f=t/q;return f<I?(int)f:I;}
static void weights(int a,int q){
 if(a==d){
  long V[NN],M=0;for(int i=0;i<m;i++){V[i]=0;for(int b=0;b<d;b++)V[i]+=(long)X[i].x[b]*n[b];if(V[i]>M)M=V[i];}
  if(M<(long)(2*I-2)*q-1)return;
  long L=0,R=0;for(int i=0;i<m;i++){L+=F(V[i],q);R+=F(M-V[i],q);}
  tests++;
  if(L>(long)d*R){fails++;if(fails<6){printf("FAIL i=%d d=%d m=%d q=%d M=%ld L=%ld R=%ld n=",I,d,m,q,M,L,(long)d*R);for(int b=0;b<d;b++)printf("%d,",n[b]);printf(" D=");for(int i=0;i<m;i++){printf("[");for(int b=0;b<d;b++)printf("%d",X[i].x[b]);printf("]");}printf("\n");fflush(stdout);}}
  return;}
 for(n[a]=q+1;n[a]<=WM*q;n[a]++)weights(a+1,q);
}
static void shape(void){for(int a=0;a<d;a++)if(find(unit(a))<0)return;shapes++;for(int q=2;q<=QMAX;q++)weights(0,q);}
static void generate(void){
 if(sz==m){shape();return;}
 uint64_t cand[NN*DD],last=X[sz-1].z;int c=0;
 for(int a=0;a<d;a++)if(find(unit(a))<0&&last>unit(a))return;
 for(int i=0;i<sz;i++)for(int a=0;a<d;a++){uint64_t z=X[i].z+unit(a);if(z<=last)continue;int ok=1;
  for(int b=0;b<d;b++)if(((z>>(6*b))&63)&&find(z-unit(b))<0){ok=0;break;}if(ok)cand[c++]=z;}
 qsort(cand,c,sizeof(*cand),cmp64);for(int j=0;j<c;j++)if(!j||cand[j]!=cand[j-1]){X[sz].z=cand[j];for(int a=0;a<d;a++)X[sz].x[a]=(cand[j]>>(6*a))&63;sz++;generate();sz--;}
}
int main(int argc,char**argv){d=atoi(argv[1]);int m0=atoi(argv[2]),m1=atoi(argv[3]);I=atoi(argv[4]);QMAX=atoi(argv[5]);WM=atoi(argv[6]);
 for(m=m0;m<=m1;m++){tests=fails=shapes=0;sz=1;memset(X,0,sizeof(X));generate();printf("d=%d m=%d i=%d q<=%d n<=%dq shapes=%llu tests(M>=(2i-2)q-1)=%llu fails=%llu\n",d,m,I,QMAX,WM,(unsigned long long)shapes,(unsigned long long)tests,(unsigned long long)fails);fflush(stdout);}
}
