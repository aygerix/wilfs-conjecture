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
static uint64_t inst, k4inst, fail[5];
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
 for(int i=0;i<m;i++){V[i]=0;for(int a=0;a<d;a++)V[i]+=X[i].x[a]*n[a];if(V[i]>M)M=V[i];int r=V[i]%m;if(seen[r])return;seen[r]=1;}
 inst++;
 if(M/m!=4)return;
 k4inst++;
 int rho=5*m-1-M,cls[DD];
 for(int a=0;a<d;a++)cls[a]=(n[a]+rho)/m;
 long g=0,ell=0;
 for(int j=1;j<=4;j++){
  int dj=0;for(int a=0;a<d;a++)dj+=cls[a]<=j;
  long L=0,F=0,R=0;
  for(int i=0;i<m;i++){
   int ok=1;for(int a=0;a<d;a++)if(X[i].x[a]&&cls[a]>j)ok=0;
   if(!ok)continue;
   int band=(V[i]+rho)/m,lam=(M-V[i])/m;
   if(lam!=4-band){printf("BANDERR\n");exit(1);}
   L+=lam;F++;R+=(V[i]%m)>=m-rho;
  }
  long w=(long)(dj+1)*L-4*F+R;
  if(w<minW[j]){minW[j]=w;}
  if(w<0){fail[j]++;if(dumped[j]<3){dumped[j]++;dump("NEG",j,w,rho,cls);}}
 }
 for(int i=0;i<m;i++){g+=V[i]/m;ell+=(M-V[i])/m;}
 if(d*ell-g<0){printf("GWFAIL\n");dump("GW",4,d*ell-g,rho,cls);}
}
static void lifts(int a){if(a==d){check();return;}for(int k=1;k<=4;k++){n[a]=s[a]+m*k;lifts(a+1);}}
static void residues(int a){
 if(a==d){lifts(0);return;}
 for(int r=1;r<m;r++){
  int dup=0;for(int b=0;b<a;b++)if(s[b]==r)dup=1;if(dup)continue;s[a]=r;
  int seen[NN]={0},ok=1;
  for(int i=0;i<m;i++){int active=1,z=0;for(int b=0;b<d;b++){if(b>a&&X[i].x[b])active=0;z+=X[i].x[b]*s[b];}if(active){z%=m;if(seen[z]){ok=0;break;}seen[z]=1;}}
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
 if(argc!=4)return 1;d=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]);
 for(m=first;m<=last;m++){
  inst=k4inst=0;for(int j=0;j<5;j++){fail[j]=0;minW[j]=LONG_MAX;dumped[j]=0;}
  sz=1;memset(X,0,sizeof(X));generate();
  printf("SUMMARY d=%d m=%d inst=%llu K4=%llu minW1..4=%ld %ld %ld %ld fails=%llu %llu %llu %llu\n",d,m,(unsigned long long)inst,(unsigned long long)k4inst,
   minW[1],minW[2],minW[3],minW[4],(unsigned long long)fail[1],(unsigned long long)fail[2],(unsigned long long)fail[3],(unsigned long long)fail[4]);fflush(stdout);
 }
}
