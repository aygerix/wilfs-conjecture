/* Greedy residue-complete down-set completion, not necessarily an Apery tile.
 * All execution on fejer, nice, one core. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "multi_low.h"
#define MM 20001
#define DD 160
typedef struct{int m,h,d,sz,g[DD],val[MM],dg[MM],f[MM][4];} State;
static State cur,trial,best,record;
static uint64_t st;
static uint64_t rnd(void){st^=st<<13;st^=st>>7;st^=st<<17;return st;}
static void sort(int*x,int k){for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)if(x[j]<x[i]){int z=x[j];x[j]=x[i];x[i]=z;}}
static int add(State*s,const int*x,int k){
 int v=0;for(int j=0;j<k;j++)v+=s->g[x[j]];
 int r=v%s->m;if(r==(s->h-1)%s->m||s->dg[r]>=0||v>4*s->m+s->h-1)return 0;
 if(k>1)for(int j=0;j<k;j++){
  int rr=(v-s->g[x[j]])%s->m;if(s->dg[rr]!=k-1)return 0;
  int pos=0;for(int l=0;l<k;l++)if(l!=j){if(s->f[rr][pos++]!=x[l])return 0;}
 }
 s->val[r]=v;s->dg[r]=k;for(int j=0;j<k;j++)s->f[r][j]=x[j];s->sz++;return 1;
}
static int extend(State*s,int residue){
 int idx=s->d;if(idx>=DD-1)return 0;
 s->g[idx]=s->m+s->h+(residue-s->h+s->m)%s->m;
 if(!add(s,&idx,1))return 0;s->d++;
 for(int band=3;band<=4;band++)for(int j=0;j<=idx;j++){
  int x[2]={j,idx};int v=s->g[j]+s->g[idx];
  if((v+s->m-s->h)/s->m==band)add(s,x,2);
 }
 for(int j=0;j<=idx;j++)for(int k=j;k<=idx;k++){int x[3]={j,k,idx};add(s,x,3);}
 return 1;
}
typedef struct{int WA,W,deficit,a,b,e,q2,q3,s,t,u4,J,JA,hot,alpha,p,SR,LC,Trans,newlower;} Stats;
static long long C2(long long a){return a*(a-1)/2;}
static long long C3(long long a){return a*(a-1)*(a-2)/6;}
static Stats stats(State*s,int a){
 Stats o={0};o.a=a;o.b=s->d-a;o.e=s->m-s->sz;
 int m=s->m,h=s->h,L=m,theta=(3*h+1)/2,ell=4,g=0;
 for(int j=0;j<a;j++){int z=s->g[j]-m;if(z<L)L=z;o.alpha+=2*z<h;o.p+=3*z>=2*h;}
 for(int r=1;r<m;r++)if(s->dg[r]>0){
  int dg=s->dg[r],v=s->val[r],A=0,B=0,band=(v+m-h)/m,tau=v-dg*m;
  for(int j=0;j<dg;j++){A+=s->f[r][j]<a;B+=s->f[r][j]>=a;}
  ell+=(4*m+h-1-v)/m;g+=v/m;
  o.q2+=dg==2&&A==2&&band==2;o.q3+=dg==2&&A==2&&band==3;
  o.s+=dg==2&&A==1&&B==1&&band==3;o.t+=dg==2&&B==2&&band==3;
  o.u4+=dg==3&&A==3;o.hot+=dg==3&&A==3&&tau>=2*h;
  assert(!(dg==3&&A==3&&band==3));
  if(dg==2&&B==2&&band==3)o.SR++;
  if(dg==3&&A==2&&B==1){int bv=0;for(int j=0;j<dg;j++)if(s->f[r][j]>=a)bv=s->g[s->f[r][j]];if((v-bv+m-h)/m==3)o.SR++;}
  if(dg==3&&((A==1&&B==2)||B==3))o.SR++;
  int iny=(h<=r&&r<theta)||(1<=r&&r<theta-m);
  int allowed=(dg==1&&A==0)||(dg==2&&A==2&&band==3)||(dg==2&&B>0&&band==4);
  if(iny&&!allowed){o.J++;if(A==dg)o.JA++;}
 }
 /* All missing residues become E units, including the maximum residue. */
 for(int r=1;r<m;r++)if(s->dg[r]<0){int v=3*m+h+(r-h+m)%m;g+=v/m;}
 o.W=(s->d+o.e)*ell-g;
 o.WA=3*a*(a+1)+(2*a-2)*o.q2+(a-3)*o.q3-4*o.u4;
 o.LC=(a+1)*o.q2;
 int ra=C2(a+1)-o.q2-o.q3;
 o.Trans=a*o.b-o.s+o.e*(3*a+2*o.b)+o.e*(2*o.q2+o.q3+o.s+o.t);
 int G=o.e*(3*a+2*o.b-1+o.q3+o.s+o.t);
 long long Ca=C3(a+1),mn=o.LC;if(mn>Ca)mn=Ca;
 int delta=h-2*L;if(delta<0)delta=0;
 o.deficit=3*delta-((a-1)*(o.b+1)+G+mn+(o.b+2)*o.q2+o.e*2*o.q2);
 o.newlower=o.LC+C3(o.p+2)-Ca+5*ra+o.Trans;
 assert(o.SR+o.hot<=m-h);
 assert(o.W>=o.WA+o.Trans+o.hot);
 assert(o.W>=o.newlower);
 int loss=2*o.J-(o.b+2)*o.q2;if(loss<0)loss=0;
 assert(o.W>=(a-1)*(o.b+1)+G+o.LC+o.e*2*o.q2-loss);
 if(a>=6&&o.alpha==1){assert(2*o.JA<=a-1+o.LC+2*o.q2);assert(o.W>=0);}
 return o;
}
static void show(const char*label,State*s,Stats o){
 printf("%s m=%d h=%d a=%d b=%d e=%d WA=%d W=%d LOWdef=%d alpha=%d p=%d q2=%d q3=%d u4=%d J=%d JA=%d hot=%d newlower=%d weights=",label,s->m,s->h,o.a,o.b,o.e,o.WA,o.W,o.deficit,o.alpha,o.p,o.q2,o.q3,o.u4,o.J,o.JA,o.hot,o.newlower);
 for(int j=0;j<s->d;j++)printf("%s%d",j?",":"",s->g[j]);puts("");fflush(stdout);
}
static void save(State*s,Stats o,int writefile){
 int m=s->m,dd=s->d;int *n=malloc(m*sizeof(int)),*F=calloc((size_t)4*m,sizeof(int)),*dg=calloc(m,sizeof(int));
 for(int j=0;j<dd;j++)n[j]=s->g[j];
 for(int r=1;r<m;r++){
  if(s->dg[r]>0){dg[r]=s->dg[r];for(int j=0;j<dg[r];j++)F[4*r+j]=s->f[r][j];}
  else {n[dd]=3*m+s->h+(r-s->h+m)%m;dg[r]=1;F[4*r]=dd++;}
 }
 assert(dd==s->d+o.e);p7sparse(m,dd,F,dg,n);multiverify(m,dd,F,dg,n);
 if(!writefile){free(n);free(F);free(dg);return;}
 FILE*f=fopen("frontier_best.json","w");assert(f);fprintf(f,"{\"m\":%d,\"h\":%d,\"weights\":[",m,s->h);
 for(int j=0;j<dd;j++)fprintf(f,"%s%d",j?",":"",n[j]);fprintf(f,"],\"D\":[");
 for(int r=0;r<m;r++){fprintf(f,"%s[",r?",":"");for(int j=0;j<dg[r];j++)fprintf(f,"%s%d",j?",":"",F[4*r+j]);fprintf(f,"]");}
 fprintf(f,"]}\n");fclose(f);free(n);free(F);free(dg);
}
int main(int argc,char**argv){
 assert(argc>=5&&argc<=7);st=strtoull(argv[1],0,10)*2654435761ULL+1;int tries=atoi(argv[2]),mlo=atoi(argv[3]),mhi=atoi(argv[4]),mode=argc>=6?atoi(argv[5]):0,amin=argc==7?atoi(argv[6]):1;assert(mhi<MM);
 long valid=0,neg=0,oldfront=0,newfront=0;int closest=-1000000000,minwa=1000000000;
 for(int it=0;it<tries;it++){
  int m=mlo+rnd()%(mhi-mlo+1),h=12+rnd()%(m-11),a=13+rnd()%12,alpha=amin,flavor=it%5;
  memset(&cur,0,sizeof(cur));cur.m=m;cur.h=h;cur.d=a;cur.sz=1;
  for(int r=0;r<m;r++)cur.dg[r]=-1;cur.dg[0]=0;
  int L=h;
  for(int j=0;j<a;j++){
   int t;
   if(j<alpha){int lo=(h+2)/3,hi=(h-1)/2;t=lo+rnd()%(hi-lo+1);if(t<L)L=t;}
   else{int lo=flavor==0?h-L:flavor==1?(2*h+2)/3:(h+1)/2;if(lo>=h)lo=h-1;t=lo+rnd()%(h-lo);}
   cur.g[j]=m+t;
  }
  sort(cur.g,a);int ok=1;
  for(int j=0;j<a;j++){int x=j;if(!add(&cur,&x,1))ok=0;}
  if(!ok)continue;
  for(int band=3;band>=2;band--)for(int j=0;j<a;j++)for(int k=j;k<a;k++){
   int x[2]={j,k},v=cur.g[j]+cur.g[k];if((v+m-h)/m==band)add(&cur,x,2);
  }
  for(int j=0;j<a;j++)for(int k=j;k<a;k++)for(int l=k;l<a;l++){
   int x[3]={j,k,l},v=cur.g[j]+cur.g[k]+cur.g[l];if((v+m-h)/m==4)add(&cur,x,3);
  }
  Stats o=stats(&cur,a);if(o.WA>=0)continue;
  valid++;
  for(int step=0;step<35&&cur.d<DD-1;step++){
   int bestscore=mode?-1000000000:o.deficit,bestgain=0;
   for(int prop=0;prop<24;prop++){
    int r=1+rnd()%(m-1);
    if(mode){int tries=0;while((cur.dg[r]>=0||r==(h-1)%m)&&tries++<m)r=r==m-1?1:r+1;}
    if(cur.dg[r]>=0||r==(h-1)%m)continue;
    memcpy(&trial,&cur,sizeof(cur));if(!extend(&trial,r))continue;Stats z=stats(&trial,a);
    int score=mode?(trial.sz-cur.sz)*10000-(z.W-o.W):z.deficit;
    if(score>bestscore){bestscore=score;bestgain=1;memcpy(&best,&trial,sizeof(best));}
   }
   if(!bestgain)break;
   memcpy(&cur,&best,sizeof(cur));o=stats(&cur,a);
  }
  neg++;oldfront+=o.deficit>0;newfront+=o.deficit>0&&o.newlower<0&&o.alpha>=2;
  if(o.WA<minwa)minwa=o.WA;
  int isrecord=o.alpha>=amin&&o.deficit>closest;save(&cur,o,isrecord);
  if(isrecord){closest=o.deficit;show("closest",&cur,o);memcpy(&record,&cur,sizeof(record));}
 }
  printf("seed=%s mode=%d min_low=%d attempts=%d valid_negative_A=%ld optimized=%ld old_frontier=%ld new_frontier=%ld closest_LOW_deficit=%d minWA=%d\n",argv[1],mode,amin,tries,valid,neg,oldfront,newfront,closest,minwa);
 p7summary();multisummary();
}
