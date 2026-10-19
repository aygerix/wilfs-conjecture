/* P5f checks; include after the unchanged P5e multi_low.h. */
#include <math.h>
static long long fcount,farc,fstrong,fneg,flarge;
static long long fC(int n,int k){
 if(n<k)return 0;long long z=1;for(int j=1;j<=k;j++)z=z*(n-j+1)/j;return z;
}
static long long fmac(long long q,int deg){
 long long out=0;int top=100000;
 for(int j=deg;j;j--){int z=j-1;while(z+1<top&&fC(z+1,j)<=q)z++;
  out+=fC(z+1,j+1);q-=fC(z,j);top=z;}
 assert(!q);return out;
}
static void fverify(int m,int d,const int *F,const int *dg,const int *n){
 int M=0;for(int i=0;i<m;i++){int v=0;for(int j=0;j<dg[i];j++)v+=n[F[4*i+j]];if(v>M)M=v;}
 if(M/m!=4)return;fcount++;
 int h=M-4*m+1,a=0,b=0,alpha=0,L=m;
 int *cl=calloc(d,sizeof(int)),*lo=calloc(d,sizeof(int));
 for(int j=0;j<d;j++){cl[j]=(n[j]+m-h)/m;if(cl[j]==1){a++;lo[j]=2*(n[j]-m)<h;alpha+=lo[j];if(n[j]-m<L)L=n[j]-m;}b+=cl[j]==2;}
 int p=a-alpha,exc=0;for(int j=0;j<d;j++)exc+=cl[j]==1&&!lo[j]&&n[j]-m<h-L;
 int n0=0,l=0,c0=0,k=0,u3=0,u4=0,q=0,q2=0,ja0=0,hhl=0;long long ell=0,g=0;
 for(int i=0;i<m;i++){
  int tau=0,A=0,B=0,nlo=0;
  for(int j=0;j<dg[i];j++){int z=F[4*i+j];tau+=n[z]-m;A+=cl[z]==1;B+=cl[z]==2;nlo+=lo[z];}
  if(dg[i]==2&&A==2){q++;q2+=tau<h;if(nlo==2)n0++;else if(nlo==1&&tau<h)l++;}
  c0+=dg[i]==3&&nlo==3;k+=dg[i]==4;
  if(dg[i]==3&&A==3){u3+=tau<h;u4+=tau>=h;}
  int allowed=(dg[i]==1&&!A)||(dg[i]==2&&A==2&&tau>=h)||(dg[i]==2&&A==1&&B==1&&tau>=m+h)||(dg[i]==2&&B==2&&tau>=m+h);
  int r=tau%m,inside=p7inside(r,h,2*h-L,m);
  int val=dg[i]*m+tau;ell+=(M-val)/m;g+=val/m;
  if(inside&&!allowed&&A==dg[i]){ja0++;hhl+=dg[i]==3&&nlo==1;}
 }
 p7need(k<=fmac(u3,3),"P5f global quartic Macaulay",m,d,NULL,n);
 long long WA=3LL*a*(a+1)+(a-3LL)*q-4LL*(u3+u4)+(a+1LL)*(q2+u3)-4LL*k;
 if(alpha){
  p7need(l<=alpha*exc,"P5f exception pair incidence",m,d,NULL,n);
  long long mixed=1LL*l*(p-exc)+alpha*fC(exc+1,2);
  p7need(hhl<=mixed,"P5f H0 mixed intruders",m,d,NULL,n);
  long long cp=alpha+n0+c0+l+exc+fC(exc+2,3)+1LL*n0*p+mixed;
  long long old=alpha+n0+c0+l+exc+fC(exc+2,3)+(n0+1LL*alpha*exc)*p;
  p7need(ja0<=cp+k&&cp<=old,"P5f HPAIR total",m,d,NULL,n);
  farc++;fstrong+=cp<old;
 }
 if(WA<0&&a>=24){
  p7need(2LL*u3<1LL*a*a,"P5f universal low cubic bound",m,d,NULL,n);
  int j=0;while(fC(j+2,2)<=q)j++;
  p7need(2*j>a,"P5f deficient Macaulay block",m,d,NULL,n);fneg++;
 }
 if(alpha>=4&&a>=16*fC(alpha+1,2)){p7need(d*ell-g>=0,"P5f quadratic LARGE-A",m,d,NULL,n);flarge++;}
 free(cl);free(lo);
}
static void fsummary(void){printf("P5f instances=%lld HPAIR=%lld strict_improvements=%lld WAneg_a24=%lld large_hyp=%lld\n",fcount,farc,fstrong,fneg,flarge);}
