/* Targeted actual semigroups <m,base> union [3m+h,infinity).
 * Compile/run exclusively on fejer; single core, nice.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXM 20001
#define MAXA 80
static uint64_t st;
static uint64_t rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static int member[5*MAXM],ap[MAXM],base[MAXA],ng[MAXA],fact[MAXM][4],degree[MAXM],typ[MAXM];
static long long C2(long long a){return a*(a-1)/2;}
static long long C3(long long a){return a*(a-1)*(a-2)/6;}
static void show(const char*label,int m,int h,int nb,int a,int b,int c,int e,int q2,int q3,int u3,int u4,int k,int WA,int W,int lowplus,int alpha,int hot,int JA){
 printf("%s m=%d h=%d a=%d b=%d c=%d e=%d q2=%d q3=%d u3=%d u4=%d k=%d WA=%d W=%d LOWplus=%d alpha=%d hot=%d JA=%d base=",label,m,h,a,b,c,e,q2,q3,u3,u4,k,WA,W,lowplus,alpha,hot,JA);
 for(int j=0;j<nb;j++)printf("%s%d",j?",":"",base[j]);puts("");fflush(stdout);
}
int main(int argc,char**argv){
 assert(argc==5);st=strtoull(argv[1],0,10)*2654435761ULL+1;long trials=atol(argv[2]);int mlo=atoi(argv[3]),mhi=atoi(argv[4]);assert(mhi<MAXM);
 long actual=0,large=0,deficient=0,lowdef=0,frontier=0,one=0,frontier2=0;int best=1000000000,bestwa=1000000000;
 for(long it=0;it<trials;it++){
  int m=mlo+rnd()%(mhi-mlo+1),h=2+rnd()%(m-1),C=3*m+h,M=4*m+h-1;
  int aa=7+rnd()%14,bb=rnd()%41,alpha=1+rnd()%(aa/2+1),flavor=it%5,nb=1;base[0]=m;
  int L=1+rnd()%((h+1)/2);
  for(int j=0;j<aa;j++){
   int t;
   if(j<alpha){int span=(h-1)/2;t=span?1+rnd()%span:1;}
   else if(flavor==0){int lo=h-L;if(lo>=h)lo=h-1;t=lo+rnd()%(h-lo);}
   else if(flavor==1){int lo=(h+1)/2;t=lo+rnd()%(h-lo);}
   else if(flavor==2){int lo=(h+2)/3,hi=(2*h+2)/3;if(hi<=lo)hi=lo+1;t=lo+rnd()%(hi-lo);}
   else {int lo=(2*h+2)/3;if(lo>=h)lo=h-1;t=lo+rnd()%(h-lo);}
   base[nb++]=m+t;
  }
  for(int j=0;j<bb;j++)base[nb++]=m+h+rnd()%m;
  for(int j=0;j<nb;j++)for(int k=j+1;k<nb;k++)if(base[k]<base[j]){int t=base[k];base[k]=base[j];base[j]=t;}
  memset(member,0,(M+1)*sizeof(int));member[0]=1;
  for(int z=1;z<C;z++)for(int j=0;j<nb&&base[j]<=z;j++)if(member[z-base[j]]){member[z]=1;break;}
  for(int z=C;z<=M;z++)member[z]=1;
  while(C>0&&member[C-1])C--;
  if(C<=3*m)continue;
  h=C-3*m;M=C+m-1;
  for(int r=0;r<m;r++){int z=r;while(!member[z])z+=m;assert(z<=M);ap[r]=z;}
  int nng=0,a=0,b=0,c=0,e=0,Lactual=m,alow=0,p=0;
  for(int z=m+1;z<=M;z++)if(member[z]){
   int dec=0;for(int j=0;j<nb&&base[j]<z;j++)if(member[z-base[j]]){dec=1;break;}
   if(!dec){
    int cl=(z+m-h)/m;a+=cl==1;b+=cl==2;c+=cl==3;e+=cl==4;
    if(cl==1){if(z-m<Lactual)Lactual=z-m;alow+=2*(z-m)<h;p+=3*(z-m)>=2*h;}
    if(z<C){assert(nng<MAXA);ng[nng++]=z;}
   }
  }
  memset(degree,0,m*sizeof(int));int ell=0,g=0,q2=0,q3=0,u3=0,u4=0,k4=0,s=0,t=0,JA=0,J=0,hot=0,SR=0;
  int theta=(3*h+1)/2;
  for(int z=1;z<=M;z++){
   int r=z%m;if(ap[r]!=z)continue;int found=0;
   for(int j=0;j<nng&&!found&&ng[j]<=z;j++){
    int pr=(z-ng[j])%m;
    if(ap[pr]==z-ng[j]){int dg=degree[pr]+1;assert(dg<=4);degree[r]=dg;for(int u=0;u<dg-1;u++)fact[r][u]=fact[pr][u];fact[r][dg-1]=ng[j];found=1;}
   }
   if(!found){assert(z>=C);degree[r]=1;fact[r][0]=z;}
   int dg=degree[r],A=0,B=0,CC=0,bc=0;
   for(int j=0;j<dg;j++){int cl=(fact[r][j]+m-h)/m;A+=cl==1;B+=cl==2;CC+=cl==3;}
   int band=(z+m-h)/m,tau=z-dg*m;
   q2+=dg==2&&A==2&&band==2;q3+=dg==2&&A==2&&band==3;
   u3+=dg==3&&A==3&&band==3;u4+=dg==3&&A==3&&band==4;k4+=dg==4;
   s+=dg==2&&A==1&&B==1&&band==3;t+=dg==2&&B==2&&band==3;
   hot+=dg==3&&A==3&&tau>=2*h;
   if(dg==2&&B==2&&band==3)SR++;
   if(dg==2&&B==1&&CC==1)SR++;
   if(dg==3&&A==2&&B==1){int bv=0;for(int j=0;j<dg;j++)if((fact[r][j]+m-h)/m==2)bv=fact[r][j];if((z-bv+m-h)/m==3)SR++;}
   if(dg==3&&((A==1&&B==2)||B==3))SR++;
   int rr=z%m,iny=(h<=rr&&rr<theta)||(1<=rr&&rr<theta-m);
   int allowed=(dg==1&&A==0)||(dg==2&&A==2&&band==3)||(dg==2&&A==1&&B==1&&band==4)||(dg==2&&B==2&&band==4);
   if(iny&&!allowed){J++;if(A==dg)JA++;}
   (void)bc;
  }
  for(int r=0;r<m;r++){ell+=(M-ap[r])/m;g+=ap[r]/m;}
  int d=a+b+c+e,W=d*ell-g,WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+k4);
  long long Q=C2(a+1),Ca=C3(a+1),ra=Q-q2-q3,ta=C3(a+2)-u3-u4,LC=(a+1)*(q2+u3)-4*k4;
  int Trans=a*b-s+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s+t+u3)+b*u3;
  assert(SR+hot<=m-h);assert(W>=WA+Trans+hot);
  long long D3=3*ta-(a+2)*ra;
  assert(W>=LC+C3(p+2)-Ca+5*ra+D3+Trans);
  int delta=h-2*Lactual;if(delta<0)delta=0;
  int G=c*(c+e+1)+e*(3*a+2*b-1)+(c+e)*(q3+s+t);
  long long bound= (a-1)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3);
  int loss=2*J-(b+2)*q2-k4;if(loss<0)loss=0;
  if(a>=3)assert(W>=bound+D3-loss);
  if(a>=6&&alow==1){one++;assert(2*JA<=(a-1)+LC+2*q2+k4);assert(W>=0);}
  actual++;large+=a>=7;
  if(a<7||!delta)continue;
  if(WA<0){deficient++;lowdef++;}
  long long mn=(a+1)*q2;if(mn>Ca)mn=Ca;
  int lowplus=3*delta-((a-1)*(b+1)+G+mn+(b+2)*q2+b*u3+k4+(c+e)*(2*q2+u3));
  if(WA<0&&lowplus>0){
   frontier++;long long other=LC+C3(p+2)-Ca+5*ra+D3+Trans;
   if(other<0&&alow>=2)frontier2++;
   if(W<best){best=W;show("frontier",m,h,nb,a,b,c,e,q2,q3,u3,u4,k4,WA,W,lowplus,alow,hot,JA);}
  }
  if(WA<bestwa){bestwa=WA;if(WA<0)show("best_WA",m,h,nb,a,b,c,e,q2,q3,u3,u4,k4,WA,W,lowplus,alow,hot,JA);}
  (void)ta;
 }
 printf("seed=%s trials=%ld actual=%ld a_ge7=%ld deficient_low=%ld frontier=%ld frontier_after_new=%ld one_low_checks=%ld best_WA=%d best_frontier_W=%d\n",argv[1],trials,actual,large,lowdef,frontier,frontier2,one,bestwa,best);
}
