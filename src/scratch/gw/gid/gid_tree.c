/* General cell identity G-ID on all semigroups (genus <= G), lex down-set factorization (as p5_tree.c).
   W = sum_{y!=0} lam(y) phi(y) + sum_x sum_a x_a beta_{x,a} - sum_x gamma(x),
   phi(y) = sum_{a: y+e_a not in D} (y_a+1); beta_{x,a} = [eps_x + r_a >= m]; gamma(x) = floor(sum x_a r_a / m).
   Profiles deficient cells (c_x < 0): degree, lam, phi, residue window position.  usage: gid_tree G */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
typedef unsigned __int128 u128;
#define PM 80
#ifndef GRADED
#define GRADED 1
#endif
static int G; static long cnt, idfail, nsg;
static long defcnt[8][3][4]; /* [degree][lam==0,lam==1,lam>=2][window: s<=mu, mu<s<=2mu, 2mu<s<=3mu, >3mu] */
static long defsum, maxdef; static long qfail[8], qcnt[8], qmin[8], qfail3=0, qcnt3=0, qmin3=1L<<40; static long winfail, winfail2, nondefpos, fb=0, fc=0, fd=0, fe=0, nmu=0; static long minwin=1L<<40; static long pos_win1_zero; static long sgdef;
static int gapq(u128 g,int z){return z<128&&((g>>z)&1);}
static void analyze(u128 gm,int F,int m,int *gens,int e){
  int ap[PM],M=0,ng[PM],d=0; static int X[PM][PM];
  for(int i=0;i<e;i++) if(gens[i]!=m) ng[d++]=gens[i];
  if(d<1) return;
  for(int r=0;r<m;r++){int w=r;while(gapq(gm,w))w+=m;ap[r]=w;if(w>M)M=w;}
  int ready[PM]={0}; ready[0]=1; for(int h=0;h<d;h++) X[0][h]=0;
  for(int w=1;w<=M;w++){ int r=w%m; if(ap[r]!=w) continue; int found=0; int best[PM]; int bdeg=1<<30;
    for(int j=0;j<d;j++) if(w>=ng[j]){ int t=(w-ng[j])%m; if(ap[t]==w-ng[j]){ assert(ready[t]); int cand[PM]; int cd=0; for(int h=0;h<d;h++){ cand[h]=X[t][h]+(h==j); cd+=cand[h]; }
        int better=0; if(!found) better=1; else if(GRADED && cd<bdeg) better=1; else if(!GRADED || cd==bdeg){ for(int h=0;h<d;h++){ if(cand[h]!=best[h]){ better=(cand[h]>best[h]); break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
    assert(found); for(int h=0;h<d;h++) X[r][h]=best[h]; ready[r]=1; }
  nsg++;
  int mu=M%m; long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
  /* membership: cell y+e_a in D iff the residue (ap[r]+ng[a])%m has X equal to y+e_a */
  long tot=0; int anydef=0; int maxdeg=0; long Qwin=0, Qdebt=0, Qoth=0; long credit=0, debt=0, debtall=0, Fu=0, cl1=0, cpar=0, ctop=0; int hi=(2*mu<=m-1)?2*mu:m-1;
  for(int r=1;r<m;r++){ int lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; int deg=0;
    for(int a=0;a<d;a++){ deg+=X[r][a]; sr+=(long)X[r][a]*(ng[a]%m);
      if(X[r][a]) B+=(long)X[r][a]*((eps+ng[a]%m)>=m);
      int t=(ap[r]+ng[a])%m; int in=(ap[t]==ap[r]+ng[a]); if(in){ for(int h=0;h<d;h++) if(X[t][h]!=X[r][h]+(h==a)){in=0;break;} }
      if(!in) phi+=X[r][a]+1; }
    long gam=sr/m; long cx=(long)lam*phi+B-gam; tot+=cx;
    if(deg>maxdeg) maxdeg=deg; if(deg==1) Qwin+=cx; else if(r>mu && r<=hi) Qwin+=cx; else if(cx<0) Qdebt+=-cx; else Qoth+=cx;
    if(deg==1) Fu+=cx; else if(lam>=1) cl1+=(cx>0?cx:0); else if(cx>0) ctop+=cx;
    if(r>mu && r<=hi) credit+=cx; if(cx<0){ debtall+=-cx; if(r<=mu) debt+=-cx; }
    if(cx<0){ anydef=1; int dg=deg<7?deg:7; int lc=lam<2?lam:2; int s=r; int wi= s<=mu?0: (s<=2*mu?1:(s<=3*mu?2:3)); defcnt[dg][lc][wi]++; defsum+=-cx; if(-cx>maxdef) maxdef=-cx; }
    if(cx==0 && r>mu && r<=2*mu && deg>=2) pos_win1_zero++;
  }
  if(d>=3){ qcnt3++; long q3=Qwin-Qdebt; if(q3<0){ qfail3++; if(qfail3<6){ printf("D3FAIL m=%d d=%d mu=%d K=%d W=%ld Qwin=%ld Qdebt=%ld gens:",m,d,mu,M/m,W,Qwin,Qdebt); for(int a=0;a<d;a++) printf(" %d",ng[a]); printf("\n"); } } if(q3<qmin3) qmin3=q3; }
  { int md=maxdeg<7?maxdeg:7; qcnt[md]++; long q=Qwin-Qdebt; if(0&&q<0){ qfail[md]++; if(md==3||md==4){ printf("QFAIL m=%d mu=%d K=%d M=%d W=%ld Qwin=%ld Qdebt=%ld gens:",m,mu,M/m,M,W,Qwin,Qdebt); for(int a=0;a<d;a++) printf(" %d",ng[a]); printf("\n");
      for(int r=1;r<m;r++){ int lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; for(int a=0;a<d;a++){ sr+=(long)X[r][a]*(ng[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+ng[a]%m)>=m); int t=(ap[r]+ng[a])%m; int in=(ap[t]==ap[r]+ng[a]); if(in){ for(int h=0;h<d;h++) if(X[t][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
        long cx=(long)lam*phi+B-sr/m; printf("   r=%2d w=%3d lam=%d phi=%ld B=%ld gam=%ld c=%ld x=(",r,ap[r],lam,phi,B,sr/m,cx); for(int a=0;a<d;a++) printf("%d",X[r][a]); printf(")%s\n", r<=mu?" CROWN":(r<=hi?" WIN":"")); } } } if(qcnt[md]==1||q<qmin[md]) qmin[md]=q; }
  if(mu==m-1) nmu++; if(debtall>credit+Fu) fb++; if(debtall>credit+cl1) fc++; if(debtall>Fu) fd++; if(debtall>cl1+ctop) fe++;
  if(0&&credit<debt){ winfail++; if(winfail<=6){ printf("WINFAIL m=%d mu=%d K=%d M=%d W=%ld credit=%ld debt=%ld gens:",m,mu,M/m,M,W,credit,debt); for(int a=0;a<d;a++) printf(" %d",ng[a]); printf("\n");
      for(int r=1;r<m;r++){ int lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; for(int a=0;a<d;a++){ sr+=(long)X[r][a]*(ng[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+ng[a]%m)>=m); int t=(ap[r]+ng[a])%m; int in=(ap[t]==ap[r]+ng[a]); if(in){ for(int h=0;h<d;h++) if(X[t][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
        long cx=(long)lam*phi+B-sr/m; printf("   r=%2d w=%3d lam=%d phi=%ld B=%ld gam=%ld c=%ld x=(",r,ap[r],lam,phi,B,sr/m,cx); for(int a=0;a<d;a++) printf("%d",X[r][a]); printf(")%s\n", r<=mu?" LOW":(r<=hi?" WIN":"")); } } } if(credit<debtall) winfail2++; if(credit-debtall<minwin && debtall>0){ minwin=credit-debtall; }
  if(tot!=W){ idfail++; if(idfail<5) printf("ID FAIL m=%d W=%ld tot=%ld\n",m,W,tot); }
  if(anydef) sgdef++;
}
static void visit(u128 gm,int F,int m,int *gens,int e,int genus){
  cnt++; if(m>1&&m<PM) analyze(gm,F,m,gens,e);
  if(genus==G) return; int ng[PM*2];
  for(int j=0;j<e;j++){ int nn=gens[j]; if(nn<=F) continue; u128 gm2=gm|((u128)1<<nn); int e2=0,m2;
    if(nn==m){ m2=m+1; for(int k=m2;k<=2*m2-1;k++) ng[e2++]=k; }
    else { m2=m; for(int k=0;k<e;k++) if(gens[k]!=nn) ng[e2++]=gens[k]; int y=nn+m,dec=0; for(int a=m;a<=y/2&&!dec;a++) if(!gapq(gm2,a)&&!gapq(gm2,y-a)) dec=1; if(!dec) ng[e2++]=y; }
    visit(gm2,nn,m2,ng,e2,genus+1); }
}
int main(int argc,char**argv){ G=atoi(argv[1]); int gens[]={1}; visit(0,-1,1,gens,1,0);
  printf("d>=3: S=%ld  WQ fails=%ld  min(Qwin-Qdebt)=%ld\n",qcnt3,qfail3,qmin3); for(int md=1;md<8;md++) if(qcnt[md]) printf("maxdeg=%d: S=%ld  Q=units+window-debt <0: %ld  minQ=%ld\n",md,qcnt[md],qfail[md],qmin[md]); printf("debt>credit+Funits: %ld | debt>credit+pos(lam>=1 nonunit): %ld | debt>Funits: %ld | debt>pos nonunit cells: %ld | mu=m-1: %ld\n",fb,fc,fd,fe,nmu); printf("WIN (credit in (mu,2mu] >= debt in [1,mu]) fails: %ld ; credit >= all debt fails: %ld ; min(credit-alldebt | debt>0)=%ld\n",winfail,winfail2,minwin); printf("genus<=%d all=%ld analyzed=%ld IDfail=%ld S_with_deficit=%ld total_deficit=%ld maxdef=%ld zero-c pairs+ in (mu,2mu]: %ld\n",G,cnt,nsg,idfail,sgdef,defsum,maxdef,pos_win1_zero);
  const char*wn[4]={"s<=mu","(mu,2mu]","(2mu,3mu]",">3mu"};
  for(int dg=2;dg<8;dg++) for(int lc=0;lc<3;lc++){ long t=0; for(int w=0;w<4;w++) t+=defcnt[dg][lc][w]; if(!t) continue;
    printf("deg=%d lam=%s:",dg,lc==0?"0":(lc==1?"1":">=2")); for(int w=0;w<4;w++) printf(" %s=%ld",wn[w],defcnt[dg][lc][w]); printf("\n"); }
  return 0; }
