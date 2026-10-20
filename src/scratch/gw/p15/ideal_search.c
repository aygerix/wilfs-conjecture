/* Adversarial injective ideals, d=2..6, every p, m<=60. Fejer only.
 * ./ideal_search lo hi starts steps seed. Does not abort on U failures.
 * Records least (m,N,d) and largest excess, preserving full witnesses. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
typedef struct{int m,d,N,r[6],f[64][6];} State;
static uint64_t rng;static unsigned rn(unsigned n){rng^=rng<<13;rng^=rng>>7;rng^=rng<<17;return rng%n;}static double ur(void){return rn(10000000)/10000000.;}
static int find(const State*s,int*f){for(int i=0;i<s->N;i++)if(!memcmp(f,s->f[i],s->d*sizeof(int)))return i;return -1;}
static int degree(const State*s,int i){int z=0;for(int a=0;a<s->d;a++)z+=s->f[i][a];return z;}
static int valid(const State*s){uint64_t used=0;for(int i=0;i<s->N;i++){int R=0;for(int a=0;a<s->d;a++)R+=s->f[i][a]*s->r[a];uint64_t b=1ull<<(R%s->m);if(used&b)return 0;used|=b;}return 1;}
static int score(const State*s,int*pp){
 int base=0,dec=0,dif[66]={0};
 for(int i=0;i<s->N;i++){
  int R=0,j=0;for(int a=0;a<s->d;a++){R+=s->f[i][a]*s->r[a];j+=s->f[i][a];}dec+=j>=2;
  base+=R/s->m;
  if(R%s->m){dif[1]+=1-j;dif[R%s->m+1]-=1-j;}
  for(int a=0;a<s->d;a++)if(s->f[i][a]){int t=s->f[i][a],u=R-s->r[a];base-=t*(R/s->m-u/s->m);if(u%s->m){dif[1]+=t;dif[u%s->m+1]-=t;}}
 }
 int best=-99999,k=0;for(int p=1;p<=s->m;p++){k+=dif[p];int v=base+k-dec;if(v>best){best=v;*pp=p;}}
 return best;
}
static int add(State*s){if(s->N==s->m)return 0;int x=rn(s->N),a=rn(s->d),f[6];memcpy(f,s->f[x],sizeof(f));f[a]++;if(find(s,f)>=0)return 0;
 for(int b=0;b<s->d;b++)if(f[b]){f[b]--;int j=find(s,f);f[b]++;if(j<0)return 0;}
 memcpy(s->f[s->N++],f,sizeof(f));if(!valid(s)){s->N--;return 0;}return 1;
}
static int remove_max(State*s,int floor){if(s->N<=floor)return 0;int i=rn(s->N);if(degree(s,i)<2)return 0;
 for(int j=0;j<s->N;j++)if(j!=i){int up=1;for(int a=0;a<s->d;a++)if(s->f[j][a]<s->f[i][a])up=0;if(up)return 0;}
 memcpy(s->f[i],s->f[--s->N],sizeof(s->f[i]));return 1;
}
static int gcd(int a,int b){while(b){int t=a%b;a=b;b=t;}return a;}
static void dump(const char*tag,const State*s,int ex,int p){
 printf("%s m=%d d=%d N=%d p=%d excess=%d r=[",tag,s->m,s->d,s->N,p,ex);for(int a=0;a<s->d;a++)printf("%s%d",a?",":"",s->r[a]);printf("] D=[");for(int i=0;i<s->N;i++){printf("%s[",i?",":"");for(int a=0;a<s->d;a++)printf("%s%d",a?",":"",s->f[i][a]);printf("]");}puts("]");fflush(stdout);
}
int main(int argc,char**argv){int lo=argc>1?atoi(argv[1]):10,hi=argc>2?atoi(argv[2]):60,starts=argc>3?atoi(argv[3]):10,steps=argc>4?atoi(argv[4]):5000;rng=argc>5?strtoull(argv[5],0,10):150015;
 printf("CONFIG lo=%d hi=%d starts=%d steps=%d seed=%llu\n",lo,hi,starts,steps,(unsigned long long)rng);
 unsigned long long tested=0,fails=0,has2=0;int smallm=999,smallN=999,smallD=999,big=0;
 for(int m=lo;m<=hi;m++)for(int d=2;d<=6&&d<m;d++)for(int run=0;run<starts;run++){
  State s={.m=m,.d=d,.N=d+1};
  int template=run%3==0&&m%2==0&&m>=14&&d+8<=m;
  if(template){s.N=0;s.r[0]=m/2+1;s.r[1]=m/2+2;for(int i=0;i<=3;i++)for(int j=0;j<=3-i;j++){s.f[s.N][0]=i;s.f[s.N++][1]=j;}
   for(int a=2;a<d;a++){do{s.r[a]=1+rn(m-1);s.f[s.N][a]=1;}while(!valid(&s)||({int z=0;for(int i=0;i<s.N;i++){int R=0;for(int b=0;b<d;b++)R+=s.f[i][b]*s.r[b];if(R%m==s.r[a])z=1;}z;}));s.N++;}
  }else{
   for(int a=0;a<d;a++){int good;do{s.r[a]=1+rn(m-1);good=1;for(int b=0;b<a;b++)if(s.r[a]==s.r[b])good=0;}while(!good);s.f[a+1][a]=1;}
   for(int k=0;k<2000;k++)add(&s);
  }
  if(!valid(&s)){puts("INIT_INVALID");return 3;}
  int floor=s.N>5?s.N-2:d+1;if(floor<d+1)floor=d+1;int p=0,cur=score(&s,&p);
  for(int it=0;it<steps;it++){
   State z=s;int mode=rn(5),ok=1;
   if(mode==0){int a=rn(d);z.r[a]=1+rn(m-1);ok=valid(&z);}
   else if(mode==1){int u;do{u=1+rn(m-1);}while(gcd(u,m)!=1);for(int a=0;a<d;a++)z.r[a]=z.r[a]*u%m;}
   else if(mode==2)ok=add(&z);
   else if(mode==3)ok=remove_max(&z,floor);
   else{ok=remove_max(&z,floor);if(ok){int done=0;for(int k=0;k<20&&!done;k++)done=add(&z);ok=done;}}
   if(!ok)continue;tested++;int q,ex=score(&z,&q);if(ex>0){fails++;if(m<smallm||(m==smallm&&(z.N<smallN||(z.N==smallN&&d<smallD)))){smallm=m;smallN=z.N;smallD=d;dump("SMALLEST",&z,ex,q);}if(ex>big){big=ex;dump("LARGEST",&z,ex,q);}}
   double temp=.05+1.5*pow(1.-(double)it/steps,2);if(ex>=cur||ur()<exp((ex-cur)/temp)){s=z;cur=ex;}
  }
 }
 printf("SUMMARY tested=%llu failures=%llu smallest_m=%d smallest_N=%d smallest_d=%d largest_excess=%d\n",tested,fails,smallm,smallN,smallD,big);return 0;
}
