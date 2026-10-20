/* P14: direct UF-RELAY and C/E/arc accounting. Fejer only.
 * Extended from P13; the earlier source is preserved. */
#ifndef P13_CORE_H
#define P13_CORE_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <limits.h>
#ifndef MM
#define MM 2048
#endif
typedef long long ll;
typedef struct {int m,d,q,a,alpha,b,cg,eg,npoor,nmfpoor,Ucrit,RA,MF,pA,Nlow,MFno2; ll M,h,ell,W,C2,need,B,Bc,E,Eu,Ltop,Delta,Wp,Ppoor,CuSlack,PlusSlack,PoorSlack,TopSlack,Z,CU,Relay,BaseCE,Ccorr,JC,QDef,H2,AAPay,QBound,n[MM];} Res;
static ll sorted[MM];static int dep[MM],steps[MM];
static int cmp(const void *a,const void *b){ll x=*(const ll*)a,y=*(const ll*)b;return(x>y)-(x<y);}
static int forward(int i,int m,ll n,const ll*w){if(steps[i]>=0)return steps[i];int j=(i+n)%m;return steps[i]=(w[j]==w[i]+n?1+forward(j,m,n,w):0);}
static int backward(int i,int m,ll n,const ll*w){if(dep[i]>=0)return dep[i];ll v=w[i]-n;if(v<0)return dep[i]=0;int j=v%m;return dep[i]=(w[j]==v?1+backward(j,m,n,w):0);}
static void evaluate(int m,const ll*w,Res*r){
 memset(r,0,sizeof(*r));r->m=m;r->C2=(ll)m*(m-1)/2;ll sum=0;
 for(int i=0;i<m;i++){sorted[i]=w[i];sum+=w[i];if(w[i]>r->M)r->M=w[i];}qsort(sorted,m,sizeof(ll),cmp);
 r->q=r->M/m;r->h=r->M-4*m+1;
 for(int i=1;i<m;i++){ll x=sorted[i];int comp=0;for(int a=0;a<r->d;a++){ll y=x-r->n[a];if(y>=0&&w[y%m]==y){comp=1;break;}}if(!comp)r->n[r->d++]=x;}
 for(int a=0;a<r->d;a++){ll t=r->n[a]-m;if(t<r->h){r->a++;if(2*t<r->h)r->alpha++;}}
 r->need=(r->d-1)*r->C2;r->B=(ll)r->d*m*r->M-(r->d+1)*sum;
 ll ev[MM],uv[MM]={0},lv[MM]={0},pv[MM]={0},ld[MM]={0};int jd[MM]={0},ad[MM]={0},uc[MM]={0},fac[MM][4];for(int i=0;i<m;i++){ev[i]=-w[i];r->ell+=(r->M-w[i])/m;}
 for(int a=0;a<r->d;a++){
  ll n=r->n[a];for(int i=0;i<m;i++)dep[i]=steps[i]=-1;
  for(int i=0;i<m;i++){
   int k=forward(i,m,n,w),h=backward(i,m,n,w);ll top=w[i]+k*n;
   r->Bc+=r->M-top;r->Ltop+=(r->M-top)/m;ld[a]+=(r->M-top)/m;ev[i]+=n*h;
   if(h){ll dif=(r->M-w[i]+n)/m-(r->M-w[i])/m;uv[i]+=n;lv[i]+=h*dif;pv[i]+=(ll)h*(((r->M-w[i]+n)%m)-((r->M-w[i])%m));jd[i]+=h;if(uc[i]<4)fac[i][uc[i]]=a;uc[i]++;if((r->M-n)/m==3)ad[i]+=h;}
  }
 }
 ll sp=0;
 for(int i=0;i<m;i++){
  ll g=w[i]-(ll)m*lv[i];r->E+=ev[i];if(uv[i]>w[i])r->Eu+=uv[i]-w[i];sp+=pv[i];
  if(pv[i]-ev[i]!=g){fprintf(stderr,"LOCAL ID FAIL\n");exit(8);}
  if(r->q==4){ll lam=(r->M-w[i])/m,K=4-lam-lv[i];if(K<0)r->Z-=K;
   if(K<=0&&(r->M-w[i])%m<=m-1-(r->h+1)/2)r->Nlow++;
   if(ev[i]){if(K>=0){fprintf(stderr,"MF UNIT FAIL\n");exit(8);}r->MF++;ll cr=lam+uc[i]-4;r->CU+=cr>1?cr:1;cr=lam+jd[i]-4;r->JC+=cr>1?cr:1;}
   if(K>0){if(K!=1||ev[i]){fprintf(stderr,"K>1 FAIL\n");exit(8);}r->Ucrit++;if(jd[i]==3&&ad[i]==3)r->RA++;else if((r->M-w[i])%m>=m-r->h){fprintf(stderr,"SHORT ARC FAIL\n");exit(8);}}
  }
  if(g>0){r->Wp+=g;r->Ppoor+=pv[i];r->npoor++;if(ev[i])r->nmfpoor++;}
 }
 r->Delta=r->d*r->C2-r->Bc;r->W=(r->d+1)*r->ell-(r->M-m+1);
 if(r->B-r->Bc!=r->E||r->Delta!=sp-(ll)m*r->Ltop||r->B!=(ll)m*r->W+r->need||r->Eu>r->E){fprintf(stderr,"GLOBAL ID FAIL\n");exit(8);}
 r->CuSlack=r->Bc+r->Eu-r->need;r->PlusSlack=r->C2+(ll)m*r->Ltop-r->Wp;r->PoorSlack=r->C2+(ll)m*r->Ltop-r->Ppoor;
 r->TopSlack=r->Ltop-r->Ucrit;
 if(r->q==4&&(r->W!=m-r->h+r->Ltop-r->Ucrit+r->Z||r->Z<r->CU||r->W<r->Ltop+r->CU-r->RA)){fprintf(stderr,"COUNT PAY FAIL\n");exit(8);}
 if(r->q==4&&r->a>0&&(r->a+5)*r->W<(r->a+5)*(r->Ltop+r->CU)-(r->a-1)*(m-1-r->d-r->MF)){fprintf(stderr,"SHADOW PAYMENT FAIL\n");exit(8);}
 if(r->q==4){
  char shadow[MM]={0};
  for(int i=0;i<m;i++)if(4-(r->M-w[i])/m-lv[i]==1&&jd[i]==3&&ad[i]==3){
   for(int j=0;j<uc[i];j++){ll v=w[i]-r->n[fac[i][j]];shadow[v%m]=1;}
  }
  for(int i=0;i<m;i++)if(shadow[i])r->pA++;
  r->Relay=r->Ltop+r->CU+r->pA-r->RA;
  if(r->W!=r->Ltop+r->Z+r->Nlow-r->h/2||r->W<r->d+1-r->h+r->Ltop+r->Z||r->W<r->Relay||r->Z<r->CU+r->pA){fprintf(stderr,"ARC/EH/RELAY ID FAIL\n");exit(8);}
  for(int a=0;a<r->d;a++){
   ll n=r->n[a],la=(r->M-n)/m;
   if(la==2)r->b++;
   if(la==1){
    r->cg++;ll removed=0;
    for(int i=1;i<m;i++)if(w[i]<2*m&&w[(w[i]+n)%m]==w[i]+n)removed+=(r->M-w[i])/m;
    if(ld[a]!=r->ell-3-removed){fprintf(stderr,"EXACT C FAIL\n");exit(8);}
   }
   if(la==0){r->eg++;if(ld[a]!=r->ell-4){fprintf(stderr,"EXACT E FAIL\n");exit(8);}}
  }
  r->BaseCE=(ll)r->cg*(r->cg+1)+(ll)r->eg*(3*r->a+2*r->b+r->cg);
  if(r->Ltop<r->BaseCE+(ll)(r->cg+r->eg)*r->pA){fprintf(stderr,"CE BASE FAIL\n");exit(8);}
  r->Ccorr=r->d+1-r->h+r->BaseCE;
  if(r->W<r->Ccorr){fprintf(stderr,"CE CORRIDOR FAIL\n");exit(8);}
  int r2[MM]={0},ra2[MM]={0};ll qwt[MM]={0};
  for(int a=0;a<r->d;a++)for(int b=a;b<r->d;b++){
   ll v=r->n[a]+r->n[b];if(v>r->M||w[v%m]!=v)continue;
   int i=v%m;ll la=(r->M-r->n[a])/m,lb=(r->M-r->n[b])/m,lam=(r->M-v)/m;
   r2[i]++;qwt[i]+=la+lb-2*lam;if(la==3&&lb==3)ra2[i]++;
  }
  for(int i=1;i<m;i++){
   ll lam=(r->M-w[i])/m,K=4-lam-lv[i];
   if(r2[i]){ll cr=lam+qwt[i]-3;r->QDef+=cr;r->H2+=lam;if(cr<0||1-K<cr){fprintf(stderr,"QUADRATIC PAY FAIL\n");exit(8);}}
   else if(ev[i])r->MFno2++;
   if(ra2[i]){ll cr=(3-lam)*(2*ra2[i]-1);r->AAPay+=cr;if(lam<1||lam>2||1-K<cr){fprintf(stderr,"AA PAY FAIL\n");exit(8);}}
  }
  r->QBound=r->d+1-r->h+r->BaseCE+(r->cg+r->eg)*r->H2+r->QDef+2*r->MFno2;
  if(r->W<r->QBound||r->QDef<r->AAPay){fprintf(stderr,"QUADRATIC TOTAL FAIL\n");exit(8);}
 }
}
static int apery(int m,int ng,const ll*g,ll*w){int used[MM]={0};for(int i=0;i<m;i++)w[i]=LLONG_MAX/8;w[0]=0;for(int z=0;z<m;z++){int u=-1;for(int i=0;i<m;i++)if(!used[i]&&(u<0||w[i]<w[u]))u=i;if(w[u]==LLONG_MAX/8)return 0;used[u]=1;for(int a=0;a<ng;a++){int j=(u+g[a])%m;if(w[j]>w[u]+g[a])w[j]=w[u]+g[a];}}return 1;}
static void dump(const char*tag,const Res*r,const ll*w){
 printf("%s m=%d e=%d q=%d a=%d alpha=%d b=%d C=%d Egen=%d M=%lld W=%lld RA=%d pA=%d Ltop=%lld Z=%lld C_U=%lld MF=%d Nlow=%d rho-Rout=%lld RELAY=%lld CEBASE=%lld CECORR=%lld gens=[%d",tag,r->m,r->d+1,r->q,r->a,r->alpha,r->b,r->cg,r->eg,r->M,r->W,r->RA,r->pA,r->Ltop,r->Z,r->CU,r->MF,r->Nlow,r->m-r->h-r->Ucrit+r->RA,r->Relay,r->BaseCE,r->Ccorr,r->m);
 for(int a=0;a<r->d;a++)printf(",%lld",r->n[a]);printf("] Ap=[");for(int i=0;i<r->m;i++)printf("%s%lld",i?",":"",w[i]);puts("]");fflush(stdout);
}
#endif
