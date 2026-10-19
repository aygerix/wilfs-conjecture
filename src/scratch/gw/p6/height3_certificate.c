/* Exact exhaustive MaxCL certificate, active dimension <=5, height <=3.
 * fejer only, nice single-core. Args: d m_low m_high [method].
 * method=0 uses unions of cubic choices; method=1 tests all feasible
 * containers of quadratic divisors, avoiding the choice/dominance DP.
 * Coordinate permutations only are normalized; ALL residue vectors otherwise.
 * A tile is encoded by its quadratic face and one legal cubic per remaining
 * residue. DP enumerates every possible union of covered quadratic divisors.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long ull;
typedef long long ll;
#define SZ 32768
static int d,m,method,p[8],np,ci[15],cj[15],pr[15],nc,cr[35],ca[35],cb[35],cc[35];
static unsigned cm[35];
static ull used[SZ],cover[SZ],all,units;
static unsigned short dp1[SZ],dp2[SZ];
static ull seen[SZ],stamp;
static ull vectors,threecovers,faces,flat,shape_ok,force_ok,dp_faces,dp_masks,sigtests,maxdp;
static ll min_cert=0x7fffffffffffffffLL;
static int opts[56][35],nopts[56],rrlist[56];
static ll maxslack(unsigned q,unsigned covered,int *where){
 int w[56]={0},inc[5]={0};ull ur=used[q];
 for(int j=0;j<np;j++)if(q>>j&1){inc[ci[j]]=inc[cj[j]]=1;if(!(covered>>j&1))w[pr[j]]=d+2;}
 for(int a=0;a<d;a++)if(!inc[a])w[p[a]]=d+1;
 for(int r=0;r<m;r++)if(!(ur>>r&1))w[r]=d+3;
 ll v=0,tot=0,mx=0;for(int r=0;r<m;r++){v+=(ll)r*w[r];tot+=w[r];}mx=v;*where=0;
 for(int s=1;s<m;s++){v+=(ll)m*w[s-1]-tot;if(v>mx){mx=v;*where=s;}}
 sigtests+=m;return (ll)(d+1)*m*(m-1)/2-mx;
}
static ll crude(int t,int pairmax,int spikes){
 ll v=0;int r=m-1;
 for(int j=0;j<t;j++)v+=(ll)(d+3)*r--;
 for(int j=0;j<pairmax;j++)v+=(ll)(d+2)*r--;
 for(int j=0;j<spikes;j++)v+=(ll)(d+1)*r--;
 assert(r>=-1);return (ll)(d+1)*m*(m-1)/2-v;
}
static void fail(unsigned q,unsigned cov,int sg,ll slack){
 unsigned actual=0;int chosen[56],nch=0;
 for(int r=0;r<m;r++)if(!(used[q]>>r&1)){
  int j;for(j=0;j<nc;j++)if(cr[j]==r&&(cm[j]&q)==cm[j]&&(cm[j]&cov)==cm[j])break;
  assert(j<nc);chosen[nch++]=j;actual|=cm[j];
 }
 int actualsg;ll actualsl=maxslack(q,actual,&actualsg);assert(actualsl<=slack&&actualsl<0);
 printf("COUNTEREXAMPLE d=%d m=%d sigma=%d slack=%lld p=",d,m,actualsg,actualsl);
 for(int a=0;a<d;a++)printf("%s%d",a?",":"",p[a]);
 printf("\nD_multisets: []");for(int a=0;a<d;a++)printf(" [%d]",a);
 for(int j=0;j<np;j++)if(q>>j&1)printf(" [%d,%d]",ci[j],cj[j]);
 for(int j=0;j<nch;j++){int c=chosen[j];printf(" [%d,%d,%d]",ca[c],cb[c],cc[c]);}
 printf("\n");fflush(stdout);(void)sg;exit(2);
}
static void check_face(unsigned q){
 int nq=__builtin_popcount(q),t=m-1-d-nq;if(!t){flat++;return;}assert(t>0);
 faces++;unsigned forced=0;int nr=0;
 for(int r=0;r<m;r++)if(!(used[q]>>r&1)){
  unsigned common=q;int cnt=0;
  for(int j=0;j<nc;j++)if(cr[j]==r&&(cm[j]&q)==cm[j]){common&=cm[j];opts[r][cnt++]=cm[j];}
  assert(cnt);nopts[r]=cnt;forced|=common;rrlist[nr++]=r;
 }
 assert(nr==t);int inc[5]={0},spikes=0;
 for(int j=0;j<np;j++)if(q>>j&1)inc[ci[j]]=inc[cj[j]]=1;
 for(int a=0;a<d;a++)spikes+=!inc[a];
 ll v=crude(t,nq-__builtin_popcount(forced),spikes);
 if(v>=0){shape_ok++;if(v<min_cert)min_cert=v;return;}
 int sg;v=maxslack(q,forced,&sg);
 if(v>=0){force_ok++;if(v<min_cert)min_cert=v;return;}
 dp_faces++;
 if(method==1){
  unsigned extra=q&~forced,x=extra;
  do{
   unsigned c=forced|x;
   if((used[q]|cover[c])==all){
    v=crude(t,nq-__builtin_popcount(c),spikes);
    if(v<0)v=maxslack(q,c,&sg);
    dp_masks++;
    if(v<0)fail(q,c,sg,v);
    if(v<min_cert)min_cert=v;
   }
   if(!x)break;
   x=(x-1)&extra;
  }while(1);
  return;
 }
 /* All choices whose non-forced requirements contain a smaller choice are
  * dominated for every sigma, since every pair residue weight is nonnegative.
  */
 int nrr=0;
 for(int ii=0;ii<nr;ii++){
  int r=rrlist[ii],nn=0,small[35];
  for(int j=0;j<nopts[r];j++){
   unsigned x=opts[r][j]&~forced;int dominated=0;
   for(int k=0;k<nopts[r];k++){
    unsigned y=opts[r][k]&~forced;
    if((y&x)==y&&(y!=x||k<j)){dominated=1;break;}
   }
   if(!dominated)small[nn++]=x;
  }
  assert(nn);if(nn==1&&small[0]==0)continue;
  memcpy(opts[r],small,nn*sizeof(int));nopts[r]=nn;rrlist[nrr++]=r;
 }
 int len=1;dp1[0]=0;
 for(int ii=0;ii<nrr;ii++){
  int r=rrlist[ii],next=0;++stamp;assert(stamp);
  for(int j=0;j<len;j++)for(int k=0;k<nopts[r];k++){
   unsigned x=dp1[j]|opts[r][k];if(seen[x]!=stamp){seen[x]=stamp;dp2[next++]=x;}
  }
  memcpy(dp1,dp2,next*sizeof(unsigned short));len=next;if((ull)len>maxdp)maxdp=len;
 }
 for(int j=0;j<len;j++){
  unsigned c=forced|dp1[j];v=maxslack(q,c,&sg);dp_masks++;
  if(v<0)fail(q,c,sg,v);
  if(v<min_cert)min_cert=v;
 }
}
static void check_vector(void){
 vectors++;int pid[5][5],bad[15],oi[15],oj[15],orig[15],nop=0;
 units=1;for(int a=0;a<d;a++)units|=1ULL<<p[a];
 ull cov=units;
 for(int a=0;a<d;a++)for(int b=a;b<d;b++){
  int r=(p[a]+p[b])%m;pid[a][b]=pid[b][a]=nop;oi[nop]=a;oj[nop]=b;bad[nop]=(units>>r)&1;orig[nop++]=r;
  cov|=1ULL<<r;
 }
 for(int a=0;a<d;a++)for(int b=a;b<d;b++)for(int c=b;c<d;c++)cov|=1ULL<<((p[a]+p[b]+p[c])%m);
 if(cov!=all)return;
 threecovers++;
 int comp[15];np=0;
 for(int j=0;j<nop;j++)if(bad[j])comp[j]=-1;else{comp[j]=np;ci[np]=oi[j];cj[np]=oj[j];pr[np++]=orig[j];}
 assert(np<=15);unsigned size=1U<<np;memset(cover,0,size*sizeof(ull));nc=0;cov=units;
 for(int j=0;j<np;j++)cov|=1ULL<<pr[j];
 for(int a=0;a<d;a++)for(int b=a;b<d;b++)for(int c=b;c<d;c++){
  int i=comp[pid[a][b]],j=comp[pid[a][c]],k=comp[pid[b][c]],r=(p[a]+p[b]+p[c])%m;
  if(i<0||j<0||k<0||((units>>r)&1))continue;
  if((i!=j&&pr[i]==pr[j])||(i!=k&&pr[i]==pr[k])||(j!=k&&pr[j]==pr[k]))continue;
  unsigned req=(1U<<i)|(1U<<j)|(1U<<k);
  cm[nc]=req;cr[nc]=r;ca[nc]=a;cb[nc]=b;cc[nc]=c;nc++;
  cover[req]|=1ULL<<r;cov|=1ULL<<r;
 }
 if(cov!=all)return;
 for(unsigned bit=1;bit<size;bit<<=1)for(unsigned base=0;base<size;base+=2*bit)for(unsigned j=0;j<bit;j++)cover[base+bit+j]|=cover[base+j];
 used[0]=units;
 for(unsigned q=0;q<size;q++){
  if(q){unsigned prev=q&(q-1);int j=__builtin_ctz(q);ull rb=1ULL<<pr[j];used[q]=used[prev]&&!(used[prev]&rb)?used[prev]|rb:0;}
  if(used[q]&&(used[q]|cover[q])==all)check_face(q);
 }
}
static void rec(int k,int start){
 if(k==d){check_vector();return;}
 for(int x=start;x<=m-(d-k);x++){p[k]=x;rec(k+1,x+1);}
}
int main(int ac,char**av){
 assert(ac==4||ac==5);d=atoi(av[1]);int lo=atoi(av[2]),hi=atoi(av[3]);method=ac==5?atoi(av[4]):0;assert(2<=d&&d<=5&&0<=method&&method<=1);
 int bound=(d+1)*(d+2)*(d+3)/6;if(lo<d+1)lo=d+1;if(hi>bound)hi=bound;
 for(m=lo;m<=hi;m++){
  vectors=threecovers=faces=flat=shape_ok=force_ok=dp_faces=dp_masks=sigtests=maxdp=0;
  min_cert=0x7fffffffffffffffLL;all=(1ULL<<m)-1;rec(0,1);
  printf("d=%d m=%d vectors=%llu covers=%llu h3_pairfaces=%llu flat=%llu shape=%llu forced=%llu dp_faces=%llu dp_masks=%llu sigma_tests=%llu maxdp=%llu min_bound=%lld method=%d FAILURES=0\n",d,m,vectors,threecovers,faces,flat,shape_ok,force_ok,dp_faces,dp_masks,sigtests,maxdp,min_cert,method);fflush(stdout);
 }
 return 0;
}
