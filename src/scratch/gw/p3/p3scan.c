/* Exact exhaustive P3 experiments. Build/run only on fejer.
 * Canonical order ideals, with all labeled instances counted by orbit weight.
 * mode 0: n_a in [m+1,4m]; mode 1: residues complete, n_a=s_a+m*k_a, k=1..3.
 * Independent mathematical predicates are evaluated directly from all cells.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <assert.h>
#define DD 5
#define NN 64
typedef struct {uint64_t z; unsigned char x[DD];} Cell;
static Cell X[NN];
static int d,m,sz,mode,n[DD],s[DD],perm[DD],used[DD],canonical,aut;
static uint64_t shapes,weightedshapes,instances,complete,fail,highfail,lpbad,tcibad,weight;
static uint64_t lowchecks;
static int64_t minhigh;
static int above[NN][NN],lower[NN][DD],nonmax[NN];
static uint64_t unit(int a){return UINT64_C(1)<<(6*a);}
static int find(uint64_t z){for(int i=0;i<sz;i++)if(X[i].z==z)return i;return -1;}
static int cmp64(const void*a,const void*b){uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b;return(x>y)-(x<y);}
static void perms(int j){
 if(!canonical)return;
 if(j==d){uint64_t z[NN];for(int i=0;i<m;i++){z[i]=0;for(int a=0;a<d;a++)z[i]|=(uint64_t)X[i].x[perm[a]]<<(6*a);}qsort(z,m,sizeof(*z),cmp64);
 for(int i=0;i<m;i++){if(z[i]<X[i].z){canonical=0;return;}if(z[i]>X[i].z)return;}aut++;return;}
 for(int a=0;a<d;a++)if(!used[a]){used[a]=1;perm[j]=a;perms(j+1);used[a]=0;}
}
static int small(int x){return x<3?x:3;}
static void dump(const char*name,int sl){
 fprintf(stderr,"%s d=%d m=%d slack=%d n=",name,d,m,sl);for(int a=0;a<d;a++)fprintf(stderr,"%d,",n[a]);fprintf(stderr," D=");
 for(int i=0;i<m;i++){fprintf(stderr,"[");for(int a=0;a<d;a++)fprintf(stderr,"%d,",X[i].x[a]);fprintf(stderr,"]");}fprintf(stderr,"\n");fflush(stderr);
}
static void check(void){
 int V[NN],H[NN],M=0,A=0,B=0,C=0,T=0,Y=0,beta=0,seen[NN]={0},resok=1;
 for(int i=0;i<m;i++){V[i]=0;for(int a=0;a<d;a++)V[i]+=X[i].x[a]*n[a];if(V[i]>M)M=V[i];int r=V[i]%m;if(seen[r])resok=0;seen[r]=1;}
 if(mode&&!resok)return;
 instances+=weight;if(resok)complete+=weight;
 if(M/m==3){
  int rho=4*m-1-M,a=0,b=0,q=0,r=0,ss=0,t=0,u=0,L=0,g=0;
  int cls[DD]={0};
  for(int j=0;j<d;j++){cls[j]=n[j]<2*m-rho?1:n[j]<3*m-rho?2:3;a+=cls[j]==1;b+=cls[j]==2;}
  for(int i=0;i<m;i++){
   int deg=0,aa=0,bb=0,cc=0;for(int j=0;j<d;j++){deg+=X[i].x[j];aa+=X[i].x[j]*(cls[j]==1);bb+=X[i].x[j]*(cls[j]==2);cc+=X[i].x[j]*(cls[j]==3);}
   assert(deg<=3);L+=(M-V[i])/m;g+=V[i]/m;
   if(deg==2){assert(cc==0);if(V[i]<3*m-rho){assert(aa==2);q++;}else if(aa==2)r++;else if(aa==1)ss++;else {assert(bb==2);t++;}}
   if(deg==3){assert(aa==3);u++;for(int j=0;j<d;j++)if(X[i].x[j])assert(V[lower[i][j]]<3*m-rho);}
  }
  assert(q+r<=a*(a+1)/2);assert(ss<=a*b);assert(t<=b*(b+1)/2);assert(3*u<=(a+2)*q);
  assert(L==3+2*a+b+q);
  int W=(d+1)*L-3*m+rho;
  int base=2*a*(a+1)+(a-2)*q-3*(r+u);
  assert(base>=0);
  assert(W==base+b*(3*a+b+1+q)-3*(ss+t)+(d-a-b)*(2*a+b+q)+rho);
  if(resok){assert(t<=rho);assert(g+L==3*m-rho);assert(W>=b*q+(d-a-b)*(2*a+b+q));}
  lowchecks+=weight;
 }
 for(int i=0;i<m;i++){H[i]=0;for(int j=0;j<m;j++)if(above[i][j]&&V[j]-V[i]>H[i])H[i]=V[j]-V[i];}
 for(int i=0;i<m;i++){
  int k=V[i]/m,l=(M-V[i])/m,h=H[i]/m;A+=small(k);B+=small(l);C+=small(h);
  if(i&&k<3)beta+=3-k;
  if(nonmax[i]&&h<3)T+=h;
  if(i){int trap=1;for(int a=0;a<d;a++)if(lower[i][a]>=0&&H[lower[i][a]]>=3*m)trap=0;Y+=trap;}
 }
 int sl=d*B-A;
 if(sl<0){if(!fail)dump("P3FAIL",sl);fail+=weight;}
 if(M>=4*m){if(sl<minhigh)minhigh=sl;if(sl<0){if(!highfail)dump("HIGHFAIL",sl);highfail+=weight;}}
 if(d*C<A){if(!lpbad)dump("LP3FAIL",d*C-A);lpbad+=weight;}
 if(d*T+beta<3*Y){if(!tcibad)dump("TCI3FAIL",d*T+beta-3*Y);tcibad+=weight;}
}
static void lifts(int a){if(a==d){check();return;}for(int k=1;k<=3;k++){n[a]=s[a]+m*k;lifts(a+1);}}
static void residues(int a){
 if(a==d){lifts(0);return;}
 for(int r=1;r<m;r++){
  int dup=0;for(int b=0;b<a;b++)if(s[b]==r)dup=1;if(dup)continue;s[a]=r;
  int seen[NN]={0},ok=1;
  for(int i=0;i<m;i++){int active=1,z=0;for(int b=0;b<d;b++){if(b>a&&X[i].x[b])active=0;z+=X[i].x[b]*s[b];}if(active){z%=m;if(seen[z]){ok=0;break;}seen[z]=1;}}
  if(ok)residues(a+1);
 }
}
static void weights(int a){if(a==d){check();return;}for(n[a]=m+1;n[a]<=4*m;n[a]++)weights(a+1);}
static void shape(void){
 for(int a=0;a<d;a++)if(find(unit(a))<0)return;
 canonical=1;aut=0;memset(used,0,sizeof(used));perms(0);if(!canonical)return;
 weight=1;for(int a=2;a<=d;a++)weight*=a;weight/=aut;shapes++;weightedshapes+=weight;
 for(int i=0;i<m;i++){
  nonmax[i]=0;for(int a=0;a<d;a++){lower[i][a]=X[i].x[a]?find(X[i].z-unit(a)):-1;if(find(X[i].z+unit(a))>=0)nonmax[i]=1;}
  for(int j=0;j<m;j++){above[i][j]=1;for(int a=0;a<d;a++)if(X[j].x[a]<X[i].x[a])above[i][j]=0;}
 }
 if(mode)residues(0);else weights(0);
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
 if(argc!=5)return 1;d=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]);mode=atoi(argv[4]);if(d<1||d>DD||last>=NN)return 1;
 puts("d,m,mode,canonical_shapes,labeled_shapes,instances,residue_complete,P3fail,Kge4fail,minKge4slack,LP3fail,TCI3fail,K3_lemma_checks");fflush(stdout);
 for(m=first;m<=last;m++){
  shapes=weightedshapes=instances=complete=fail=highfail=lpbad=tcibad=lowchecks=0;minhigh=LLONG_MAX;sz=1;memset(X,0,sizeof(X));generate();
  printf("%d,%d,%d,%llu,%llu,%llu,%llu,%llu,%llu,%lld,%llu,%llu,%llu\n",d,m,mode,(unsigned long long)shapes,(unsigned long long)weightedshapes,(unsigned long long)instances,(unsigned long long)complete,(unsigned long long)fail,(unsigned long long)highfail,(long long)minhigh,(unsigned long long)lpbad,(unsigned long long)tcibad,(unsigned long long)lowchecks);fflush(stdout);
 }
}
