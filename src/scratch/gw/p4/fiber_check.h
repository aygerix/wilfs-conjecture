/* Actual-residue checks of SP and HP on full-quadratic faces, fejer only. */
#ifndef FIBER_CHECK_H
#define FIBER_CHECK_H
#include <assert.h>
#include <stdint.h>
static uint64_t fiberfaces,fiberhp,fiberheavy,a6seen,a7seen,lcfaces,neighborchecks;
static int fibergcd(int x,int y){while(y){int z=x%y;x=y;y=z;}return x;}
static int fiberL2(int s){if(s==2)return 2;if(s==3)return 4;if(s==4)return 8;return 3*(s-(s%3!=0));}
static void fiberface(int m,int d,const int *X,const int *n,const int *ids,int k){
 if(k<1||k*(k+1)/2>m-1-k)return;
 int inside[128]={0},count=0;
 for(int j=0;j<k;j++)inside[ids[j]]=1;
 for(int i=0;i<m;i++){
  int deg=0,ok=1;for(int j=0;j<d;j++){deg+=X[i*d+j];if(X[i*d+j]&&!inside[j])ok=0;}
  count+=(deg==2&&ok);
 }
 if(count!=k*(k+1)/2)return;
 int s=k+1,R[128],pairs[128]={0};R[0]=0;for(int j=0;j<k;j++)R[j+1]=n[ids[j]]%m;
 for(int i=0;i<s;i++)for(int j=i;j<s;j++){int r=(R[i]+R[j])%m;assert(!pairs[r]);pairs[r]=1;}
 int freq[128]={0},support_sum[128]={0},allthree[128],total=0,used=0;unsigned masks[128]={0};
 for(int r=0;r<m;r++)allthree[r]=1;
 for(int i=0;i<s;i++)for(int j=i;j<s;j++)for(int z=j;z<s;z++){
  unsigned mask=(1u<<i)|(1u<<j)|(1u<<z);int size=__builtin_popcount(mask),r=(R[i]+R[j]+R[z])%m;
  assert(!(masks[r]&mask));masks[r]|=mask;support_sum[r]+=size;allthree[r]&=(size==3);
  used+=freq[r]==0;freq[r]++;total++;
 }
 int excess=total-used,H=s*(s*(s-1)/2+1);
 assert(2*m>=2*H-fiberL2(s)*excess);fiberfaces++;
 if(s>=6&&s%3==0){
  int g=s/3,heavy=0;
  for(int r=0;r<m;r++)if(freq[r]==g&&allthree[r]&&support_sum[r]==s)heavy++;
  assert(heavy<=fibergcd(g,m));
  assert(2*m>=2*H-(3*s-6)*excess-6*(g-1)*fibergcd(g,m));fiberhp++;fiberheavy+=heavy;
 }
}
static void fiberverify(int m,int d,const int *X,const int *n){
 int ids[128];for(int j=0;j<d;j++)ids[j]=j;fiberface(m,d,X,n,ids,d);
 int M=0,V[128];for(int i=0;i<m;i++){int v=0;for(int j=0;j<d;j++)v+=X[i*d+j]*n[j];V[i]=v;if(v>M)M=v;}
 if(M/m!=4)return;
 int rho=5*m-1-M,a=0,cl[128];for(int j=0;j<d;j++){cl[j]=(n[j]+rho)/m;if(cl[j]==1)ids[a++]=j;}
 a6seen+=(a==6);a7seen+=(a==7);fiberface(m,d,X,n,ids,a);
 if(a<3)return;
 int q2=0,q3=0,u3=0,k=0;
 for(int i=0;i<m;i++){
  int deg=0,adeg=0;for(int j=0;j<d;j++){deg+=X[i*d+j];adeg+=X[i*d+j]*(cl[j]==1);}
  if(deg!=adeg)continue;
  int band=(V[i]+rho)/m;
  q2+=(deg==2&&band==2);q3+=(deg==2&&band==3);u3+=(deg==3&&band==3);k+=(deg==4);
 }
 int L=(a+1)*(q2+u3)-4*k,F=a*(a-1)*(a+1)/6,base=(a+1)*q2;
 assert(L>=(base<F?base:F));lcfaces++;
 if(q2+q3!=a*(a+1)/2)return;
 for(int bj=0;bj<d;bj++)if(cl[bj]==2){
  int adj[128]={0},r=0,v2=0,v3=0;
  for(int i=0;i<m;i++)if(X[i*d+bj]){
   int deg=0,adeg=0;for(int j=0;j<d;j++){deg+=X[i*d+j];adeg+=X[i*d+j]*(cl[j]==1);}
   if(deg==2&&adeg==1&&(V[i]+rho)/m==3)for(int j=0;j<a;j++)if(X[i*d+ids[j]])adj[j]=1;
   if(deg==3&&adeg==2){int aa=(V[i]-n[bj]+rho)/m;v2+=aa==2;v3+=aa==3;}
  }
  for(int j=0;j<a;j++)r+=adj[j];
  int lowin=0;
  for(int i=0;i<m;i++)if((V[i]+rho)/m==2){
   int deg=0,adeg=0,ok=1;for(int j=0;j<d;j++){deg+=X[i*d+j];adeg+=X[i*d+j]*(cl[j]==1);}
   if(deg!=2||adeg!=2)continue;
   for(int j=0;j<a;j++)if(X[i*d+ids[j]]&&!adj[j])ok=0;lowin+=ok;
  }
  int p=a-r,Dv=2*q2+q3+(a+1)*r-4*v2-3*v3;
  assert(p+Dv>=p*(4*a+3-3*p)/2+q2-lowin);neighborchecks++;
 }
}
static void fibersummary(void){
 printf("FIBER faces=%llu HP=%llu full_support_fibers=%llu A6=%llu A7=%llu LC=%llu neighbors=%llu\n",(unsigned long long)fiberfaces,(unsigned long long)fiberhp,(unsigned long long)fiberheavy,(unsigned long long)a6seen,(unsigned long long)a7seen,(unsigned long long)lcfaces,(unsigned long long)neighborchecks);
}
#endif
