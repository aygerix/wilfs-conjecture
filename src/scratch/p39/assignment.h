/* Integer Hungarian algorithm. Every result verifies a permutation and feasible
 * assignment-dual potentials of equal value, so optimization is certificate checked. */
#ifndef WILF_ASSIGNMENT_H
#define WILF_ASSIGNMENT_H
#include <assert.h>
#include <limits.h>
static long long assignment(int n,int A[MM][MM],int perm[MM],long long alpha[MM],long long beta[MM]){
 long long u[MM+1]={0},v[MM+1]={0};int p[MM+1]={0},way[MM+1]={0};
 for(int i=1;i<=n;i++){
  p[0]=i;int j0=0,used[MM+1]={0};long long minv[MM+1];for(int j=1;j<=n;j++)minv[j]=LLONG_MAX/4;
  do{used[j0]=1;int i0=p[j0],j1=0;long long delta=LLONG_MAX/4;
   for(int j=1;j<=n;j++)if(!used[j]){long long cur=-A[i0-1][j-1]-u[i0]-v[j];if(cur<minv[j]){minv[j]=cur;way[j]=j0;}if(minv[j]<delta){delta=minv[j];j1=j;}}
   for(int j=0;j<=n;j++){if(used[j]){u[p[j]]+=delta;v[j]-=delta;}else if(j)minv[j]-=delta;}
   j0=j1;
  }while(p[j0]);
  do{int j1=way[j0];p[j0]=p[j1];j0=j1;}while(j0);
 }
 long long val=0,dual=0;
 for(int j=1;j<=n;j++)perm[p[j]-1]=j-1;
 for(int i=0;i<n;i++){alpha[i]=-u[i+1];beta[i]=-v[i+1];val+=A[i][perm[i]];dual+=alpha[i]+beta[i];}
 assert(val==dual);
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)assert(alpha[i]+beta[j]>=A[i][j]);
 return val;
}
#endif
