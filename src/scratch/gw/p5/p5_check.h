/* P5 assertions; compile/run only on fejer. Counts are cumulative. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define PMAX 128
static uint64_t pchecks,pquad,pnoa,psaturated,pshort,pcarry,pa2,pwaneg,pa3,pwa3neg;
static uint64_t hchecks,hdeficits,hcellcharges,hcolcharges;
static int pmin;
static uint64_t p5primary,p5upper,p5linear,p5curve,p5low,p5adaptive,p5lc,p5class[4];
static int p5min=1000000000,p5amin=1000000000,p5maxa,p5maxb;
static long long C2(long long x){return x*(x-1)/2;}
static long long C3(long long x){return x*(x-1)*(x-2)/6;}
static long long mac2(long long t){
 long long k=1;while(C2(k+1)<=t)k++;
 return C3(k+1)+C2(t-C2(k)+1);
}
static void h4verify(int m,int d,const int*X,const int*n,int q){(void)m;(void)d;(void)X;(void)n;(void)q;}
static int p5verify(int m,int d,const int*X,const int*n){
 int V[PMAX],dg[PMAX],cl[PMAX],M=0,seen[PMAX]={0},owner[PMAX];
 assert(m<PMAX&&d<PMAX);
 for(int i=0;i<m;i++){
  V[i]=dg[i]=0;for(int j=0;j<d;j++){assert(n[j]>m);V[i]+=X[i*d+j]*n[j];dg[i]+=X[i*d+j];}
  assert(!seen[V[i]%m]);seen[V[i]%m]=1;owner[V[i]%m]=i;if(V[i]>M)M=V[i];
 }
 if(M/m!=4)return 0;p5primary++;
 int rho=5*m-1-M,h=m-rho,a=0,b=0,c=0,e=0,L=m;
 for(int j=0;j<d;j++){
  cl[j]=(n[j]+rho)/m;a+=cl[j]==1;b+=cl[j]==2;c+=cl[j]==3;e+=cl[j]==4;
  if(cl[j]==1&&n[j]-m<L)L=n[j]-m;
 }
 int q2=0,q=0,u3=0,u=0,k=0,s=0,S=0,H=0,t=0,T=0,I=0,v2=0,v=0,w=0,z=0;
 int ty[PMAX],band[PMAX],ell=0,g=0,N=0;
 for(int i=0;i<m;i++){
  int A=0,B=0,C=0,E=0;band[i]=(V[i]+rho)/m;
  ell+=(M-V[i])/m;g+=V[i]/m;N+=dg[i]>=2;
  for(int j=0;j<d;j++){A+=X[i*d+j]*(cl[j]==1);B+=X[i*d+j]*(cl[j]==2);C+=X[i*d+j]*(cl[j]==3);E+=X[i*d+j]*(cl[j]==4);}
  ty[i]=0;
  if(dg[i]==1&&B+C+E==1)ty[i]=1;
  if(dg[i]==2&&A==2){q2+=band[i]==2;q+=band[i]==3;if(band[i]==3)ty[i]=1;}
  if(dg[i]==2&&A==1&&B==1){s+=band[i]==3;S+=band[i]==4;if(band[i]==4)ty[i]=1;}
  if(dg[i]==2&&A==1&&C==1)H++;
  if(dg[i]==2&&B==2){t+=band[i]==3;T+=band[i]==4;if(band[i]==4)ty[i]=1;}
  if(dg[i]==2&&B==1&&C==1)I++;
  if(dg[i]==3&&A==3){u3+=band[i]==3;u+=band[i]==4;}
  if(dg[i]==3&&A==2&&B==1){int bv=0;for(int j=0;j<d;j++)if(cl[j]==2)bv+=n[j]*X[i*d+j];if((V[i]-bv+rho)/m==2)v2++;else v++;}
  if(dg[i]==3&&A==1&&B==2)w++;
  if(dg[i]==3&&B==3)z++;
  if(dg[i]==4)k++;
 }
 long long Q=C2(a+1),Bc=C2(b+1),Z=C3(b+2),Ca=C3(a+1),r=c+e;
 assert(m==1+d+N&&ell==4+3*a+2*b+c+2*q2+q+s+t+u3);
 assert(g+ell==4*m-rho);int W=d*ell-g;
 assert(W==(d+1)*(ell-4)-4*N+rho);
 assert(q2+q<=Q&&s+S<=a*b&&t+T<=Bc&&H<=a*c&&I<=b*c);
 assert(3*(u3+u)<=(a+2)*(q2+q)&&3*u3<=(a+2)*q2&&4*k<=(a+3)*u3);
 assert(v2<=b*q2&&v<=b*q&&2*(v2+v)<=(a+1)*s);
 assert(w<=a*t&&2*w<=(b+1)*s&&3*z<=(b+2)*t);
 assert(t+I+v+w+z<=rho);
 assert(z<=mac2(t));
 if(b)assert(3*(Z*t-(long long)z*Bc)*(2*b+1)>=2*Bc*t*(Bc-t));
 int WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q+u3)-4*(u+k);
 int Trans=a*b-s+c*(c+1)+e*(3*a+2*b+c)+r*(2*q2+q+s+t+u3)+b*u3;
 int Rem=4*(a*b-s-S)+4*(a*c-H)+4*(Bc-t-T)+rho-t-I-v-w-z+3*(b*c-I)+(b+2)*t-3*z+a*t+(b+1)*s-3*w+2*b*q2+b*q+(a+1)*s-4*v2-3*v;
 assert(Rem>=0&&W==WA+Trans+Rem);
 int K=q+b+c+e+S+T;
 if(a){
  int delta=h-2*L;if(delta<0)delta=0;
  assert(h<=2*K+2+3*delta);p5adaptive++;
  if(3*L>h){
   int theta=delta?3*L:(3*h+1)/2,ys=0;
   for(int rr=1;rr<m;rr++)if((rr>=h&&rr<theta)||(theta>m&&rr<theta-m)){
    ys++;assert(ty[owner[rr]]);
   }
   if(delta)assert(ys>=3*L-h-1);else assert(2*ys>=h-2);
  }
  if(a>=3){
   long long LC=(a+1)*(q2+u3)-4*k,mn=(a+1)*q2;if(mn>Ca)mn=Ca;
   assert(LC>=mn);p5lc++;
   long long G=c*(c+e+1)+e*(3*a+2*b-1)+r*(q+s+t);
   long long loss=3*delta-(b+2)*q2-k;if(loss<0)loss=0;
   assert(W>=(a-1)*(b+1)+G+mn+b*u3+r*(2*q2+u3)-loss);
   p5low+=delta>0;
  }
 }
 if(a&&2*L<h)return 1;
 assert(!q2&&!u3&&!k&&!v2);p5upper++;
 assert(h<=2*K+2);
 long long bound=a?(a-1)*(b+1)+c*(c+e+1)+e*(3*a+2*b-1)+r*(q+s+t):c*(c+1)+e*(2*b+c)+r*t;
 assert(W>=bound);
 if(a&&W-bound<p5min)p5min=W-bound;
 if(W<p5amin)p5amin=W;
 if(a>p5maxa)p5maxa=a;if(b>p5maxb)p5maxb=b;
 p5class[0]+=a>0;p5class[1]+=b>0;p5class[2]+=c>0;p5class[3]+=e>0;
 if(a>=3&&b<=a+1)p5linear++;else if(a==2&&b<=1)p5linear++;else if(a>=2)p5curve++;
 return 1;
}
static void p5summary(void){
 printf("primary=%llu upper=%llu linear=%llu curvature=%llu low_instances=%llu adaptive=%llu LC=%llu classes=%llu,%llu,%llu,%llu max_a=%d max_b=%d minW=%d min_strong_slack=%d\n",
 (unsigned long long)p5primary,(unsigned long long)p5upper,(unsigned long long)p5linear,(unsigned long long)p5curve,(unsigned long long)p5low,(unsigned long long)p5adaptive,(unsigned long long)p5lc,
 (unsigned long long)p5class[0],(unsigned long long)p5class[1],(unsigned long long)p5class[2],(unsigned long long)p5class[3],p5maxa,p5maxb,p5amin,p5min);
}
