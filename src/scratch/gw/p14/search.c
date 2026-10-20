/* P14 hard-q=4 Kunz annealing. Usage: search m starts steps objective seed sparse shaped [seedfile].
 * objective 0 CHAIN-U; 1 CHAIN-POOR; 2 WILF+; 3 TOP-STRONG.
 * 4: UF-RELAY deficit (penalty +10 at RA=0 in unseeded runs).
 * 5: ratio (Lambda+C_U)/(RA-pA), only with a seedfile.
 * Sparse=1 enforces 3e<m. shaped=1 enforces a>=19, alpha>=6.
 * A seedfile contains Ap by residue and enforces RA>pA on every state. */
#include "core.h"
#include <math.h>
static uint64_t rs;static uint64_t rand64(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static unsigned rn(unsigned n){return rand64()%n;}static double ur(void){return(rand64()>>11)*0x1.0p-53;}
static int valid(int m,const ll*w,int t){if(w[t]<m+t||w[t]>4*m+t)return 0;for(int i=1;i<m;i++){if(w[t]+w[i]<w[(t+i)%m])return 0;int j=(t-i+m)%m;if(w[i]+w[j]<w[t])return 0;}return 1;}
static double score(const Res*r,int obj){if(obj==5)return (double)(r->Ltop+r->CU)/(r->RA-r->pA);return obj==4?(double)r->Relay:(obj==3?(double)r->TopSlack/r->m:(obj==0?(double)r->CuSlack/(r->need?r->need:1):(double)(obj==1?r->PoorSlack:r->PlusSlack)/r->C2));}
int main(int argc,char**argv){
 int m=argc>1?atoi(argv[1]):61,starts=argc>2?atoi(argv[2]):30,steps=argc>3?atoi(argv[3]):100000,obj=argc>4?atoi(argv[4]):0,sparse=argc>6?atoi(argv[6]):0,shaped=argc>7?atoi(argv[7]):0;
 rs=argc>5?strtoull(argv[5],0,10):130001;if(!rs)rs=130001;
 printf("CONFIG m=%d starts=%d steps=%d objective=%d seed=%llu sparse=%d shaped=%d seedfile=%s\n",m,starts,steps,obj,(unsigned long long)rs,sparse,shaped,argc>8?argv[8]:"none");fflush(stdout);
 ll w[MM],bw[MM],g[MM];Res s,z,bs;double best=1e99;unsigned long long proposals=0,good=0,accepted=0;
 for(int run=0;run<starts;run++){
  int seeded=0;
  for(int tr=0;tr<10000&&!seeded;tr++){
   int mode=run%4;
   if(argc>8){FILE*f=fopen(argv[8],"r");if(!f)return 6;for(int i=0;i<m;i++)if(fscanf(f,"%lld",&w[i])!=1)return 6;fclose(f);}
   else if(shaped){
    int k=(m-2)/5,ng=0;if(m!=5*k+2||k<105||!(k&1))return 5;
    for(int j=0;j<6;j++)g[ng++]=m+2+4*j;
    int hh=k+1,first=(hh+1)/2;while(first%4!=2)first++;
    for(int j=0;j<13;j++)g[ng++]=m+first+4*j;
    for(int j=k+1;j<=2*k+1;j++)g[ng++]=m+j;
    if(!apery(m,ng,g,w))continue;
   }
   else if(mode==0&&!sparse){w[0]=0;for(int i=1;i<m;i++)w[i]=(2+rn(3))*m+i;}
   else {
    int a=1+rn(m-2),b=a+1+rn(m-a-1),ng=0;
    if(mode==1){a=m/5+1;b=2*m/5+1;}if(mode==2){a=3*m/5;b=4*m/5;}
    for(int i=a;i<=b;i++)g[ng++]=m+i;
    if(mode==3){int nn=2+rn(8);for(int i=0;i<nn;i++)g[ng++]=m+1+rn(m-1);}
    if(!apery(m,ng,g,w))continue;
    ll K=3*m+1+rn(m-1);for(int i=1;i<m;i++){ll cap=K+(i-K%m+m)%m;if(w[i]>cap)w[i]=cap;}
   }
   evaluate(m,w,&s);if(s.q!=4||s.d<2||(sparse&&3*(s.d+1)>=m)||(shaped&&(s.a<19||s.alpha<6)))continue;if(argc>8&&s.RA<=s.pA)return 7;seeded=1;
  }
  if(!seeded){fprintf(stderr,"NO SEED run %d\n",run);continue;}
  for(int it=-1;it<steps;it++){
   int t=0;ll old=0;
   if(it>=0){proposals++;t=1+rn(m-1);old=w[t];w[t]+=(rn(2)?m:-m);if(!valid(m,w,t)){w[t]=old;continue;}evaluate(m,w,&z);if(z.q!=4||z.d<2||(sparse&&3*(z.d+1)>=m)||(shaped&&(z.a<19||z.alpha<6))||(argc>8&&z.RA<=z.pA)){w[t]=old;continue;}good++;}
   else z=s;
   double val=score(&z,obj);if(obj==4&&z.RA==0)val+=10;
   if(val<best){best=val;bs=z;memcpy(bw,w,m*sizeof(ll));dump("RECORD",&z,w);}
   if(z.CuSlack<0||z.PoorSlack<0||z.PlusSlack<0||z.nmfpoor){dump("COUNTEREXAMPLE",&z,w);return 2;}
   if((obj==4||obj==5)&&z.Relay<0){dump("UF_RELAY_COUNTEREXAMPLE",&z,w);return 4;}
   double temp=obj==5?.01+pow(1.0-(double)(it+1)/steps,2):(obj==4?.2+3*pow(1.0-(double)(it+1)/steps,2):.00003+.06*pow(1.0-(double)(it+1)/steps,2));
   double oldval=score(&s,obj);if(obj==4&&s.RA==0)oldval+=10;
   if(it<0||val<=oldval||ur()<exp((oldval-val)/temp)){s=z;accepted++;}else w[t]=old;
  }
  fprintf(stderr,"RUN %d proposals=%llu validclass=%llu accepted=%llu best=%.12f\n",run+1,proposals,good,accepted,best);fflush(stderr);
 }
 printf("SUMMARY m=%d obj=%d sparse=%d shaped=%d proposals=%llu validclass=%llu accepted=%llu best=%.12f\n",m,obj,sparse,shaped,proposals,good,accepted,best);if(best<1e90)dump("BEST",&bs,bw);
}
