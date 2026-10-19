/* Exhaustive residue-complete down-sets; all active axes, residues 1..m-1,
 * lifts 1..4. One shape per coordinate-permutation orbit (unweighted).
 * Adapted from k4scan.c. Usage: p4_scan d first last. fejer only.
 */
#include "p5_check.h"
#include <limits.h>
#define DD 5
#define NN 64
typedef struct {uint64_t z;unsigned char x[DD];} Cell;
static Cell X[NN];
static int d,m,sz,n[DD],s[DD],perm[DD],used[DD],canonical,mode=1;
static uint64_t instances,shapes;
static uint64_t unit(int a){return UINT64_C(1)<<(6*a);}
static int find(uint64_t z){for(int i=0;i<sz;i++)if(X[i].z==z)return i;return -1;}
static int cmp64(const void*a,const void*b){uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b;return(x>y)-(x<y);}
static void perms(int j){
 if(!canonical)return;
 if(j==d){uint64_t z[NN];for(int i=0;i<m;i++){z[i]=0;for(int a=0;a<d;a++)z[i]|=(uint64_t)X[i].x[perm[a]]<<(6*a);}qsort(z,m,sizeof(*z),cmp64);
  for(int i=0;i<m;i++){if(z[i]<X[i].z){canonical=0;return;}if(z[i]>X[i].z)return;}return;}
 for(int a=0;a<d;a++)if(!used[a]){used[a]=1;perm[j]=a;perms(j+1);used[a]=0;}
}
static void check(void){
 int flat[NN*DD];for(int i=0;i<m;i++)for(int j=0;j<d;j++)flat[i*d+j]=X[i].x[j];
 instances++;if(mode)p5verify(m,d,flat,n);else h4verify(m,d,flat,n,m);
}
static void weights(int a){if(a==d){check();return;}for(n[a]=m+1;n[a]<=3*m;n[a]++)weights(a+1);}
static void lifts(int a){if(a==d){check();return;}for(int k=1;k<=4;k++){n[a]=s[a]+m*k;lifts(a+1);}}
static void residues(int a){
 if(a==d){lifts(0);return;}
 for(int r=1;r<m;r++){
  int dup=0;for(int b=0;b<a;b++)if(s[b]==r)dup=1;if(dup)continue;s[a]=r;
  int seen[NN]={0},ok=1;
  for(int i=0;i<m;i++){
   int active=1,z=0;for(int b=0;b<d;b++){if(b>a&&X[i].x[b])active=0;z+=X[i].x[b]*s[b];}
   if(active){z%=m;if(seen[z]){ok=0;break;}seen[z]=1;}
  }
  if(ok)residues(a+1);
 }
}
static void shape(void){
 for(int a=0;a<d;a++)if(find(unit(a))<0)return;
 canonical=1;memset(used,0,sizeof(used));perms(0);if(!canonical)return;
 shapes++;if(mode)residues(0);else weights(0);
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
 assert(argc==4||argc==5);d=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]);if(argc==5)mode=atoi(argv[4]);assert(d>=1&&d<=DD&&last<NN);
 for(m=first;m<=last;m++){
  instances=shapes=pchecks=pquad=pnoa=psaturated=pshort=pcarry=pa2=pwaneg=pa3=pwa3neg=0;pmin=INT_MAX;
  hchecks=hdeficits=hcellcharges=hcolcharges=0;
  sz=1;memset(X,0,sizeof(X));generate();printf("d=%d m=%d canonical_shapes=%llu instances=%llu ",d,m,(unsigned long long)shapes,(unsigned long long)instances);p5summary();fflush(stdout);
 }
}
