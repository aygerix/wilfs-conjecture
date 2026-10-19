/* Additional actual-instance assertions for P5 continuation; fejer only. */
#include "p5_check.h"
static uint64_t n6,ng6,nlow6,none6,nplus6,nsr6,nclosed6,ncore6;
static int smallest_missing=1000000,closest6=-1000000000;
static int p6verify(int m,int d,const int*X,const int*n){
 p5verify(m,d,X,n);
 int M=0,V[PMAX],cl[PMAX],deg[PMAX];
 for(int i=0;i<m;i++){V[i]=deg[i]=0;for(int j=0;j<d;j++){V[i]+=X[i*d+j]*n[j];deg[i]+=X[i*d+j];}if(V[i]>M)M=V[i];}
 if(M/m!=4)return 0;
 int h=M-4*m+1,rho=m-h,a=0,b=0,c=0,e=0,al=0,p=0,L=m;
 for(int j=0;j<d;j++){cl[j]=(n[j]+rho)/m;a+=cl[j]==1;b+=cl[j]==2;c+=cl[j]==3;e+=cl[j]==4;if(cl[j]==1){al+=2*(n[j]-m)<h;p+=3*(n[j]-m)>=2*h;if(n[j]-m<L)L=n[j]-m;}}
 int q2=0,q3=0,u3=0,u4=0,k4=0,s=0,t=0,S4=0,T4=0,Hac=0,Ibc=0,SR=0,hot=0,J=0,JA=0,ell=0,g=0,K=0,bad[PMAX];
 int theta=(3*h+1)/2;
 for(int i=0;i<m;i++){
  int A=0,B=0,C=0,E=0,band=(V[i]+rho)/m;
  ell+=(M-V[i])/m;g+=V[i]/m;
  for(int j=0;j<d;j++){A+=X[i*d+j]*(cl[j]==1);B+=X[i*d+j]*(cl[j]==2);C+=X[i*d+j]*(cl[j]==3);E+=X[i*d+j]*(cl[j]==4);}
  q2+=deg[i]==2&&A==2&&band==2;q3+=deg[i]==2&&A==2&&band==3;
  u3+=deg[i]==3&&A==3&&band==3;u4+=deg[i]==3&&A==3&&band==4;k4+=deg[i]==4;
  s+=deg[i]==2&&A==1&&B==1&&band==3;t+=deg[i]==2&&B==2&&band==3;
  S4+=deg[i]==2&&A==1&&B==1&&band==4;T4+=deg[i]==2&&B==2&&band==4;
  Hac+=deg[i]==2&&A==1&&C==1;Ibc+=deg[i]==2&&B==1&&C==1;
  hot+=deg[i]==3&&A==3&&V[i]-3*m>=2*h;
  if(deg[i]==2&&B==2&&band==3)SR++;
  if(deg[i]==2&&B==1&&C==1)SR++;
  if(deg[i]==3&&A==2&&B==1){int bv=0;for(int j=0;j<d;j++)if(cl[j]==2)bv+=n[j]*X[i*d+j];if((V[i]-bv+rho)/m==3)SR++;}
  if(deg[i]==3&&((A==1&&B==2)||B==3))SR++;
  int rr=V[i]%m,iny=(h<=rr&&rr<theta)||(1<=rr&&rr<theta-m);
  int allowed=(deg[i]==1&&A==0)||(deg[i]==2&&A==2&&band==3)||(deg[i]==2&&A==1&&B==1&&band==4)||(deg[i]==2&&B==2&&band==4);
  bad[i]=!allowed;K+=allowed;
  if(iny&&!allowed){J++;if(A==deg[i])JA++;}
 }
 long long Q=C2(a+1),Ca=C3(a+1),ra=Q-q2-q3,ta=C3(a+2)-u3-u4;
 long long LC=(a+1)*(q2+u3)-4*k4;
 int WA=3*a*(a+1)+(2*a-2)*q2+(a-3)*(q3+u3)-4*(u4+k4),W=d*ell-g;
 int Trans=a*b-s+c*(c+1)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s+t+u3)+b*u3;
 assert(SR+hot<=rho);assert(W>=WA+Trans+hot);
 long long D3=3*ta-(a+2)*ra;
 assert(W>=LC+C3(p+2)-Ca+5*ra+D3+Trans);
 assert(q2+ra>=C2(al+1));
 if(q2<C2(al+1)&&m<smallest_missing){
  smallest_missing=m;printf("low_pair_omission m=%d h=%d alpha=%d q2=%d ra=%lld weights=",m,h,al,q2,ra);for(int j=0;j<d;j++)printf("%s%d",j?",":"",n[j]);puts("");
 }
 n6++;
 if(a>=3){
  int delta=h-2*L;if(delta<0)delta=0;
  int eta=3*delta;if(2*J<eta)eta=2*J;
  for(int j=0;j<d;j++)if(cl[j]==1&&2*(n[j]-m)>=h){
   int HH=n[j]-m,th=h+HH,JH=0;
   for(int i=0;i<m;i++){
    int rr=V[i]%m,inside=(h<=rr&&rr<th)||(1<=rr&&rr<th-m);
    if(inside&&bad[i]){
     JH++;int outsider=0;for(int k=0;k<d;k++)if(X[i*d+k]&&cl[k]==1&&n[k]-m<HH)outsider=1;
     assert(outsider);
    }
   }
   assert(HH<=K+JH+1);ncore6++;
   int lossH=h-2*HH+2*JH;if(lossH<eta)eta=lossH;
  }
  long long G=c*(c+e+1)+e*(3*a+2*b-1)+(c+e)*(q3+s+t);
  long long low=(a-1)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3);
  long long Cdef=D3+4*(a*b-s-S4+C2(b+1)-t-T4)+3*(a*c-Hac)+3*(b*c-Ibc);
  int loss=eta-(b+2)*q2-k4;if(loss<0)loss=0;
  assert(W>=low+Cdef-loss);ng6++;
  if(WA<0){assert(LC>=(a+1)*q2);assert(4*mac2(q2+q3)>3*a*(a+1)+(a-3)*(q2+q3)+LC);}
  if(a>=6&&al==1){assert(2*JA<=a-1+LC+2*q2+k4);assert(W>=0);none6++;}
  if(a>=7){
   nlow6+=al>0;
   long long mn=(a+1)*q2;if(mn>Ca)mn=Ca;
   int margin=3*delta-((a-1)*(b+1)+G+mn+(b+2)*q2+b*u3+k4+(c+e)*(2*q2+u3));
   if(WA<0&&al>0){
    if(margin>closest6)closest6=margin;
    if(margin>0){nplus6++;if(LC+C3(p+2)-Ca+5*ra+D3+Trans>=0||al<=1)nclosed6++;}
   }
  }
 }
 (void)ta;return 1;
}
static void p6summary(void){
 p5summary();printf("continuation primary=%llu general_arc=%llu high_arcs=%llu one_low=%llu low_a_ge7=%llu old_frontier=%llu new_closed=%llu closest_LOW_deficit=%d smallest_low_pair_omission_m=%d\n",(unsigned long long)n6,(unsigned long long)ng6,(unsigned long long)ncore6,(unsigned long long)none6,(unsigned long long)nlow6,(unsigned long long)nplus6,(unsigned long long)nclosed6,closest6,smallest_missing);
}
