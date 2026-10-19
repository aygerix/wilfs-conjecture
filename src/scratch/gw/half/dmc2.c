/* DMC / MC_i: sum_x min(i,kappa) <= sum_{k<=min(d,t)} sum_x min(i, floor((V_k - v)/m)_+ ), V_k = values of corners desc.
   mode 0: random residue-complete down-sets (random growth), corners = maximal cells.
   mode 1: random semigroups, corners = PF+m (<=_S-maximal Apery elements).
   usage: dmc mode seed trials mmin mmax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static int cmpd(const void*a,const void*b){ long x=*(long*)a,y=*(long*)b; return x>y?-1:x<y; }
#define MAXM 128
static int m,d,ncell; static int cell[MAXM][8]; static long val[MAXM]; static long V[MAXM]; static int nV;
static long fl(long a,long b){ return a>=0? a/b : -((-a+b-1)/b); }
static int find(int*x){ for(int c=0;c<ncell;c++){ int ok=1; for(int a=0;a<d;a++) if(cell[c][a]!=x[a]){ok=0;break;} if(ok) return c; } return -1; }
static long tests=0,fails=0,gwfails=0,tgt=0; static long fi[16];
static void check(void){
  long M=0; for(int c=0;c<ncell;c++) if(val[c]>M) M=val[c]; int K=M/m; if(K<1) return;
  qsort(V,nV,sizeof(long),cmpd); int nk=nV<d?nV:d; if(nV>d) tgt++;
  for(int i=1;i<=K;i++){ long L=0,R=0; for(int c=0;c<ncell;c++){ long k1=val[c]/m; L+=k1<i?k1:i; for(int k=0;k<nk;k++){ long l1=fl(V[k]-val[c],m); if(l1<0) l1=0; R+=l1<i?l1:i; } }
    tests++; if(L>R){ fails++; if(i<16) fi[i]++; if(fails<=4) printf("MC FAIL i=%d K=%d m=%d d=%d t=%d L=%ld R=%ld\n",i,K,m,d,nV,L,R); break; } }
  long g=0,l=0; for(int c=0;c<ncell;c++){ g+=val[c]/m; l+=(M-val[c])/m; } if(g>(long)d*l) gwfails++;
}
int main(int argc,char**argv){
  int mode=atoi(argv[1]); st=strtoull(argv[2],0,10)*2654435761ULL+3; long trials=atol(argv[3]); int mmin=atoi(argv[4]),mmax=atoi(argv[5]);
  static long ap[512]; static int done[512];
  for(long tt=0;tt<trials;tt++){
    m=mmin+rnd()%(mmax-mmin+1);
    if(mode==0||mode==2){
      d=2+rnd()%4; int n[8]; int span=m*(1+rnd()%6); for(int a=0;a<d;a++) n[a]=m+1+rnd()%span;
      ncell=1; memset(cell[0],0,sizeof(cell[0])); val[0]=0; char used[MAXM]; memset(used,0,sizeof used); used[0]=1;
      int stuck=0;
      while(ncell<m && !stuck){ /* collect addable cells with new residue */
        int cand[4096][8]; int nc=0;
        for(int c=0;c<ncell&&nc<4000;c++) for(int a=0;a<d;a++){ int x[8]; memcpy(x,cell[c],sizeof x); x[a]++;
          long v=val[c]+n[a]; if(mode==0&&used[v%m]) continue; if(find(x)>=0) continue;
          int ok=1; for(int b=0;b<d&&ok;b++) if(x[b]>0){ x[b]--; if(find(x)<0) ok=0; x[b]++; }
          if(ok){ memcpy(cand[nc],x,sizeof x); nc++; } }
        if(nc==0){ stuck=1; break; }
        int pick=rnd()%nc; memcpy(cell[ncell],cand[pick],sizeof cell[0]); long v=0; for(int a=0;a<d;a++) v+=(long)cand[pick][a]*n[a];
        val[ncell]=v; used[v%m]=1; ncell++; }
      if(stuck) continue;
      nV=0; for(int c=0;c<ncell;c++){ int mx=1; for(int a=0;a<d&&mx;a++){ int x[8]; memcpy(x,cell[c],sizeof x); x[a]++; if(find(x)>=0) mx=0; } if(mx) V[nV++]=val[c]; }
      check();
    } else {
      int ng=1+rnd()%6; int gens[8]; int span=m*(2+rnd()%8); for(int k=0;k<ng;k++) gens[k]=m+1+rnd()%span;
      for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
      for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1;
        for(int k=0;k<ng;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
      int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
      int e=1; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec) e++; }
      d=e-1; ncell=m; for(int r=0;r<m;r++) val[r]=ap[r];
      nV=0; for(int r=1;r<m;r++){ int mx=1; for(int s=1;s<m&&mx;s++){ int r2=(r+s)%m; if(ap[r2]==ap[r]+ap[s]) mx=0; } if(mx) V[nV++]=ap[r]; }
      check();
    }
  }
  printf("first failing i histogram:"); for(int i=1;i<16;i++) printf(" %ld",fi[i]); printf("\n"); printf("mode=%d instances tested=%ld (with t>d: %ld) MC_i fails: %ld  GW fails: %ld\n",mode,tests?tgt+0:0,tgt,fails,gwfails);
  return 0; }
