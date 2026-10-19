/* Exact verifier of the residue-free sharp-cutoff theorem H4.
 * All arithmetic and runs on fejer. q need not equal the cardinality.
 */
#ifndef H4_CHECK_H
#define H4_CHECK_H
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#define HN 128
static uint64_t hchecks,hdeficits,hcellcharges,hcolcharges;
static int hfind(int m,int d,const int *X,const int *x){
 for(int i=0;i<m;i++){int ok=1;for(int b=0;b<d;b++)if(X[i*d+b]!=x[b])ok=0;if(ok)return i;}return -1;
}
static int hF(int v,int q){assert(v>=0);int k=v/q;return k<4?k:4;}
static void h4verify(int m,int d,const int *X,const int *n,int q){
 int V[HN],B[HN],M=0;assert(m<HN&&d<HN&&q>=1);
 for(int i=0;i<m;i++){
  V[i]=B[i]=0;for(int b=0;b<d;b++){assert(n[b]>q);V[i]+=X[i*d+b]*n[b];B[i]+=hF(X[i*d+b]*n[b],q);}if(V[i]>M)M=V[i];
 }
 if(M<6*q-1)return;
 int J[HN*HN],CS[HN*HN],usedcol[HN*HN]={0},usedcell[HN]={0},sourcecol[HN*HN]={0};
 memset(J,-1,sizeof(J));memset(CS,0,sizeof(CS));
 int sep=0,lhs=0,rhs=0,surplus=0,deficits=0,totalcs=0;
 for(int i=0;i<m;i++){sep+=B[i];lhs+=hF(V[i],q);rhs+=d*hF(M-V[i],q);if(B[i]>hF(V[i],q))surplus+=B[i]-hF(V[i],q);}
 for(int b=0;b<d;b++)for(int i=0;i<m;i++)if(!X[i*d+b]){
  int x[HN];for(int a=0;a<d;a++)x[a]=X[i*d+a];int j=0,cs=0;
  for(;;j++){x[b]=j;int t=hfind(m,d,X,x);if(t<0)break;cs+=hF(M-V[t],q)-hF(j*n[b],q);}
  assert(cs>=0);J[i*d+b]=j-1;CS[i*d+b]=cs;totalcs+=cs;
 }
 assert(rhs==sep+totalcs);
 for(int i=0;i<m;i++)if(B[i]<hF(V[i],q)){
  assert(hF(V[i],q)-B[i]==1);int b=-1,deg=0,supp=0,base[HN];
  for(int a=0;a<d;a++){
   base[a]=X[i*d+a];deg+=base[a];supp+=base[a]>0;
   if(base[a]&&(b<0||n[a]>n[b]||(n[a]==n[b]&&a>b)))b=a;
  }
  assert((deg==2||deg==3)&&supp>=2&&b>=0);
  int j0=base[b],basedeg=deg-j0;base[b]=0;int z=hfind(m,d,X,base);assert(z>=0);
  int key=z*d+b;assert(!sourcecol[key]);sourcecol[key]=1;
  int jstar;
  if(basedeg==1){
   assert(j0==1||j0==2);
   if(j0==1&&n[b]>=2*q)jstar=2;else jstar=3;
  }else{assert(basedeg==2&&j0==1&&n[b]<2*q);jstar=2*n[b]>=3*q?2:3;}
  base[b]=jstar;int y=hfind(m,d,X,base);
  if(y>=0){assert(!usedcell[y]);usedcell[y]=1;assert(B[y]-hF(V[y],q)>=1);hcellcharges++;}
  else{assert(J[key]<jstar&&CS[key]>=1&&!usedcol[key]);usedcol[key]=1;hcolcharges++;}
  deficits++;
 }
 assert(sep-lhs==surplus-deficits);assert(deficits<=surplus+totalcs&&lhs<=rhs);
 hchecks++;hdeficits+=deficits;
}
#endif
