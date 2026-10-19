/* Independent GW exhaustive search.  gcc -O3 -std=c11 gw_scan.c -o gw_scan
 * All labeled order ideals are generated once by increasing lexicographic
 * prefixes; one representative per S_d orbit is tested, with orbit weight.
 * No project Python enumeration or mathematical helper code is used. */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#include <time.h>
#define DD 6
#define NN 32
typedef struct { uint64_t z; unsigned char x[DD]; } Cell;
static Cell cells[NN];
static int d,m,K=2,do_minimal,sz,perm[DD],used[DD],s[DD],order[DD];
static int stage[NN],nc[DD],ids[DD][NN],corners[NN],nt;
static int64_t sums[DD],baseg,basev[NN],n[DD];
static uint64_t ideals,orbits,pairs,instances,failures,minimal,nonminimal,eq_nonminimal;
static uint64_t hard_instances,weight;
static int64_t minE,minHard;
static unsigned aut;
static int canonical;
static uint64_t pfail,ptight;static int64_t pminslack=INT64_MAX;
static double now(clockid_t clk){struct timespec t;clock_gettime(clk,&t);return t.tv_sec+t.tv_nsec*1e-9;}
static int cmp64(const void*a,const void*b){uint64_t x=*(const uint64_t*)a,y=*(const uint64_t*)b;return (x>y)-(x<y);}
static int find(uint64_t z){for(int i=0;i<sz;i++)if(cells[i].z==z)return i;return -1;}
static uint64_t unit(int a){return UINT64_C(1)<<(5*a);}
static void perms(int q){
 if(!canonical)return;
 if(q==d){
  uint64_t z[NN];
  for(int i=0;i<m;i++){z[i]=0;for(int a=0;a<d;a++)z[i]|=(uint64_t)cells[i].x[perm[a]]<<(5*a);}
  qsort(z,m,sizeof(*z),cmp64);
  for(int i=0;i<m;i++){if(z[i]<cells[i].z){canonical=0;return;}if(z[i]>cells[i].z)return;}
  aut++;return;
 }
 for(int a=0;a<d;a++)if(!used[a]){used[a]=1;perm[q]=a;perms(q+1);used[a]=0;}
}
static int is_minimal(void){
 int64_t dist[NN];int done[NN]={0};
 for(int r=0;r<m;r++)dist[r]=INT64_MAX/4;
 dist[0]=0;
 for(int j=0;j<m;j++){
  int r=-1;for(int a=0;a<m;a++)if(!done[a]&&(r<0||dist[a]<dist[r]))r=a;
  done[r]=1;
  for(int a=0;a<d;a++){int t=(r+s[a])%m;if(dist[t]>dist[r]+n[a])dist[t]=dist[r]+n[a];}
 }
 for(int i=0;i<m;i++){int r=(int)(basev[i]%m);int64_t v=0;for(int a=0;a<d;a++)v+=cells[i].x[a]*n[a];if(dist[r]!=v)return 0;}
 return 1;
}
static void lifts(int a,int64_t g){
 if(a<d){for(int k=0;k<=K;k++){n[a]=s[a]+m*k;lifts(a+1,g+k*sums[a]);}return;}
 int64_t M=0;for(int j=0;j<nt;j++){int i=corners[j];int64_t v=0;for(int b=0;b<d;b++)v+=cells[i].x[b]*n[b];if(v>M)M=v;}
 int64_t c=M-m+1,E=d*c-(d+1)*g;
 instances+=weight;if(E<minE)minE=E;
 { /* prefix family P_i: sum_{j<=i} #{kappa>=j} <= d sum_{j<=i} #{lambda>=j}, all i>=1 */
  int hk[256]={0},hl[256]={0},top=0;
  for(int i=0;i<m;i++){int64_t v=0;for(int b=0;b<d;b++)v+=cells[i].x[b]*n[b];int k=(int)(v/m),l=(int)((M-v)/m);
   if(k>255||l>255)abort();hk[k]++;hl[l]++;if(k>top)top=k;if(l>top)top=l;}
  int A=m,B=m;int64_t run=0,best=INT64_MIN;int tight=0;
  for(int j=1;j<=top;j++){A-=hk[j-1];B-=hl[j-1];run+=A-(int64_t)d*B;if(run>best)best=run;if(run==0&&A>0)tight=1;}
  if(top>=1){if(-best<pminslack)pminslack=-best;}
  if(tight)ptight+=weight;
  if(best>0){pfail+=weight;if(pfail<=weight*5){fprintf(stderr,"PFAIL d=%d m=%d n=",d,m);for(int b=0;b<d;b++)fprintf(stderr,"%lld,",(long long)n[b]);
   fprintf(stderr," D=");for(int i=0;i<m;i++){fprintf(stderr,"[");for(int b=0;b<d;b++)fprintf(stderr,"%d,",cells[i].x[b]);fprintf(stderr,"]");}fprintf(stderr,"\n");fflush(stderr);}}
 }
 if(nt>d){hard_instances+=weight;if(E<minHard)minHard=E;}
 if(do_minimal){if(is_minimal())minimal+=weight;else {nonminimal+=weight;if(E==0)eq_nonminimal+=weight;}}
 else if(E==0&&!is_minimal())eq_nonminimal+=weight;
 if(E<0){
  failures+=weight;fprintf(stderr,"FAIL d=%d m=%d E=%lld c=%lld g=%lld n=",d,m,(long long)E,(long long)c,(long long)g);
  for(int b=0;b<d;b++)fprintf(stderr,"%lld,",(long long)n[b]);
  fprintf(stderr," D=");
  for(int i=0;i<m;i++){fprintf(stderr,"[");for(int b=0;b<d;b++)fprintf(stderr,"%d,",cells[i].x[b]);fprintf(stderr,"]");}
  fprintf(stderr,"\n");fflush(stderr);exit(2);
 }
}
static void residues(int a,uint64_t mask){
 if(a>=d){pairs+=weight;int64_t total=0;for(int i=0;i<m;i++){basev[i]=0;for(int b=0;b<d;b++)basev[i]+=cells[i].x[b]*s[b];total+=basev[i];}
  baseg=(total-(int64_t)m*(m-1)/2)/m;lifts(0,baseg);return;}
 if(a>=DD)abort();
 int b=order[a];
 for(int t=1;t<m;t++){
  int dup=0;for(int j=0;j<a;j++)if(s[order[j]]==t){dup=1;break;}if(dup)continue;
  s[b]=t;uint64_t bits=mask;int ok=1;
  for(int j=0;j<nc[a];j++){
   int i=ids[a][j],r=0;for(int h=0;h<d&&h<=a;h++)r+=cells[i].x[order[h]]*s[order[h]];r%=m;
   uint64_t bit=UINT64_C(1)<<r;if(bits&bit){ok=0;break;}bits|=bit;
  }
  if(ok)residues(a+1,bits);
 }
}
static void shape(void){
 for(int a=0;a<d;a++)if(find(unit(a))<0)return;
 canonical=1;aut=0;memset(used,0,sizeof(used));perms(0);if(!canonical)return;
 uint64_t fact=1;for(int a=2;a<=d;a++)fact*=a;weight=fact/aut;
 orbits++;ideals+=weight;memset(sums,0,sizeof(sums));nt=0;
 for(int i=0;i<m;i++){
  int maximal=1;for(int a=0;a<d;a++){sums[a]+=cells[i].x[a];if(find(cells[i].z+unit(a))>=0)maximal=0;}
  if(maximal)corners[nt++]=i;
 }
 /* Put long axes first to reject residue collisions at shallow depth. */
 for(int a=0;a<d;a++)order[a]=a;
 for(int a=0;a<d;a++)for(int b=a+1;b<d;b++)if(sums[order[b]]>sums[order[a]]){int t=order[a];order[a]=order[b];order[b]=t;}
 memset(nc,0,sizeof(nc));
 for(int i=1;i<m;i++){int j=d-1;while(!cells[i].x[order[j]])j--;stage[i]=j;ids[j][nc[j]++]=i;}
 residues(0,1);
}
static void generate(void){
 if(sz==m){shape();return;}
 uint64_t cand[NN*DD];int q=0;uint64_t last=cells[sz-1].z;
 for(int a=0;a<d;a++)if(find(unit(a))<0&&last>unit(a))return;
 for(int i=0;i<sz;i++)for(int a=0;a<d;a++){
  if(cells[i].x[a]>=m-1)continue;
  uint64_t z=cells[i].z+unit(a);if(z<=last)continue;
  int ok=1;for(int b=0;b<d;b++)if(((z>>(5*b))&31)&&find(z-unit(b))<0){ok=0;break;}
  if(ok)cand[q++]=z;
 }
 qsort(cand,q,sizeof(*cand),cmp64);
 for(int j=0;j<q;j++)if(!j||cand[j]!=cand[j-1]){
  cells[sz].z=cand[j];for(int a=0;a<d;a++)cells[sz].x[a]=(cand[j]>>(5*a))&31;
  sz++;generate();sz--;
 }
}
int main(int argc,char**argv){
 if(argc<4){fprintf(stderr,"usage: %s d m_first m_last [minimal_m]\n",argv[0]);return 1;}
 d=atoi(argv[1]);int first=atoi(argv[2]),last=atoi(argv[3]),check=argc>4?atoi(argv[4]):-1;
 if(d<1||d>DD||first<d+1||last>=NN)return 1;
 puts("d,m,canonical_downsets,labeled_downsets,residue_pairs,instances,hard_instances,failures,min_E,min_E_more_than_d_corners,minimal,nonminimal,equality_nonminimal,wall_seconds,cpu_seconds,prefix_fail,prefix_tight_somewhere,prefix_min_slack");fflush(stdout);
 for(m=first;m<=last;m++){
  pfail=ptight=0;pminslack=INT64_MAX;ideals=orbits=pairs=instances=hard_instances=failures=minimal=nonminimal=eq_nonminimal=0;minE=minHard=INT64_MAX;do_minimal=m==check;
  sz=1;memset(cells,0,sizeof(cells));double wall=now(CLOCK_MONOTONIC),cpu=now(CLOCK_PROCESS_CPUTIME_ID);generate();
  printf("%d,%d,%llu,%llu,%llu,%llu,%llu,%llu,",d,m,(unsigned long long)orbits,(unsigned long long)ideals,(unsigned long long)pairs,(unsigned long long)instances,(unsigned long long)hard_instances,(unsigned long long)failures);
  if(minE==INT64_MAX)printf("NA,");else printf("%lld,",(long long)minE);
  if(minHard==INT64_MAX)printf("NA,");else printf("%lld,",(long long)minHard);
  if(do_minimal)printf("%llu,%llu,",(unsigned long long)minimal,(unsigned long long)nonminimal);else printf("NA,NA,");
  printf("%llu,%.6f,%.6f,%llu,%llu,%lld\n",(unsigned long long)eq_nonminimal,now(CLOCK_MONOTONIC)-wall,now(CLOCK_PROCESS_CPUTIME_ID)-cpu,(unsigned long long)pfail,(unsigned long long)ptight,(long long)pminslack);fflush(stdout);
 }
 return 0;
}
