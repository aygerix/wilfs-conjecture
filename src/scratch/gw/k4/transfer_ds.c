/* GW at K = 4 (M in [4m,5m)): exhaustive residue-complete multiplicity-form instances.
 * Face test: F_j = cells supported on directions of class <= j (class = band of n_a).
 * W_j = (d_j+1)*sum_{F_j} lambda - 4|F_j| + rho_*(F_j), rho_*(F) = #{x in F : v mod m >= m-rho}.
 * W_4 = W = d*ell - g (GW slack). Build/run on fejer only.  Usage: k4scan d mfirst mlast
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#define DD 5
#define NN 64
typedef struct {uint64_t z; unsigned char x[DD];} Cell;
static Cell X[NN];
static int d,m,sz,n[DD],s[DD],perm[DD],used[DD],canonical,aut;
static uint64_t inst, k4inst, fail[5], trf[12], perK[12], defK[12]; static int KMAX, NORES;
static long minW[5]; static int dumped[5];
static uint64_t unit(int a){return UINT64_C(1)<<(6*a);}
static int find(uint64_t z){for(int i=0;i<sz;i++)if(X[i].z==z)return i;return -1;}
static int cmp64(const void*a,const void*b){uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b;return(x>y)-(x<y);}
static void perms(int j){
 if(!canonical)return;
 if(j==d){uint64_t z[NN];for(int i=0;i<m;i++){z[i]=0;for(int a=0;a<d;a++)z[i]|=(uint64_t)X[i].x[perm[a]]<<(6*a);}qsort(z,m,sizeof(*z),cmp64);
 for(int i=0;i<m;i++){if(z[i]<X[i].z){canonical=0;return;}if(z[i]>X[i].z)return;}aut++;return;}
 for(int a=0;a<d;a++)if(!used[a]){used[a]=1;perm[j]=a;perms(j+1);used[a]=0;}
}
static void dump(const char*name,int j,long w,int rho,int*cls){
 printf("%s j=%d d=%d m=%d W=%ld rho=%d n=",name,j,d,m,w,rho);for(int a=0;a<d;a++)printf("%d(c%d),",n[a],cls[a]);printf(" D=");
 for(int i=0;i<m;i++){printf("[");for(int a=0;a<d;a++)printf("%d",X[i].x[a]);printf("]");}printf("\n");fflush(stdout);
}
static void check(void){
 int V[NN],M=0,seen[NN]={0};
 for(int i=0;i<m;i++){V[i]=0;for(int a=0;a<d;a++)V[i]+=X[i].x[a]*n[a];if(V[i]>M)M=V[i];int r=V[i]%m;if(seen[r]&&!NORES)return;seen[r]=1;}
 inst++;
 int K=M/m; if(K>=12)return; perK[K]++;
 int rho=(K+1)*m-1-M;
 long L=0,F=0,ell=0,g=0; int a=0, inA[DD];
 for(int b=0;b<d;b++){inA[b]=n[b]<2*m-rho;a+=inA[b];}
 for(int i=0;i<m;i++){g+=V[i]/m;ell+=(M-V[i])/m;int ok=1;for(int b=0;b<d;b++)if(X[i].x[b]&&!inA[b])ok=0;if(ok){L+=(M-V[i])/m;F++;}}
 long WA=(long)(a+1)*L-(long)K*F, W=d*ell-g;
 if(WA<0)defK[K]++;
 if(W<WA){trf[K]++; if(a>0||trf[K]<2)dump(a>0?"TRFAIL_A":"TRFAIL0",K,W-WA,rho,inA);}
 if(W<0&&!NORES){printf("GWFAIL\n");}
}
static void lifts(int a){if(a==d){check();return;}for(int k=1;k<=KMAX;k++){n[a]=s[a]+m*k;lifts(a+1);}}
static void residues(int a){
 if(a==d){lifts(0);return;}
 for(int r=1;r<m;r++){
  int dup=0;if(!NORES)for(int b=0;b<a;b++)if(s[b]==r)dup=1;if(dup)continue;s[a]=r;
  int seen[NN]={0},ok=1;
  for(int i=0;i<m;i++){int active=1,z=0;for(int b=0;b<d;b++){if(b>a&&X[i].x[b])active=0;z+=X[i].x[b]*s[b];}if(active&&!NORES){z%=m;if(seen[z]){ok=0;break;}seen[z]=1;}}
  if(ok)residues(a+1);
 }
}
static void shape(void){
 for(int a=0;a<d;a++)if(find(unit(a))<0)return;
 canonical=1;aut=0;memset(used,0,sizeof(used));perms(0);if(!canonical)return;
 residues(0);
}
static void generate(void){
 if(sz==m){shape();return;}
 uint64_t cand[NN*DD],last=X[sz-1].z;int q=0;
 for(int a=0;a<d;a++)if(find(unit(a))<0&&last>unit(a))return;
 for(int i=0;i<sz;i++)for(int a=0;a<d;a++){
  uint64_t z=X[i].z+unit(a);if(z<=last)continue;int ok=1;
  for(int b=0;b<d;b++)if(((z>>(6*b))&63)&&find(z-unit(b))<0){ok=0;break;}
  if(ok)cand[q++]=z;
 }
 qsort(cand,q,sizeof(*cand),cmp64);for(int j=0;j<q;j++)if(!j||cand[j]!=cand[j-1]){
  X[sz].z=cand[j];for(int a=0;a<d;a++)X[sz].x[a]=(cand[j]>>(6*a))&63;sz++;generate();sz--;
 }
}
int main(int argc,char**argv){
 if(argc<5)return 1;NORES=argc>5;d=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]);KMAX=atoi(argv[4]);
 for(m=first;m<=last;m++){
  inst=0;for(int j=0;j<12;j++){trf[j]=perK[j]=defK[j]=0;}
  sz=1;memset(X,0,sizeof(X));generate();
  printf("d=%d m=%d inst=%llu :",d,m,(unsigned long long)inst);for(int K=1;K<12;K++)if(perK[K])printf(" K%d[n=%llu WA<0:%llu W<WA:%llu]",K,(unsigned long long)perK[K],(unsigned long long)defK[K],(unsigned long long)trf[K]);printf("\n");fflush(stdout);
 }
}
