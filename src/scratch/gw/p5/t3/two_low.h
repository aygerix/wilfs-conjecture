/* T2.2: independent cell counts for the two-low payment. fejer only. */
#ifndef P7_TWO_LOW_H
#define P7_TWO_LOW_H
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
static long long p7_primary,p7_two,p7_neg,p7_missing,p7_full,p7_sid,p7_a7,p7_qgap;
static long long p7_l0,p7_l1,p7_fixednegative,p7_a7beta3,p7_a7R5;
static long long p7_min_p=1000000000,p7_min_ref=1000000000,p7_min_h=1000000000;
static long long p7_currentP,p7_currentPD;
static const int *p7_failF,*p7_failDeg;
static long long p7_c2(long long z){return z*(z-1)/2;}
static long long p7_c3(long long z){return z*(z-1)*(z-2)/6;}
static void p7need(int ok,const char *label,int m,int d,const int *X,const int *n){
 if(ok)return;
 fprintf(stderr,"P7 FAILURE %s m=%d d=%d weights=",label,m,d);
 for(int j=0;j<d;j++)fprintf(stderr,"%s%d",j?",":"",n[j]);
 fprintf(stderr,"\nD=\n");
 for(int i=0;i<m;i++){
  if(X)for(int j=0;j<d;j++)fprintf(stderr,"%s%d",j?",":"",X[i*d+j]);
  else for(int j=0;j<p7_failDeg[i];j++)fprintf(stderr,"%s%d",j?",":"",p7_failF[4*i+j]);
  fputc('\n',stderr);
 }
 fflush(stderr);exit(19);
}
static int p7inside(int r,int h,int theta,int m){return (h<=r&&r<theta)||(1<=r&&r<theta-m);}
static void p7sparse(int m,int d,const int *F,const int *dg0,const int *n){
 const int *X=NULL;p7_failF=F;p7_failDeg=dg0;
 int M=0;
 for(int i=0;i<m;i++){int v=0;for(int j=0;j<dg0[i];j++)v+=n[F[4*i+j]];if(v>M)M=v;}
 if(M/m!=4)return;
 p7_primary++;
 int h=M-4*m+1,a=0,b=0,c=0,e=0,alpha=0,L=m,p=0;
 int *cl=malloc(d*sizeof(int)),*lo=calloc(d,sizeof(int));
 for(int j=0;j<d;j++){
  cl[j]=(n[j]+m-h)/m;
  a+=cl[j]==1;b+=cl[j]==2;c+=cl[j]==3;e+=cl[j]==4;
  if(cl[j]==1){if(n[j]-m<L)L=n[j]-m;lo[j]=2*(n[j]-m)<h;alpha+=lo[j];p+=3*(n[j]-m)>=2*h;}
 }
 if(a<7||alpha!=2){free(cl);free(lo);return;}
 p7_two++;
 int theta=(3*h+1)/2,HH=h-L,delta=h-2*L;
 int q2=0,q3=0,u3=0,u4=0,k=0,s3=0,s4=0,t3=0,t4=0,Hac=0,Ibc=0;
 int J=0,JA=0,JH=0,JHA=0,K=0,n0=0,l=0,l1=0,l2=0,u0=0,u1=0,k0=0,k1=0,c0=0,qcold=0,beta=0;
 int low_id[2],lowpos=0;for(int j=0;j<d;j++)if(lo[j])low_id[lowpos++]=j;
 long long ell=0,g=0;
 for(int i=0;i<m;i++){
  int v=0,dg=dg0[i],A=0,B=0,C=0,LL=0,LL1=0,LL2=0;
  for(int j=0;j<dg;j++){int z=F[4*i+j];v+=n[z];A+=cl[z]==1;B+=cl[z]==2;C+=cl[z]==3;LL+=lo[z];LL1+=z==low_id[0];LL2+=z==low_id[1];}
  int band=(v+m-h)/m,tau=v-dg*m,r=v%m;
  ell+=(M-v)/m;g+=v/m;
  q2+=dg==2&&A==2&&band==2;q3+=dg==2&&A==2&&band==3;
  u3+=dg==3&&A==3&&band==3;u4+=dg==3&&A==3&&band==4;k+=dg==4;
  s3+=dg==2&&A==1&&B==1&&band==3;s4+=dg==2&&A==1&&B==1&&band==4;
  t3+=dg==2&&B==2&&band==3;t4+=dg==2&&B==2&&band==4;
  Hac+=dg==2&&A==1&&C==1;Ibc+=dg==2&&B==1&&C==1;
  if(dg==2&&A==2&&band==2){
   if(LL==2)n0++;
   else {p7need(LL==1,"low-pair type",m,d,X,n);l++;l1+=LL1;l2+=LL2;}
  }
  if(dg==3&&A==3&&band==3){if(LL==3)u0++;else {p7need(LL==2,"low cubic type",m,d,X,n);u1++;}}
  if(dg==4){if(LL==4)k0++;else {p7need(LL==3,"quartic type",m,d,X,n);k1++;}}
  c0+=dg==3&&LL==3;
  qcold+=dg==2&&LL==2&&p7inside(r,h,theta,m);
  beta+=dg==2&&LL==2&&tau<theta-h;
  int allowed=(dg==1&&A==0)||(dg==2&&A==2&&band==3)||(dg==2&&A==1&&B==1&&band==4)||(dg==2&&B==2&&band==4);
  K+=allowed;
  if(!allowed&&p7inside(r,h,theta,m)){J++;JA+=A==dg;}
  if(!allowed&&p7inside(r,h,h+HH,m)){JH++;JHA+=A==dg;}
 }
 long long Q=p7_c2(a+1),q=q2+q3,ra=Q-q,ta=p7_c3(a+2)-u3-u4,D3=3*ta-(a+2)*ra;
 long long LC=(a+1LL)*(q2+u3)-4*k,WA=3LL*a*(a+1)+(a-3LL)*q-4LL*(u3+u4)+LC;
 long long P=a-1+LC+2*q2+k-2*JA,PH=a-1+LC+2*q2+k+delta-2*JHA;
 p7_currentP=P;p7_currentPD=P+D3;
 if(P<p7_min_p)p7_min_p=P;
 p7need(q2==n0+l&&u3==u0+u1&&k==k0+k1,"low accounting",m,d,X,n);
 p7need(3*k1<=4*u1,"two-variable cubic link",m,d,X,n);
 p7need(4*k0<=5*u0,"two-variable quartic link",m,d,X,n);
 p7need(J-JA<=b*(2+n0)+2*c,"fixed outside",m,d,X,n);
 p7need(J-JA<=b*(2+beta)+2*c,"fixed outside beta",m,d,X,n);
 p7need(P>=a-13+(5-a)*n0+l1*(a+2-l1)+l2*(a+2-l2),"rough OL2",m,d,X,n);
 p7need(P>=2-2*a,"rough OL2 uniform",m,d,X,n);
 if(q>=2&&ra>0){p7_qgap++;p7need(D3>=2*a-2,"Macaulay gap",m,d,X,n);p7need(P+D3>=0,"missing-pair OL2",m,d,X,n);}
 if(ra==0){
  p7_full++;
  if(l>=2)p7need(P>=2,"two-star OL2",m,d,X,n);
  else {
   p7_sid++;int R=0;for(int j=0;j<d;j++)R+=cl[j]==1&&!lo[j]&&n[j]-m<theta-2*L;
   p7_l0+=l==0;p7_l1+=l==1;p7_fixednegative+=P+D3<0;p7_a7R5+=a==7&&l==0&&R==5;
   int nn=R-l;if(nn<0)nn=0;
   p7need(n0==3,"full low pairs",m,d,X,n);
   p7need(nn*(nn-1)<=delta-1,"Sidon interval",m,d,X,n);
   p7need((a+1)*u0-5*k0+3*(4-c0)>=2*qcold,"cold pair payment",m,d,X,n);
   long long ref=P+D3-(4*a-4+(a+1)*l-6*R);if(ref<p7_min_ref)p7_min_ref=ref;
   p7need(ref>=0,"refined fixed OL2",m,d,X,n);
   long long hslack=PH-(delta-(2*a-2)-(3*a-5)*l);if(hslack<p7_min_h)p7_min_h=hslack;
   p7need(hslack>=0,"high arc OL2",m,d,X,n);
   p7need(JH-JHA<=b*(2+l+q2)+c*(2+l),"high outside",m,d,X,n);
   p7need(P+D3>=0||PH>=0,"Sidon arc alternative",m,d,X,n);
  }
 }
 long long G=c*(c+e+1LL)+e*(3*a+2*b-1LL)+(c+e)*(q3+s3+t3);
 long long A2=(a-1LL)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3)+D3;
 long long Cfixed=A2+(b+2LL)*q2+k-2*J,Chigh=A2+(b+2LL)*q2+k+delta-2*JH;
 long long Trans=a*b-s3+c*(c+1LL)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s3+t3+u3)+b*u3;
 long long HIGH=LC+p7_c3(p+2)-p7_c3(a+1)+5*ra+D3+Trans;
 long long W=d*ell-g;
 long long fLoss=2*J-(b+2LL)*q2-k,hLoss=-delta+2*JH-(b+2LL)*q2-k;
 if(fLoss<0)fLoss=0;
 if(hLoss<0)hLoss=0;
 p7need(W>=A2-fLoss&&W>=A2-hLoss,"actual I-LOW",m,d,X,n);
 p7need(W>=HIGH,"actual HIGH",m,d,X,n);
 p7need(HH<=K+JH+1,"H0 arc coverage",m,d,X,n);
 if(WA<0){
  p7_neg++;p7_missing+=ra>0;p7_a7+=a==7;
  p7need(q>=2,"deficient q",m,d,X,n);
  if(a==7&&n0==3&&q2==3&&u3==0){
   p7need(ra<=1,"a7 small-r",m,d,X,n);
   if(beta==3)p7need(HIGH>=0,"a7 beta3 HIGH",m,d,X,n);
   p7_a7beta3+=beta==3;
  }
  p7need(Cfixed>=0||Chigh>=0||HIGH>=0,"complete two-low alternative",m,d,X,n);
 }
 p7need(W>=0,"WILF",m,d,X,n);
 free(cl);free(lo);(void)s4;(void)t4;(void)Hac;(void)Ibc;
}
static void p7verify(int m,int d,const int *X,const int *n){
 int M=0;for(int i=0;i<m;i++){int v=0;for(int j=0;j<d;j++)v+=X[i*d+j]*n[j];if(v>M)M=v;}
 if(M/m!=4)return;
 int *F=calloc((size_t)4*m,sizeof(int)),*dg=calloc(m,sizeof(int));
 for(int i=0;i<m;i++)for(int j=0;j<d;j++)for(int z=0;z<X[i*d+j];z++){assert(dg[i]<4);F[4*i+dg[i]++]=j;}
 p7sparse(m,d,F,dg,n);free(F);free(dg);
}
static void p7summary(void){
 printf("P7 primary=%lld two_low_a_ge7=%lld negative_WA=%lld negative_missing_pair=%lld full_quadratic=%lld sidon_branches=%lld a7_negative=%lld qgap_checks=%lld min_P=%lld min_refined_slack=%lld min_high_slack=%lld\n",p7_primary,p7_two,p7_neg,p7_missing,p7_full,p7_sid,p7_a7,p7_qgap,p7_min_p,p7_min_ref,p7_min_h);
 printf("P7_BRANCHES full_l0=%lld full_l1=%lld actual_fixed_payment_negative=%lld a7_beta3=%lld a7_l0_R5=%lld\n",p7_l0,p7_l1,p7_fixednegative,p7_a7beta3,p7_a7R5);
}
#endif
