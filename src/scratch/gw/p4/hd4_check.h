/* Exact verifier of H4 for distinct weights and M>=6q-3.
 * All arithmetic and runs on fejer. q need not equal the cardinality.
 */
#ifndef HD4_CHECK_H
#define HD4_CHECK_H
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#define HN 128
static uint64_t hdchecks,hddeficits,hdcellcharges,hdcolcharges;
static int hdfind(int m,int d,const int *X,const int *x){
 for(int i=0;i<m;i++){int ok=1;for(int b=0;b<d;b++)if(X[i*d+b]!=x[b])ok=0;if(ok)return i;}return -1;
}
static int hdF(int v,int q){assert(v>=0);int k=v/q;return k<4?k:4;}
static void hd4verify(int m,int d,const int *X,const int *n,int q){
 for(int a=0;a<d;a++)for(int b=0;b<a;b++)if(n[a]==n[b])return;
 int V[HN],B[HN],M=0;assert(m<HN&&d<HN&&q>=1);
 for(int i=0;i<m;i++){
  V[i]=B[i]=0;for(int b=0;b<d;b++){assert(n[b]>q);V[i]+=X[i*d+b]*n[b];B[i]+=hdF(X[i*d+b]*n[b],q);}if(V[i]>M)M=V[i];
 }
 if(M<6*q-3)return;
 int J[HN*HN],CS[HN*HN],usedcol[HN*HN]={0},usedcell[HN]={0},sourcecol[HN*HN]={0};
 memset(J,-1,sizeof(J));memset(CS,0,sizeof(CS));
 int sep=0,lhs=0,rhs=0,surplus=0,deficits=0,totalcs=0;
 for(int i=0;i<m;i++){sep+=B[i];lhs+=hdF(V[i],q);rhs+=d*hdF(M-V[i],q);if(B[i]>hdF(V[i],q))surplus+=B[i]-hdF(V[i],q);}
 for(int b=0;b<d;b++)for(int i=0;i<m;i++)if(!X[i*d+b]){
  int x[HN];for(int a=0;a<d;a++)x[a]=X[i*d+a];int j=0,cs=0;
  for(;;j++){x[b]=j;int t=hdfind(m,d,X,x);if(t<0)break;cs+=hdF(M-V[t],q)-hdF(j*n[b],q);}
  assert(cs>=0);J[i*d+b]=j-1;CS[i*d+b]=cs;totalcs+=cs;
 }
 assert(rhs==sep+totalcs);
 for(int i=0;i<m;i++)if(B[i]<hdF(V[i],q)){
  assert(hdF(V[i],q)-B[i]==1);int b=-1,deg=0,supp=0,base[HN];
  for(int a=0;a<d;a++){
   base[a]=X[i*d+a];deg+=base[a];supp+=base[a]>0;
   if(base[a]&&(b<0||n[a]>n[b]||(n[a]==n[b]&&a>b)))b=a;
  }
  assert((deg==2||deg==3)&&supp>=2&&b>=0);
  int j0=base[b],basedeg=deg-j0;base[b]=0;int z=hdfind(m,d,X,base);assert(z>=0);
  int key=z*d+b;assert(!sourcecol[key]);sourcecol[key]=1;
  int jstar;
  if(basedeg==1){
   assert(j0==1||j0==2);
   if(j0==1&&n[b]>=2*q)jstar=2;else jstar=3;
  }else{assert(basedeg==2&&j0==1&&n[b]<2*q);jstar=2*n[b]>=3*q?2:3;}
  base[b]=jstar;int y=hdfind(m,d,X,base);
  if(y>=0){assert(!usedcell[y]);usedcell[y]=1;assert(B[y]-hdF(V[y],q)>=1);hdcellcharges++;}
  else{assert(J[key]<jstar&&CS[key]>=1&&!usedcol[key]);usedcol[key]=1;hdcolcharges++;}
  deficits++;
 }
 assert(sep-lhs==surplus-deficits);assert(deficits<=surplus+totalcs&&lhs<=rhs);
 hdchecks++;hddeficits+=deficits;
}
#endif
