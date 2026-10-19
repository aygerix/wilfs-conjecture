/* Random injective WRAP-MAX cores, completed by spikes on every missing label.
 * This is a tile construction, not a semigroup sampler.  One core per trial.
 * Every addition checks the downset, injectivity and no wrapped lower cover.
 * Usage: search SEED TRIALS MMAX KMAX [OUTPUT.json]
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define MM 1024
#define KK 10
#define HH 32768
#define CC (MM*KK)
typedef struct { uint64_t x; int v,deg; } Cell;
static Cell D[MM], cand[CC];
static uint64_t keys[HH];
static int vals[HH],used[MM],P[KK],tw[MM],arr[MM],degV[MM];
static uint64_t step[KK],rs;
static uint64_t rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static unsigned hash(uint64_t x){x^=x>>33;x*=0xff51afd7ed558ccdULL;x^=x>>33;return x&(HH-1);}
static int find(uint64_t x){unsigned h=hash(x);while(vals[h]){if(keys[h]==x)return vals[h]-1;h=(h+1)&(HH-1);}return -1;}
static void ins(uint64_t x,int j){unsigned h=hash(x);while(vals[h])h=(h+1)&(HH-1);keys[h]=x;vals[h]=j+1;}
static int eligible(uint64_t x,int m,int k){for(int a=0;a<k;a++)if((x>>(6*a))&63){int z=find(x-step[a]);if(z<0||D[z].v>=m)return 0;}return 1;}
static void emit(FILE*f,int m,int k,int n,int theta,int score){
 fprintf(f,"{\"m\":%d,\"P\":[",m);for(int a=0;a<k;a++)fprintf(f,"%s%d",a?",":"",P[a]);
 fprintf(f,"],\"D\":[");for(int j=0;j<n;j++){fprintf(f,"%s[",j?",":"");for(int a=0;a<k;a++)fprintf(f,"%s%llu",a?",":"",(unsigned long long)((D[j].x>>(6*a))&63));fprintf(f,"]");}
 fprintf(f,"],\"spikes\":[");int sep=0;for(int z=1;z<m;z++)if(!used[z]){fprintf(f,"%s%d",sep++?",":"",z);}fprintf(f,"],\"theta\":%d,\"slack\":%d}\n",theta,score);
 fflush(f);
}
int main(int argc,char**argv){
 if(argc<5){fprintf(stderr,"usage: search seed trials mmax kmax [witness]\n");return 2;}
 rs=strtoull(argv[1],0,10);if(!rs)rs=1;long trials=atol(argv[2]);int mmax=atoi(argv[3]),kmax=atoi(argv[4]);
 if(mmax>=MM||kmax>KK||mmax<8||kmax<2)return 2;
 const char*out=argc>5?argv[5]:"results/search_best.json";
 long phases=0,withV=0,high=0,zerosp=0;int best=INT_MAX,bestdegree=INT_MAX,maxh=0;
 for(long tr=0;tr<trials;tr++){
  int m=6+rnd()%(mmax-5), k=2+rnd()%(kmax-1);if(k>=m)k=m-1;
  memset(vals,0,sizeof(vals));memset(used,0,sizeof(used));int n=1,nc=0;
  D[0]=(Cell){0,0,0};ins(0,0);used[0]=1;
  int mode=rnd()%6;
  for(int a=0;a<k;a++){
   int z,lo=1,hi=m-1;
   if(mode==1)hi=m/3+1;else if(mode==2){lo=m/3;hi=2*m/3;}else if(mode==3)lo=m/2;else if(mode==4)hi=m/k+2;
   if(hi>=m)hi=m-1;if(lo<1)lo=1;if(hi-lo+1<k){lo=1;hi=m-1;}
   do{z=lo+rnd()%(hi-lo+1);}while(used[z]);
   P[a]=z;used[z]=1;step[a]=1ULL<<(6*a);D[n]=(Cell){step[a],z,1};ins(step[a],n++);
  }
  for(int j=1;j<n;j++)for(int a=0;a<k;a++){
   uint64_t x=D[j].x+step[a];int v=D[j].v+P[a];
   if(eligible(x,m,k))cand[nc++]=(Cell){x,v,2};
  }
  while(nc&&n<m){
   int c=rnd()%nc;Cell y=cand[c];cand[c]=cand[--nc];
   if(used[y.v%m]||find(y.x)>=0)continue;
   if(y.v>=2*m||!eligible(y.x,m,k))continue;
   /* Some trials retain a deliberately sparse core. */
   if((tr%5)==0 && y.deg>2 && rnd()%3==0)continue;
   D[n]=y;used[y.v%m]=1;ins(y.x,n++);
   if(y.v<m)for(int a=0;a<k;a++){
    if(((y.x>>(6*a))&63)==63)continue;
    uint64_t x=y.x+step[a];if(find(x)>=0)continue;
    if(eligible(x,m,k)&&nc<CC)cand[nc++]=(Cell){x,y.v+P[a],y.deg+1};
   }
  }
  memset(tw,0,sizeof(tw));memset(arr,0,sizeof(arr));memset(degV,0,sizeof(degV));
  int base=0,nV=0,h=0;
  for(int j=0;j<n;j++){
   int supp=0,up=0;for(int a=0;a<k;a++){int xa=(D[j].x>>(6*a))&63;supp+=xa>0;int z=xa==63?-1:find(D[j].x+step[a]);if(z<0)tw[j]+=xa+1;else up++;}
   int lab=D[j].v%m;arr[lab]+=tw[j]-k;
   if(D[j].v>=m){if(up){fprintf(stderr,"NONMAX WRAP\n");return 3;}base+=D[j].deg-1;nV++;}
   degV[lab]=up-supp;
   if(D[j].deg>h)h=D[j].deg;
  }
  for(int z=1;z<m;z++)if(!used[z])arr[z]++;
  if(nV)withV++;if(h>=3)high++;if(n==m)zerosp++;if(h>maxh)maxh=h;
  int cur=base;
  for(int th=m;th>=1;th--){
   if(th<m)cur+=arr[th];phases++;
   if(cur<best){best=cur;FILE*f=fopen(out,"w");if(!f)return 2;emit(f,m,k,n,th,cur);fclose(f);printf("best %d at trial %ld m %d k %d n %d h %d theta %d V %d\n",best,tr,m,k,n,h,th,nV);fflush(stdout);}
   if(cur<0){printf("COUNTEREXAMPLE\n");return 1;}
  }
  if((tr+1)%100000==0){printf("trials %ld phases %ld V %ld h3 %ld zero_spike %ld maxheight %d best %d\n",tr+1,phases,withV,high,zerosp,maxh,best);fflush(stdout);}
 }
 printf("DONE trials %ld phases %ld V %ld h3 %ld zero_spike %ld maxheight %d best %d\n",trials,phases,withV,high,zerosp,maxh,best);
 return 0;
}
