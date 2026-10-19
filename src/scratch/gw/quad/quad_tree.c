/* Exhaustive (genus <= G) check on semigroups with quadratic Apery set Ap(S,m) = {0} u gens u (gens+gens).
   Identity (Q-ID): W = sum_a f_a lam_a + (d+2) sum_x lam(x) + D_hi + sum_x (beta_x - gamma_x)
   where f_a = d+1-deg_P(a), D_hi = #{a : r_a > mu}, mu = M mod m.
   U = #{x in P : lam(x)=0, beta_x=0, gamma_x=1}. Residue count: U + D_lo + O_lo = mu (claimed).
   usage: quad_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int G; static long cnt, nq, idfail, resfail, mugtd, l1fail; static long minmarg=1L<<40; static long nk4=0, k4mugtd=0, uDhi=0, uDhiF=0, maxU=0; static double minratio=1e9;
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void analyze(u128 gm,int F,int m,int *gens,int e){
  int ap[128],M=0; for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;if(w>M)M=w;}
  int n[64],d=0; for(int i=0;i<e;i++) if(gens[i]!=m) n[d++]=gens[i];
  if(d<2) return;
  int isgen[128]={0}; for(int a=0;a<d;a++) isgen[n[a]%m]=1;
  int pa[128],pb[128];
  for(int r=1;r<m;r++){ if(isgen[r]) continue; int f=0; for(int a=0;a<d&&!f;a++) for(int b=a;b<d;b++) if(n[a]+n[b]==ap[r]){pa[r]=a;pb[r]=b;f=1;break;} if(!f) return; }
  nq++;
  int K=M/m, mu=M%m; long c=M-m+1;
  long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; }
  long W=(long)d*l-g;
  int deg[64]={0}; long sumbg=0, sumlx=0, U=0, Pplus=0, Olo=0;
  for(int r=1;r<m;r++){ if(isgen[r]) continue; int a=pa[r],b=pb[r]; deg[a]++; deg[b]++;
    int x=ap[r]; int lx=(M-x)/m, ex=(M-x)%m; int ra=n[a]%m, rb=n[b]%m;
    int gam=(ra+rb>=m); int bet; if(a!=b) bet=(ex+rb>=m)+(ex+ra>=m); else bet=2*(ex+ra>=m);
    sumbg+=bet-gam; sumlx+=lx; if(lx>0) Pplus++;
    if(lx==0&&bet==0&&gam==1) U++;
    else if(r<=mu) Olo++;
  }
  long Fs=0; int Dhi=0,Dlo=0;
  for(int a=0;a<d;a++){ int la=(M-n[a])/m; Fs+=(long)(d+1-deg[a])*la; if(n[a]%m>mu) Dhi++; else Dlo++; }
  long rhs=Fs+(long)(d+2)*sumlx+Dhi+sumbg;
  if(rhs!=W){ idfail++; if(idfail<5) printf("ID FAIL m=%d W=%ld rhs=%ld\n",m,W,rhs); }
  if(U+Dlo+Olo!=mu){ resfail++; if(resfail<5) printf("RES FAIL m=%d mu=%d U=%ld Dlo=%d Olo=%ld\n",m,mu,U,Dlo,Olo); }
  if(mu>d) mugtd++; if(K>=4&&d>=3){ nk4++; if(mu>d) k4mugtd++; }
  long marg=Dhi+Fs+(long)(d+1)*Pplus-U; if(marg<0){ l1fail++; if(l1fail<5) printf("L1 FAIL m=%d d=%d\n",m,d);} 
  if(U>Dhi) uDhi++; if(U>Dhi+Fs) uDhiF++; if(U>maxU){maxU=U; printf("maxU=%ld m=%d d=%d K=%d mu=%d Dhi=%d F=%ld P+=%ld W=%ld c=%ld\n",U,m,d,K,mu,Dhi,Fs,Pplus,W,c);} if(U>0){ double rt=(double)(Dhi+Fs+(long)(d+1)*Pplus)/U; if(rt<minratio){minratio=rt; printf("minratio=%.3f U=%ld m=%d d=%d K=%d mu=%d Dhi=%d F=%ld P+=%ld W=%ld c=%ld gens:",rt,U,m,d,K,mu,Dhi,Fs,Pplus,W,c); for(int a=0;a<d;a++) printf(" %d",n[a]); printf("\n");} }
  if(0){ minmarg=marg; printf("newmin marg=%ld m=%d d=%d K=%d mu=%d U=%ld Dhi=%d F=%ld P+=%ld W=%ld c=%ld gens:",marg,m,d,K,mu,U,Dhi,Fs,Pplus,W,c); for(int a=0;a<d;a++) printf(" %d",n[a]); printf("\n"); }
  (void)c;
}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++; if(m>1) analyze(gm,F,m,gens,e);
  if(genus==G) return;
  int ng[128];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue;
    u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k];
      int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); assert(G<=40); int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("K>=4,d>=3: %ld (mu>d: %ld)  U>Dhi: %ld  U>Dhi+F: %ld maxU=%ld minratio=%.3f\n",nk4,k4mugtd,uDhi,uDhiF,maxU,minratio); printf("genus<=%d all=%ld quadratic(d>=2)=%ld IDfail=%ld RESfail=%ld mu>d=%ld L1fail=%ld minmarg=%ld\n",G,cnt,nq,idfail,resfail,mugtd,l1fail,minmarg); return 0; }
