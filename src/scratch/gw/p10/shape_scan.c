/* Shape-only tests on E153 certificates. Compile/run on fejer only. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <zlib.h>

#define CAP 4096
#define HASH 16384
static int X[CAP][4], nn, h[CAP], tops[CAP][4], pos[HASH];
static uint64_t keys[HASH];
static uint64_t encode(const int*x){uint64_t z=0;for(int a=0;a<4;a++)z|=(uint64_t)x[a]<<(12*a);return z+1;}
static int slot(uint64_t z){unsigned i=(z*11400714819323198485ull)>>(64-14);while(keys[i]&&keys[i]!=z)i=(i+1)&(HASH-1);return i;}
static int lookup(const int*x){int i=slot(encode(x));return keys[i]?pos[i]:-1;}
static int upper(int i,int a){int y[4];memcpy(y,X[i],sizeof y);y[a]++;return lookup(y);}
static int ht(int i){if(h[i]>=0)return h[i];int best=0;for(int a=0;a<4;a++){int j=upper(i,a);if(j>=0&&ht(j)+1>best)best=h[j]+1;}return h[i]=best;}
static int top(int i,int a){if(tops[i][a]>=0)return tops[i][a];int j=upper(i,a);return tops[i][a]=j<0?i:top(j,a);}
static int cmp_desc(const void*a,const void*b){return *(int*)b-*(int*)a;}
static int degree_floor(int n,int dim,int copies){int h=0,total=0;while(n){int cap=copies*(dim==2?h+1:(h+1)*(h+2)/2);int take=n<cap?n:cap;total+=h*take;n-=take;h++;}return total;}
static int jfloor(int n){if(n<=0)return 0;int a=n/12,b=n%12;return 12*a*(a-1)/2+b*a;}
static long long rank_min(int*w,int n){long long R=0;for(int i=0;i<n;i++)for(int j=0;j<i;j++)R+=w[i]<w[j]?w[i]:w[j];return R;}
static void graph_rank_check(int ns1,long long R){
 int ft[16]={0},fn[16]={0},L[4]={0},inc[4]={0},mask=0;
 for(int i=0;i<nn;i++){int su=0,ma=0;for(int a=0;a<4;a++)if(X[i][a]){su++;ma|=1<<a;}
  if(su==1){for(int a=0;a<4;a++)if(X[i][a]>L[a])L[a]=X[i][a];}
  if(su==2){fn[ma]++;if(!h[i])ft[ma]++;}}
 for(int a=0;a<4;a++){int x[4]={0};x[a]=L[a];if(!h[lookup(x)])mask|=1<<a;}
 int minL[4],sum=0;
 for(int a=0;a<4;a++){for(int b=0;b<4;b++)if(a!=b&&ft[(1<<a)|(1<<b)]>inc[a])inc[a]=ft[(1<<a)|(1<<b)];minL[a]=inc[a]?inc[a]+((mask>>a)&1):1;sum+=minL[a];if(L[a]<minL[a]||(!inc[a]&&!((mask>>a)&1))){puts("AXIS_MIN_FAIL");exit(3);}}
 int w[CAP],nw=0;
 for(int ma=0;ma<16;ma++)if(ft[ma]){if(fn[ma]<ft[ma]*(ft[ma]+1)/2){puts("FACE_VOLUME_FAIL");exit(3);}for(int k=0;k<ft[ma];k++)w[nw++]=ft[ma]+5;}
 for(int a=0;a<4;a++)if((mask>>a)&1)w[nw++]=4+minL[a];
 long long bound=rank_min(w,nw);
 if(mask==15){bound=1LL<<60;for(int a=0;a<4;a++){int z[CAP];memcpy(z,w,nw*sizeof(int));z[nw-4+a]+=ns1-sum;long long rr=rank_min(z,nw);if(rr<bound)bound=rr;}}
 if(R<bound){puts("GRAPH_RANK_FAIL");exit(3);}
}
static char* ws(char*p){while(*p&&*p<=32)p++;return p;}
static char* ints(char*p,int*x){p=ws(p);if(*p++!='[')abort();for(int a=0;a<4;a++){p=ws(p);x[a]=strtol(p,&p,10);p=ws(p);if(a<3&&*p++!=',')abort();}if(*p++!=']')abort();return p;}
static void witness(int m,const int*r,long long H,int t,int z0,int z1){
 printf("{\"m\":%d,\"r\":[%d,%d,%d,%d],\"H\":%lld,\"t\":%d,\"zero\":%d,\"one\":%d,\"D\":[",m,r[0],r[1],r[2],r[3],H,t,z0,z1);
 for(int i=0;i<nn;i++)printf("%s[%d,%d,%d,%d]",i?",":"",X[i][0],X[i][1],X[i][2],X[i][3]);puts("]}");fflush(stdout);
}
int main(int argc,char**argv){if(argc<4)return 2;int lo=atoi(argv[1]),hi=atoi(argv[2]);char filename[1024];
 long long all=0,boundary=0,twosup=0;int best_num=-1000000,best_den=1;long long min_slack=1ll<<60;
 long long min_b2=1ll<<60,min_b3=1ll<<60;int failures=0;
 for(int m=lo;m<=hi;m++){
  snprintf(filename,sizeof filename,"%s/certificate_all_%d.jsonl.gz",argv[3],m);gzFile f=gzopen(filename,"rb");if(!f){perror(filename);return 2;}
  char*line=NULL;size_t used=0,cap=1<<20;line=malloc(cap);long long count=0;
  while(1){int c=gzgetc(f);if(c<0)break;used=0;do{if(used+2>=cap){cap*=2;line=realloc(line,cap);}line[used++]=c;c=gzgetc(f);}while(c>=0&&c!='\n');line[used]=0;
   char*p=strstr(line,"\"r\":");if(!p)abort();int r[4];ints(p+4,r);int ok=1;for(int a=0;a<4;a++){if(!r[a])ok=0;for(int b=0;b<a;b++)if(r[a]==r[b])ok=0;}if(!ok)continue;
   p=strstr(line,"\"tile_cells\":[");if(!p)abort();p+=14;p=ws(p);
   while(*p=='['){p++;nn=0;p=ws(p);while(*p=='['){if(nn>=CAP)abort();p=ints(p,X[nn++]);p=ws(p);if(*p==',')p=ws(p+1);else break;}if(*p++!=']')abort();p=ws(p);if(nn!=m)abort();
    memset(keys,0,sizeof keys);for(int i=0;i<nn;i++){int sl=slot(encode(X[i]));if(keys[sl])abort();keys[sl]=encode(X[i]);pos[sl]=i;h[i]=-1;for(int a=0;a<4;a++)tops[i][a]=-1;}
    int shape_ok=1;for(int a=0;a<4;a++){int u[4]={0};u[a]=1;if(lookup(u)<0)shape_ok=0;}if(shape_ok){
     long long H=0,R=0;int t=0,z0=0,z1=0,w[CAP],ts[5]={0},ns[5]={0};
     for(int i=0;i<nn;i++){int su=0;for(int a=0;a<4;a++)su+=X[i][a]>0;ns[su]++;ht(i);if(!h[i]){int deg=0;for(int a=0;a<4;a++)deg+=X[i][a];w[t++]=4+deg;ts[su]++;}int local=0;for(int a=0;a<4;a++)local+=ht(top(i,a));H+=local;z0+=local==0;z1+=local==1;}
     if(!ns[4]){
      boundary++;long long bs=6*H-12*m+15*ts[1]+20*ts[2]+36*ts[3];if(bs<min_b2)min_b2=bs;
      if(bs<0){printf("BH2_FAIL ");witness(m,r,H,t,z0,z1);failures++;}
      /* Interior 2-face and 3-face antichain bounds, squared exactly. */
      if(12*ns[2]<ts[2]*ts[2]+6*ts[2]){puts("TYPE2_FAIL");return 3;}
      long long aa=6*ns[3]-3*ts[3];
      if(aa<0||aa*aa<(long long)ts[3]*ts[3]*(2*ts[3]+1)){puts("TYPE3_FAIL");return 3;}
      if(3*H<degree_floor(ns[3],3,4)){puts("G3_FAIL");return 3;}
      long long vv=4*H+2*ns[3],n3=ns[3];if(2*vv*vv*vv<3*n3*n3*n3*n3){puts("G3_CONT_FAIL");return 3;}
      if(!ns[3]){twosup++;long long bs3=4*H-12*m+15*ts[1]+24*ts[2];if(bs3<min_b3)min_b3=bs3;if(bs3<0){printf("BH3_FAIL ");witness(m,r,H,t,z0,z1);failures++;}
       int face_n[16]={0},face_t[16]={0},f=0;
       for(int i=0;i<nn;i++){int mask=0;for(int a=0;a<4;a++)if(X[i][a])mask|=1<<a;if(__builtin_popcount((unsigned)mask)==2){face_n[mask]++;if(!h[i])face_t[mask]++;}}
       for(int mask=0;mask<16;mask++)if(face_n[mask])f++;
       if(f&&H<degree_floor(ns[2],2,f)+jfloor(3*ns[1]-ns[2]-f)){puts("G2_AXIS_FAIL");return 3;}
       for(int i=0;i<nn;i++)if(!h[i]){int mask=0,deg=0;for(int a=0;a<4;a++){if(X[i][a])mask|=1<<a;deg+=X[i][a];}if(__builtin_popcount((unsigned)mask)==2&&deg<face_t[mask]+1){puts("FACE_DEG_FAIL");return 3;}}
      }
     }
     qsort(w,t,sizeof(int),cmp_desc);for(int i=0;i<t;i++)R+=(long long)i*w[i];
     if(!ns[3]&&!ns[4])graph_rank_check(ns[1],R);
     if(3LL*t*t*t*t>32LL*m*m*m){puts("TYPE4_FAIL");return 3;}
     long long slack=H+7*t-2*m;if(slack<min_slack){min_slack=slack;printf("MIN7 %lld ",slack);witness(m,r,H,t,z0,z1);}
     int num=2*m-H;if((long long)num*best_den>(long long)best_num*t){best_num=num;best_den=t;printf("RATIO %d/%d ",num,t);witness(m,r,H,t,z0,z1);}
     if((m+1)*H+R<(long long)3*m*(m-1)/2){printf("HCR_FAIL ");witness(m,r,H,t,z0,z1);}
     count++;all++;
    }
    if(*p==',')p=ws(p+1);else break;
   }
  }
  free(line);gzclose(f);printf("DONE m=%d count=%lld total=%lld maxC=%d/%d min7=%lld boundary=%lld two=%lld minBH2x6=%lld minBH3x4=%lld failures=%d\n",m,count,all,best_num,best_den,min_slack,boundary,twosup,min_b2,min_b3,failures);fflush(stdout);
 }
 return 0;
}
