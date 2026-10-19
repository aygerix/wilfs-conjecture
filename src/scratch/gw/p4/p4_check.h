/* Shared exact assertions; compile and run exclusively on fejer.
 * Rows X have stride d. The input is a residue-complete down-set.
 * The caller independently constructs/checks the down-set.
 */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "h4_check.h"
#define PMAX 128
static uint64_t pchecks, pquad, pnoa, psaturated, pshort, pcarry, pa2, pwaneg, pa3, pwa3neg;
static int pmin=1000000000;
static int p4verify(int m,int d,const int *X,const int *n){
 int V[PMAX],cls[PMAX],seen[PMAX]={0},M=0,deg[PMAX];
 assert(m<PMAX&&d<PMAX);
 for(int i=0;i<m;i++){
  V[i]=deg[i]=0;for(int j=0;j<d;j++){assert(n[j]>m);V[i]+=X[i*d+j]*n[j];deg[i]+=X[i*d+j];}
  assert(!seen[V[i]%m]);seen[V[i]%m]=1;if(V[i]>M)M=V[i];
 }
 int lhs=0,rhs=0;
 for(int i=0;i<m;i++){int k=V[i]/m,l=(M-V[i])/m;lhs+=k<4?k:4;rhs+=l<4?l:4;}
 assert(d*rhs>=lhs);
 h4verify(m,d,X,n,m);
 if(M/m!=4)return 0;
 int rho=5*m-1-M,a=0,b=0,c=0,e=0,maxdeg=0;
 for(int j=0;j<d;j++){cls[j]=(n[j]+rho)/m;assert(cls[j]>=1&&cls[j]<=4);a+=cls[j]==1;b+=cls[j]==2;c+=cls[j]==3;e+=cls[j]==4;}
 int q2=0,q3=0,s3=0,s4=0,h=0,t3=0,t4=0,bc=0,u3=0,u4=0,v2=0,v3=0,w=0,z=0,k4=0;
 int L=0,g=0,N=0,shortseen[PMAX]={0};
 for(int i=0;i<m;i++){
  int A=0,B=0,C=0,E=0,band=(V[i]+rho)/m;
  for(int j=0;j<d;j++){A+=X[i*d+j]*(cls[j]==1);B+=X[i*d+j]*(cls[j]==2);C+=X[i*d+j]*(cls[j]==3);E+=X[i*d+j]*(cls[j]==4);}
  int sh=0;L+=(M-V[i])/m;g+=V[i]/m;
  assert((M-V[i])/m==4-band);
  if(deg[i]>maxdeg)maxdeg=deg[i];assert(deg[i]<=4);
  if(deg[i]>=2)N++;
  if(deg[i]==2){
   assert(!E);
   if(A==2){assert(band==2||band==3);q2+=band==2;q3+=band==3;}
   else if(A==1&&B==1){assert(band==3||band==4);s3+=band==3;s4+=band==4;}
   else if(A==1&&C==1){assert(band==4);h++;}
   else if(B==2){assert(band==3||band==4);t3+=band==3;t4+=band==4;if(band==3){assert(V[i]>=4*m-2*rho&&V[i]<4*m-rho);sh=1;}}
   else {assert(B==1&&C==1&&band==4);bc++;assert(V[i]>=5*m-2*rho);sh=1;}
  }
  if(deg[i]==3){
   assert(!C&&!E);
   if(A==3){assert(band==3||band==4);u3+=band==3;u4+=band==4;}
   else if(A==2&&B==1){assert(band==4);int bv=0;for(int j=0;j<d;j++)if(cls[j]==2)bv+=X[i*d+j]*n[j];int ab=(V[i]-bv+rho)/m;assert(ab==2||ab==3);v2+=ab==2;v3+=ab==3;sh=ab==3;}
   else if(A==1&&B==2){assert(band==4);w++;assert(V[i]>=5*m-2*rho+1);sh=1;}
   else {assert(B==3&&band==4&&2*rho>=m+1);z++;assert(V[i]>=5*m-2*rho);sh=1;}
  }
  if(deg[i]==4){assert(A==4&&band==4);k4++;}
  if(sh){assert(!shortseen[V[i]%m]);shortseen[V[i]%m]=1;assert((V[i]%m+2*rho)%m<rho);}
  /* Exact divisor-band implications. */
  if(deg[i]>=3)for(int j=0;j<d;j++)if(X[i*d+j]){
   int dv=V[i]-n[j],db=(dv+rho)/m;
   if(A==3&&band==3)assert(db==2);
   if(deg[i]==4)assert(db==3);
   if(A==2&&B==1&&cls[j]==1)assert(db==3);
   if(A==1&&B==2)assert(db==3);
  }
 }
 int Q=a*(a+1)/2,U=a*(a+1)*(a+2)/6;
 assert(q2+q3<=Q&&s3+s4<=a*b&&t3+t4<=b*(b+1)/2&&h<=a*c&&bc<=b*c);
 assert(3*u3<=(a+2)*q2);
 assert(3*(u3+u4)<=(a+2)*(q2+q3));
 assert(4*k4<=(a+3)*u3);
 assert(2*(v2+v3)<=(a+1)*s3&&v2<=b*q2&&v3<=b*q3);
 assert(2*w<=(b+1)*s3&&w<=a*t3&&3*z<=(b+2)*t3);
 assert(t3+bc+v3+w+z<=rho);
 assert(m==1+d+N);
 assert(L==4+3*a+2*b+c+2*q2+q3+s3+t3+u3);
 assert(g+L==4*m-rho);
 int W=d*L-g;
 assert(W==(d+1)*(L-4)-4*N+rho&&W>=0);
 int WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+k4);
 int T=a*b-s3+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s3+t3+u3)+b*u3;
 int R=4*(a*b-s3-s4)+4*(a*c-h)+4*(b*(b+1)/2-t3-t4)
  +(rho-t3-bc-v3-w-z)+3*(b*c-bc)+((b+2)*t3-3*z)
  +(a*t3+(b+1)*s3-3*w)+(2*b*q2+b*q3+(a+1)*s3-4*v2-3*v3);
 assert(R>=0&&W==WA+T+R);
 assert(T>=0&&W>=WA+T);
 assert(3*WA>=18*(Q-q2-q3)-(a-1)*q3);
 int D3=(a+2)*(q2+q3)-3*(u3+u4),Dlow=(a+2)*q2-3*u3,D4=(a+3)*u3-4*k4;
 assert(3*WA==18*(Q-q2-q3)-(a-1)*q3+4*D3+2*Dlow+3*D4);
 if(a<=2){
  if(a<=1)assert(WA>=0);
  if(a==2&&WA<0){assert(WA==-1&&q2==0&&q3==3&&u3==0&&u4==4&&k4==0);pwaneg++;}
  assert(W>=0);pa2++;
 }
 if(a<=3){
  if(a==3&&WA<0){assert(WA==-4&&q2==0&&q3==6&&u3==0&&u4==10&&k4==0);pwa3neg++;}
  assert(W>=0);pa3++;
 }
 if(W<pmin)pmin=W;
 if(maxdeg<=2){
  int bound=3*a*(a+1)+a*b+c*(c+1)+e*(3*a+2*b+c);
  if(d>=3)assert(W>=bound);
  pquad++;
 }
 if(!a){
  int bound=c*(c+1)+e*(2*b+c)+(c+e)*t3;
  assert(W>=bound);pnoa++;
 }
 if(!rho&&a>=2&&q3==Q&&u4==U){
  assert(!q2&&!u3&&!k4&&!v2&&!v3&&!w&&!z&&!bc&&!t3);
  int F=a*(a+1)*(a-1)/6,k=d-a;
  int packed=(a+1)*(a*(a+1)/2+1);
  assert(m>=packed);
  assert(m<=(a+1)*(a+2)*(a+3)/6+k*(a+1)+k*(k+1)/2);
  assert(3*k>a-1);
  assert(W>=-F+k*Q&&W>0);psaturated++;
 }
 /* Carries = sum of cell deficits from separated untruncated floors. */
 int carry=0,CS=0;
 for(int i=0;i<m;i++){
  int sep=0,rs=0;for(int j=0;j<d;j++){sep+=X[i*d+j]*n[j]/m;rs+=X[i*d+j]*n[j]%m;}
  assert(V[i]/m-sep==rs/m);carry+=rs/m;
 }
 for(int j=0;j<d;j++)for(int i=0;i<m;i++)if(!X[i*d+j]){
  int J=0;for(int t=0;t<m;t++){
   int eq=1;for(int h=0;h<d;h++)if(h!=j&&X[t*d+h]!=X[i*d+h])eq=0;
   if(eq&&X[t*d+j]>J)J=X[t*d+j];
  }
  int delta=M-V[i]-J*n[j],lam=delta/m,eps=delta%m,sl=(J+1)*lam;
  for(int t=0;t<=J;t++)sl+=(t*n[j]%m)+eps>=m;
  CS+=sl;
 }
 assert(W==CS-carry);pcarry+=carry;
 pshort+=t3+bc+v3+w+z;pchecks++;return 1;
}
static void p4summary(void){
 printf("K4=%llu quadratic=%llu no_A=%llu saturated_rho0=%llu short_members=%llu carry_units=%llu minW=%d A_le2=%llu A2_negative_face=%llu A_le3=%llu A3_negative_face=%llu\n",
 (unsigned long long)pchecks,(unsigned long long)pquad,(unsigned long long)pnoa,
 (unsigned long long)psaturated,(unsigned long long)pshort,(unsigned long long)pcarry,pmin,
 (unsigned long long)pa2,(unsigned long long)pwaneg,(unsigned long long)pa3,(unsigned long long)pwa3neg);
 printf("H4=%llu deficits=%llu cell_charges=%llu column_charges=%llu\n",(unsigned long long)hchecks,(unsigned long long)hdeficits,(unsigned long long)hcellcharges,(unsigned long long)hcolcharges);
}
