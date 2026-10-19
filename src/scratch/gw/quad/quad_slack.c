/* Quadratic Apery sets: exact identity W = sum column slack - #carries (GW-22). Decompose slack and test candidate
   charging inequalities for the top-window carry pairs C0 (carry pairs with lambda=0).
   usage: quad_slack seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st;
static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+1; long trials=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]);
  static long ap[4096]; static int done[4096]; static int gens[64]; static int isg[4096]; static long mg[64];
  static int pidx[64][64]; /* pair present? */
  long nq=0, idfail=0, f1=0,f2=0,f3=0; double worst1=1e9;
  for(long t=0;t<trials;t++){
    int m=mmin+rnd()%(mmax-mmin+1);
    int ng=2+rnd()%16; int g0=0;
    double lo=1.0+(rnd()%3000)/1000.0; double wid=(rnd()%1000)/1000.0*lo*0.5;
    for(int k=0;k<ng;k++) gens[g0++]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r;
      if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    int d=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isg[r]=!dec; if(!dec){ if(d<64) mg[d]=ap[r]; d++; } }
    if(d>=64||d<3) continue;
    /* tile: pair cells = Apery elements equal to mg[i]+mg[j]; choose lex-first factorization */
    for(int i=0;i<d;i++) for(int j=0;j<d;j++) pidx[i][j]=0;
    int quad=1, npairs=0;
    for(int r=1;r<m&&quad;r++){ if(isg[r]) continue; int f=0; for(int i=0;i<d&&!f;i++) for(int j=i;j<d;j++) if(mg[i]+mg[j]==ap[r]){ pidx[i][j]=pidx[j][i]=1; f=1; npairs++; break;} if(!f) quad=0; }
    if(!quad) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; nq++;
    long g=0; for(int r=0;r<m;r++) g+=ap[r]/m; long l=c-g; long W=(long)d*l-g;
    #define LAM(v) ((M-(v))/m)
    #define EPS(v) ((M-(v))%m)
    long carries=0, C0=0; long slack=0, s1=0,s2=0,s3=0, s2bonus=0, unitlam=0;
    for(int i=0;i<d;i++) for(int j=i+1;j<d;j++) if(pidx[i][j]){ if(mg[i]%m+mg[j]%m>=m){ carries++; if(LAM(mg[i]+mg[j])==0) C0++; } }
    /* columns */
    for(int b=0;b<d;b++){
      /* axis column from 0 */
      { long v1=mg[b]; int J= pidx[b][b]?2:1; long top= (J==2)?2*mg[b]:mg[b]; long lt=LAM(top), e=EPS(top); long s=(J+1)*lt; for(int jj=1;jj<=J;jj++) if(((jj*mg[b])%m)+e>=m) s++; s3+=s; (void)v1; }
      for(int a=0;a<d;a++) if(a!=b){ /* column based at e_a */
        if(pidx[a][b]){ long top=mg[a]+mg[b]; long s=2*LAM(top); if((mg[b]%m)+EPS(top)>=m){ s++; s2bonus++; } s2+=s; }
        else { s2+=LAM(mg[a]); }
        unitlam+=LAM(mg[a]);
      }
      for(int a=0;a<d;a++) for(int cc=a;cc<d;cc++) if(pidx[a][cc] && a!=b && cc!=b){ s1+=LAM(mg[a]+mg[cc]); }
    }
    slack=s1+s2+s3;
    if(W!=slack-carries){ idfail++; if(idfail<4) printf("IDENTITY FAIL W=%ld slack=%ld carries=%ld\n",W,slack,carries); }
    /* candidate 1: C0 <= s3 + s2 (units+axis) */
    if(C0>s2+s3) f1++;
    /* candidate 2: carries <= s1 (pair singleton columns alone) */
    if(carries>s1) f2++;
    /* candidate 3: C0 <= s2bonus + s3 */
    if(C0>s2bonus+s3) f3++;
    double rr=(double)(s2+s3-C0)/(c); if(rr<worst1) worst1=rr;
  }
  printf("seed=%s quadratic d>=3: %ld identity_fail=%ld | C0>s2+s3: %ld | carries>s1: %ld | C0>s2bonus+s3: %ld | min (s2+s3-C0)/c=%.3f\n",argv[1],nq,idfail,f1,f2,f3,worst1);
  return 0; }
