/* Additional a=4 continuation predicates; execute only on fejer. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include "hd4_check.h"
#include "fiber_check.h"
static uint64_t a4seen,a4negative,a4types[6],a4badneighbors,a4lowquartic,a5seen;
static int a4minnegative=1000000000;
static void a4verify(int m,int d,const int *X,const int *n){
 fiberverify(m,d,X,n);
 hd4verify(m,d,X,n,m);
 int M=0,V[128],cl[128];
 for(int i=0;i<m;i++){V[i]=0;for(int j=0;j<d;j++)V[i]+=X[i*d+j]*n[j];if(V[i]>M)M=V[i];}
 if(M/m!=4)return;
 int rho=5*m-1-M,a=0,b=0,ai[128],bi[128];
 for(int j=0;j<d;j++){cl[j]=(n[j]+rho)/m;if(cl[j]==1)ai[a++]=j;if(cl[j]==2)bi[b++]=j;}
 if(a==5)a5seen++;
 if(a!=4)return;
 a4seen++;
 int q2=0,q3=0,u3=0,u4=0,k=0,s3=0,t3=0,t4=0,w=0,z=0,v2[128]={0},v3[128]={0};
 int adj[4][128]={{0}},BB3[128]={0};
 for(int i=0;i<m;i++){
  int A=0,Bb=0,deg=0,band=(V[i]+rho)/m;
  for(int j=0;j<d;j++){deg+=X[i*d+j];A+=X[i*d+j]*(cl[j]==1);Bb+=X[i*d+j]*(cl[j]==2);}
  if(deg==2&&A==2){q2+=band==2;q3+=band==3;}
  if(deg==3&&A==3){u3+=band==3;u4+=band==4;}
  if(deg==4&&A==4)k++;
  if(deg==2&&A==1&&Bb==1&&band==3){
   s3++;for(int x=0;x<4;x++)for(int y=0;y<b;y++)if(X[i*d+ai[x]]&&X[i*d+bi[y]])adj[x][y]=1;
  }
  if(deg==2&&Bb==2){t3+=band==3;t4+=band==4;BB3[i]=band==3;}
  if(deg==3&&A==2&&Bb==1){
   for(int y=0;y<b;y++)if(X[i*d+bi[y]]){
    int aa=(V[i]-n[bi[y]]+rho)/m;if(aa==2)v2[y]++;else{assert(aa==3);v3[y]++;}
   }
  }
  if(deg==3&&A==1&&Bb==2)w++;
  if(deg==3&&Bb==3)z++;
 }
 int WA=60+6*q2+q3+u3-4*(u4+k);
 if(WA>=0)return;
 a4negative++;assert(q2+q3==10);
 int typ=-1;
 if(!q2){assert(!u3&&!k&&u4>=18&&u4<=20);typ=20-u4;assert(WA==-10+4*typ);}
 if(q2==1&&!u3){assert(!k&&u4>=19&&u4<=20);typ=3+20-u4;assert(WA==-5+4*(20-u4));}
 if(q2==1&&u3==1){assert(k==1&&u4==19&&WA==-4);typ=5;a4lowquartic++;}
 assert(typ>=0);a4types[typ]++;
 int p=4*b-s3;
 for(int y=0;y<b;y++){
  int r=0,qlow=0;for(int x=0;x<4;x++)r+=adj[x][y];int missing=4-r;
  for(int i=0;i<m;i++){
   int aa=0,deg=0,ok=1;
   for(int j=0;j<d;j++){deg+=X[i*d+j];aa+=X[i*d+j]*(cl[j]==1);}
   if(deg!=2||aa!=2||(V[i]+rho)/m!=2)continue;
   for(int x=0;x<4;x++)if(X[i*d+ai[x]]&&!adj[x][y])ok=0;
   qlow+=ok;
  }
  int Dv=2*q2+q3+5*r-4*v2[y]-3*v3[y];
  int lower=missing*(19-3*missing)/2+q2-qlow;
  assert(missing+Dv>=lower);
  if(missing){assert(missing+Dv>=8);a4badneighbors++;}
 }
 int Bcap=b*(b+1)/2,Z=b*(b+1)*(b+2)/6,Dw=4*t3+(b+1)*s3-3*w;
 if(!p)assert(Dw>=8*(Bcap-t3));
 if(Bcap>t3)assert(Z-z>=b);
 if(p==1&&t3+t4==Bcap){
  int bad=-1;for(int y=0;y<b;y++){int r=0;for(int x=0;x<4;x++)r+=adj[x][y];if(r==3)bad=y;}
  assert(bad>=0);int L=0;for(int i=0;i<m;i++)if(BB3[i]&&X[i*d+bi[bad]])L++;
  assert(w<=4*t3-L&&Dw>=5*t4+2*b-1);
 }
 int ell=0;for(int i=0;i<m;i++)ell+=(M-V[i])/m;int W=(d+1)*ell-(4*m-rho);
 assert(W>=0);if(W<a4minnegative)a4minnegative=W;
}
static void a4summary(void){
 printf("A4=%llu negative_faces=%llu types=",(unsigned long long)a4seen,(unsigned long long)a4negative);
 for(int j=0;j<6;j++)printf("%s%llu",j?",":"",(unsigned long long)a4types[j]);
 printf(" bad_neighbors=%llu quartic_faces=%llu min_negative_face_W=%d\n",(unsigned long long)a4badneighbors,(unsigned long long)a4lowquartic,a4minnegative);
 printf("HD4=%llu deficits=%llu cell_charges=%llu column_charges=%llu\n",(unsigned long long)hdchecks,(unsigned long long)hddeficits,(unsigned long long)hdcellcharges,(unsigned long long)hdcolcharges);
 printf("A5=%llu\n",(unsigned long long)a5seen);
 fibersummary();
}
