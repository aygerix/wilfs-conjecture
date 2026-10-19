/* Check every step of the proof of Wilf for quadratic Apery sets (Theorem GW-27).
   Steps: (S1) identity W = F + D_hi + sum_x c_x, c_x=(d+2)lam(x)+beta_x-gamma_x;
   (S2) c_x >= -1, = -1 iff U-edge; (S3) every pair with residue in (mu,2mu] has c_x >= 1;
   (S4) U-edge residues in [max(1,2mu+2-m), mu] and both endpoints have r>mu;
   (S5) case 2mu<=m-1: W >= F + d - D_mid ; case 2mu>=m: W >= F.
   modes: tree G   |  rand seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
typedef unsigned __int128 u128;
static long nq,f1,f2,f3,f4,f5,nA,nB; static double minr=1e9;
static void check(int m,const long *ap,const int *gen,int d){
  /* ap[r] Apery set; gen[0..d-1] minimal generators != m */
  long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
  static int isg[4096],pa[4096],pb[4096]; for(int r=0;r<m;r++) isg[r]=0; for(int a=0;a<d;a++) isg[gen[a]%m]=1;
  for(int r=1;r<m;r++){ if(isg[r]) continue; int f=0; for(int a=0;a<d&&!f;a++) for(int b=a;b<d;b++) if((long)gen[a]+gen[b]==ap[r]){pa[r]=a;pb[r]=b;f=1;break;} if(!f) return; }
  nq++;
  long K=M/m, mu=M%m; long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
  static int deg[4096]; for(int a=0;a<d;a++) deg[a]=0;
  long sumc=0,U=0;
  for(int r=1;r<m;r++){ if(isg[r]) continue; int a=pa[r],b=pb[r]; deg[a]++; deg[b]++;
    long x=ap[r]; long lx=(M-x)/m, ex=(M-x)%m; long ra=gen[a]%m, rb=gen[b]%m;
    int gam=(ra+rb>=m); int bet=(ex+rb>=m)+(ex+ra>=m);
    long cx=(long)(d+2)*lx+bet-gam; sumc+=cx;
    if(cx<-1||(cx==-1&&!(lx==0&&bet==0&&gam==1))) f2++;
    if(cx==-1){ U++; long lo=2*mu+2-m; if(lo<1) lo=1; if(r<lo||r>mu||ra<=mu||rb<=mu) f4++; }
    if(r>mu && r<=2*mu && cx<1) f3++;
  }
  long F=0; int Dhi=0,Dmid=0; for(int a=0;a<d;a++){ long la=(M-gen[a])/m; F+=(long)(d+1-deg[a])*la; int ra=gen[a]%m; if(ra>mu){Dhi++; if(ra<=2*mu) Dmid++;} }
  if(W!=F+Dhi+sumc) f1++;
  if(2*mu<=m-1){ nA++; if(W<F+d-Dmid) f5++; } else { nB++; if(W<F) f5++; }
  (void)K;
}
static int G; static long cnt;
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++;
  if(m>1){ long ap[128]; for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;} int gg[128],d=0; for(int i=0;i<e;i++) if(gens[i]!=m) gg[d++]=gens[i]; check(m,ap,gg,d); }
  if(genus==G) return;
  int ng[128];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
int main(int argc,char**argv){
  if(!strcmp(argv[1],"tree")){ G=atoi(argv[2]); int gens[]={1}; visit(0,-1,1,gens,1,0); printf("tree genus<=%d all=%ld ",G,cnt); }
  else { st=strtoull(argv[2],0,10)*2654435761ULL+7; long T=atol(argv[3]); int mmin=atoi(argv[4]),mmax=atoi(argv[5]);
    static long ap[4096]; static int done[4096], gs[64], gen[4096];
    for(long t=0;t<T;t++){ int m=mmin+rnd()%(mmax-mmin+1); int ng=2+rnd()%20; double lo=1.0+(rnd()%4000)/1000.0; double wid=(rnd()%1000)/1000.0*lo*0.6;
      for(int k=0;k<ng;k++) gs[k]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1;
      for(int r=0;r<m;r++){ap[r]=-1;done[r]=0;} ap[0]=0;
      for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<ng;k++){ int r2=(b+gs[k])%m; long v=ap[b]+gs[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
      int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
      int d=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) gen[d++]=(int)ap[r]; }
      check(m,ap,gen,d); }
    printf("rand seed=%s ",argv[2]); }
  printf("quadratic=%ld (caseA %ld, caseB %ld) fails: S1=%ld S2=%ld S3=%ld S4=%ld S5=%ld\n",nq,nA,nB,f1,f2,f3,f4,f5); return 0; }
