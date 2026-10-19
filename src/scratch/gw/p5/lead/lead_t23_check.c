/* Lead's independent check of codex P5c three-low claims (exactly alpha=3 low A directions), P5_REPORT.md sections 24-27.
   Setting as lead_t22_check.c: 3m<c<=4m, M=c+m-1, h=c-3m, unit offsets t=n-m; A:[1,h) B:[h,h+m) C:[h+m,h+2m) E:[h+2m,h+3m).
   Cell of degree j: tau=v-jm.  Low A: 2t<h.  L = least low offset.  E units are flagged and kept outside the tile.
   Fixed arc theta=ceil(3h/2), Y=[h,min(theta,m)) u [1,theta-m); H0=h-L, Y_H=[h,min(h+H,m)) u [1,h+H-m).
   Allowed occupants: q3 (AA tau>=h), B/C/E units, s4 (AB tau>=m+h), t4 (BB tau>=m+h).  J = other occupants, J_A pure-A.
   Tile = grlex (GR=1) or lex (GR=0) normal forms.
   Samplers: 0 random, 1 highs clustered in [h-L,theta-2L), 2 spread, 3 Sidon (pairs distinct) small h, 4 Sidon h>m/2,
   5 B_3 face (units, pairs, cubics distinct), 6 B_3 face plus 1-2 forced pair coincidences, 7 all offsets near h/2 (B_3 attempt),
   8 like 7 with forced coincidences.     usage: lead_t23_check seed trials mmin mmax GR [samp] [amin] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 6000
#define DM 72
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[DM+8], X[MM][DM]; static long mg[DM]; static int isE[MM], intr[MM], intrA[MM];
#define NCHK 53
static const char *nm[NCHK]={
 "struct u3=u0+u1,k=k0+k1,q2=n0+l",      /*0*/
 "quartic pure A, tau<h, >=3 low",        /*1*/
 "A-ID (W_A formula)",                    /*2*/
 "D3=3t-(a+2)r",                          /*3*/
 "GEN-COUNT J_A",                         /*4*/
 "GEN-COUNT J-J_A",                       /*5*/
 "GLOC F1>=Phi",                          /*6*/
 "shadow 4k0<=6u0",                       /*7*/
 "shadow 3k1<=5u1",                       /*8*/
 "GEN-ROUGH P>=15-5a",                    /*9*/
 "MG6 D3>=6a-18 (a>=13,6<=q<=Q-3)",       /*10*/
 "T2.3-M: q>=6 (W_A<0)",                  /*11*/
 "T2.3-M: P+D3>=a-3",                     /*12*/
 "T2.3-M: F1n>=0 (pure+b part)",                         /*13*/
 "END eta_H nonincreasing",               /*14*/
 "END-ETA I-LOW",                         /*15*/
 "3L-STARS F1n>=0 (l>=6)",                 /*16*/
 "3L-FIX J_A sharper count",              /*17*/
 "u0+t0>=q_c",                            /*18*/
 "(a+1)u0-5k0+3t0>=2q_c",                 /*19*/
 "3L-FIX P+D3>=A-12R",                    /*20*/
 "exceptional<=l+r",                      /*21*/
 "3L-HIGHARC J_H0A count",                /*22*/
 "3L-HIGHARC P_H>=delta-B",               /*23*/
 "3L-PACK (R-l-r form)",                  /*24*/
 "3L-PACK (actual window count)",         /*25*/
 "NEAR-GAP D3>=D_r",                      /*26*/
 "3L-GAP-STARS P+D3>=0,10,9",             /*27*/
 "3L-GAP-STARS F1n>=0",                    /*28*/
 "3L-SHARP P+D3>=Ahat-12R",               /*29*/
 "3L-HSHARP P_H+D3>=delta-Bhat",          /*30*/
 "outside H0: JH-JHA<=b(3+l+r+q2)+c(3+l+r)", /*31*/
 "table region: max(F1n,F2n)>=0",           /*32*/
 "T2.3 a>=41: max(F1n,F2n)>=0",             /*33*/
 "LOC-DEF t>=t_forced",                   /*34*/
 "WINDOW-SP short",                       /*35*/
 "WINDOW-SP wide",                        /*36*/
 "WINDOW-COUNT short cubic",              /*37*/
 "WINDOW-COUNT wide cubic",               /*38*/
 "WINDOW-COUNT PSID wide",                /*39*/
 "FIN F1n>=F_rough+bB_f",                  /*40*/
 "FIN F1n>=F_cold+bB_f",                   /*41*/
 "FIN F1n>=F_raw+bB_f",                    /*42*/
 "FIN F2n>=delta-B+D3+bB_h",               /*43*/
 "c=e=0 reduction: F1>=0 if c+e>0",       /*44*/
 "OUT3b J-J_A<=b(3+beta)+3c",             /*45*/
 "a=13 n0=6 l=0 beta=6 u3=0: P+D3>=0",    /*46*/
 "Wilf",                                  /*47*/
 "C/E part fixed arc >=0",         /*48*/
 "C/E part H0 arc >=0 (r<=2)",           /*49*/
 "JOINT-SP (r<=2, eps=t-t_forced)",       /*50*/
 "JOINT-SP (any r, eps_M)",               /*51*/
 "JOINT-COUNT cubics"};                   /*52*/
static long fails[NCHK], applic[NCHK], minsl[NCHK];
static int curm; static long curW; static int g0;
static void chk(int i,long slack){ applic[i]++; if(slack<minsl[i]) minsl[i]=slack; if(slack<0){ fails[i]++; if(fails[i]<=3){ printf("FAIL %s slack=%ld m=%d W=%ld gens:",nm[i],slack,curm,curW); for(int k=0;k<g0;k++) printf(" %d",gens[k]); printf("\n"); } } }
static long C2(long x){ return x>=2? x*(x-1)/2 : 0; }
static long C3(long x){ return x>=3? x*(x-1)*(x-2)/6 : 0; }
static long key[MM]; static int cmpk(const void*x,const void*y){ long u=key[*(const int*)x], v=key[*(const int*)y]; return u<v?-1:u>v; }
static long lam(long n){ if(n<=1) return 0; if(n==2) return 1; if(n==3) return 2; if(n==4) return 4; return (n%3==0)? 3*n/2 : 3*(n-1)/2; }
/* lambda_n for n>=5 with 3 not dividing n is 3(n-1)/2, which may be a half-integer: keep doubled versions */
static long lam2(long n){ if(n<=1) return 0; if(n==2) return 2; if(n==3) return 4; if(n==4) return 8; return (n%3==0)? 3*n : 3*(n-1); }
static long mac2(long q){ long j=1; while((j+2)*(j+1)/2<=q) j++; long s=q-j*(j+1)/2; return (j+2)*(j+1)*j/6+s*(s+1)/2; }
static long Hn(long n){ return n*(C2(n)+1); }
static int okset(int *T,int nt,int m,int deg){ /* all multiset sums of size 1..deg distinct mod m and nonzero */
  static unsigned char used[MM]; memset(used,0,m); used[0]=1;
  for(int i=0;i<nt;i++){ int r=T[i]%m; if(used[r]) return 0; used[r]=1; }
  if(deg>=2) for(int i=0;i<nt;i++) for(int j=i;j<nt;j++){ int r=(T[i]+T[j])%m; if(used[r]) return 0; used[r]=1; }
  if(deg>=3) for(int i=0;i<nt;i++) for(int j=i;j<nt;j++) for(int k=j;k<nt;k++){ int r=(T[i]+T[j]+T[k])%m; if(used[r]) return 0; used[r]=1; }
  return 1; }
static int budget;
static int okset2(int *T,int nt,int m){ /* units and pairs distinct mod m and nonzero; triple collision excess <= budget */
  static unsigned char used[MM]; memset(used,0,m); used[0]=1;
  for(int i=0;i<nt;i++){ int r=T[i]%m; if(used[r]) return 0; used[r]=1; }
  for(int i=0;i<nt;i++) for(int j=i;j<nt;j++){ int r=(T[i]+T[j])%m; if(used[r]) return 0; used[r]=1; }
  int ex=0; for(int i=0;i<nt;i++) for(int j=i;j<nt;j++) for(int k=j;k<nt;k++){ int r=(T[i]+T[j]+T[k])%m; if(used[r]){ if(++ex>budget) return 0; } used[r]=1; }
  return 1; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+17; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]); int SAMP=argc>6?atoi(argv[6]):-1; int AMIN=argc>7?atoi(argv[7]):7;
  if(mmax>=MM) mmax=MM-1;
  for(int i=0;i<NCHK;i++) minsl[i]=1L<<40; long tested=0, nWAneg=0, byA[64]={0}, nrA[4]={0}, nFINapp=0;
  for(long tr=0;tr<T;tr++){
    int m=mmin+rnd()%(mmax-mmin+1); int h=8+rnd()%(m-8>0?m-8:1); if(h>=m) h=m-1;
    int samp=SAMP>=0?SAMP:(int)(rnd()%10); int na=AMIN+rnd()%(AMIN<13?10:6), nb=rnd()%4, ncc=rnd()%3, ne=rnd()%3; g0=0;
    static int TT[DM]; int nt=0;
    if(samp==9){ /* lows in [h/4,h/2) (smallest L), highs in [h-L,h): l=0 typically, near-full faces, W_A<0 regime */
      h=m/5+rnd()%(3*m/10); if(h<40) continue; int lowhi=(h-1)/2; int Lm=h/4+rnd()%((lowhi-h/4+1)>0?(lowhi-h/4+1):1);
      budget=(rnd()%3==0)?0:(int)(rnd()%(4*na+20)); int tries=0; TT[nt++]=Lm;
      while(nt<3 && tries<20000){ tries++; int t=Lm+1+rnd()%((lowhi-Lm)>0?(lowhi-Lm):1); if(t>lowhi) continue; TT[nt]=t; if(okset2(TT,nt+1,m)) nt++; }
      if(nt<3) continue; int nex=rnd()%3; tries=0;
      while(nt<na && tries<20000){ tries++; int t; if(nex>0&&rnd()%4==0){ t=(h+1)/2+rnd()%((h-Lm-(h+1)/2)>0?(h-Lm-(h+1)/2):1); } else t=h-Lm+rnd()%Lm; if(t>=h||2*t<h) continue; TT[nt]=t; if(okset2(TT,nt+1,m)){ nt++; if(t<h-Lm) nex--; } }
      if(nt<AMIN) continue;
    } else if(samp>=5){
      if(samp<=6){ h=m/4+rnd()%(3*m/4); if(h>=m) h=m-1; } else { h=m/3+rnd()%(2*m/3); if(h>=m) h=m-1; }
      if(h<40) continue;
      double eps=0.05+0.25*(rnd()%1000)/1000.0; int lo=(samp<=6)?1:(int)(h/2-eps*h), hi=(samp<=6)?(h-1):(int)(h/2+eps*h); if(lo<1) lo=1; if(hi>h-1) hi=h-1;
      int lowhi=(h-1)/2; /* low means 2t<h, i.e. t<=lowhi */
      int tries=0; budget=(rnd()%3==0)?0:(int)(rnd()%(4*na+20));
      while(nt<3 && tries<20000){ tries++; int t=lo+rnd()%((lowhi-lo+1)>0?(lowhi-lo+1):1); if(t>lowhi||t<1) continue; TT[nt]=t; if(okset2(TT,nt+1,m)) nt++; }
      if(nt<3) continue;
      int hlo=(h+1)/2; if(hlo<lo) hlo=lo; tries=0;
      while(nt<na && tries<20000){ tries++; int t=hlo+rnd()%((hi-hlo+1)>0?(hi-hlo+1):1); if(t>=h) continue; TT[nt]=t; if(okset2(TT,nt+1,m)) nt++; }
      if(nt<AMIN) continue;
      if(samp==6||samp==8){ /* force 1-2 pair coincidences t_k+t_new = t_i+t_j with new high offset */
        int nf=1+rnd()%2; for(int f=0;f<nf;f++){ for(int tt=0;tt<200;tt++){ int i=rnd()%nt,j=rnd()%nt,k=rnd()%nt; int t=TT[i]+TT[j]-TT[k]; if(k==i||k==j) continue; if(2*t<h||t>=h) continue; int dup=0; for(int q=0;q<nt;q++) if(TT[q]==t) dup=1; if(dup) continue; if(nt<DM-8){ TT[nt++]=t; break; } } } }
    } else if(samp>=3){
      if(samp==4){ h=m/2+rnd()%(m/2); if(h>=m) h=m-1; } else { h=8+rnd()%(m/3>8?m/3-8:1); }
      int lowhi=(h-1)/2; if(lowhi<3) continue; int tries=0;
      while(nt<3 && tries<5000){ tries++; int t=1+rnd()%lowhi; TT[nt]=t; if(okset(TT,nt+1,m,2)) nt++; }
      if(nt<3) continue;
      int L0=TT[0]; for(int i=1;i<3;i++) if(TT[i]<L0) L0=TT[i];
      int lo2=h-L0; if(rnd()%3==0) lo2=(h+1)/2; tries=0;
      while(nt<na && tries<8000){ tries++; int t=lo2+rnd()%(h-lo2>0?h-lo2:1); if(t>=h||2*t<h) continue; TT[nt]=t; if(okset(TT,nt+1,m,2)) nt++; }
      if(nt<AMIN) continue;
    } else {
      int lowhi=(h-1)/2; if(lowhi<3) continue;
      int Ls[3]; for(int i=0;i<3;i++){ Ls[i]=1+rnd()%lowhi; TT[nt++]=Ls[i]; }
      int L0=Ls[0]; if(Ls[1]<L0) L0=Ls[1]; if(Ls[2]<L0) L0=Ls[2];
      int lo=(h+1)/2, hi=h-1; if(hi<lo) continue;
      for(int k=3;k<na;k++){ int t;
        if(samp==1){ int H0=h-L0; int w=(3*h+1)/2-2*L0-H0; if(w<1) w=1; t=H0+rnd()%w; if(t>hi) t=hi; if(t<lo) t=lo; }
        else t=lo+rnd()%(hi-lo+1);
        TT[nt++]=t; }
    }
    for(int i=0;i<nt;i++) gens[g0++]=m+TT[i];
    for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m; for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m; for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m;
    long Ct=3L*m+h;
    /* Apery set by Dijkstra over residues */
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    for(int r=1;r<m;r++){ long f=Ct+((r-Ct%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3L*m && c<=4L*m)) continue;
    long H=c-3L*m;
    int d=0, ok=1, e=0; memset(mg,0,sizeof mg);
    for(int r=1;r<m;r++){ isE[r]=0; int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; }
        if(!dec){ if(ap[r]-m>=H+2*m){ e++; isE[r]=1; } else { if(d>=DM){ok=0;break;} mg[d++]=ap[r]; } } }
    if(!ok) continue;
    int cls[DM], low[DM]; int a=0,b=0,cc=0,nlow=0; long tof[DM]; int lowid[3];
    for(int i=0;i<d;i++){ long tt=mg[i]-m; tof[i]=tt; low[i]=0; if(tt<H){cls[i]=0;a++; if(2*tt<H){ if(nlow<3) lowid[nlow]=i; low[i]=1; nlow++; }} else if(tt<H+m){cls[i]=1;b++;} else {cls[i]=2;cc++;} }
    if(a<AMIN||nlow!=3) continue;
    long L=tof[lowid[0]]; for(int i=1;i<3;i++) if(tof[lowid[i]]<L) L=tof[lowid[i]];
    int lowix[DM]; for(int i=0;i<d;i++) lowix[i]=-1; for(int i=0;i<3;i++) lowix[lowid[i]]=i;
    static int ord[MM]; for(int r=0;r<m;r++) ord[r]=r;
    /* sort residues by Apery value (insertion sort is O(m^2); use simple counting by qsort) */
    { static long key[MM]; for(int r=0;r<m;r++) key[r]=ap[r]*MM+r;
      int cmp(const void*x,const void*y){ long u=key[*(const int*)x], v=key[*(const int*)y]; return u<v?-1:u>v; }
      qsort(ord,m,sizeof(int),cmp); }
    for(int q=0;q<d;q++) X[0][q]=0;
    for(int ii=1;ii<m&&ok;ii++){ int r=ord[ii]; long w=ap[r]; if(isE[r]){ for(int q=0;q<d;q++) X[r][q]=0; continue; } int found=0,bdeg=1<<30; static int best[DM],cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int t2=(int)((w-mg[j])%m); if(ap[t2]==w-mg[j]&&!isE[t2]){ int cd=0; for(int q=0;q<d;q++){ cand[q]=X[t2][q]+(q==j); cd+=cand[q]; }
        int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int q=0;q<d;q++) if(cand[q]!=best[q]){ better=cand[q]>best[q]; break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found) ok=0; else for(int q=0;q<d;q++) X[r][q]=best[q]; }
    if(!ok) continue;
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)(d+e)*l-g;
    curm=m; curW=W; tested++; chk(47,W); if(a<64) byA[a]++;
    /* counts */
    long q2=0,q3=0,u3=0,u4=0,k=0,s3=0,t3=0,n0=0,lp[3]={0,0,0},u0=0,u1=0,k0=0,k1=0,beta=0,c0=0,nAC=0,nBC=0; int badq=0, badstruct=0;
    long hc=(H+1)/2, theta=(3*H+1)/2;
    for(int r=1;r<m;r++){ intr[r]=0; intrA[r]=0; if(isE[r]) continue; int deg=0,nA=0,nB=0,nC=0,nl=0,lowf=-1; for(int q=0;q<d;q++){ int xq=X[r][q]; deg+=xq; if(!xq) continue; if(cls[q]==0) nA+=xq; else if(cls[q]==1) nB+=xq; else nC+=xq; if(low[q]){ nl+=xq; lowf=lowix[q]; } }
      long tau=ap[r]-(long)deg*m;
      if(deg==2&&nA==2){ if(tau<H) q2++; else q3++; }
      if(deg==3&&nA==3){ if(tau<H){ u3++; if(nl<=1) badstruct=1; } else u4++; }
      if(deg==4){ k++; if(nA!=4||tau>=H||nl<3) badq=1; if(nl==4) k0++; if(nl==3) k1++; }
      if(deg==2&&nA==1&&nB==1&&tau<m+H) s3++;
      if(deg==2&&nB==2&&tau<m+H) t3++;
      if(deg==2&&nA==1&&nC==1) nAC++;
      if(deg==2&&nB==1&&nC==1) nBC++;
      if(deg==2&&nl==2){ n0++; if(tau<hc) beta++; }
      if(deg==2&&nA==2&&nl==1&&tau<H) lp[lowf]++;
      if(deg==3&&nl==3){ c0++; if(tau<H) u0++; }
      if(deg==3&&nl==2&&nA==3&&tau<H) u1++;
      int allA=(nA==deg); int allowed=0;
      if(deg==2&&nA==2&&tau>=H) allowed=1; if(deg==1&&!allA) allowed=1; if(deg==2&&nA==1&&nB==1&&tau>=m+H) allowed=1; if(deg==2&&nB==2&&tau>=m+H) allowed=1;
      if(!allowed){ intr[r]=1; intrA[r]=allA; } }
    long lsum=lp[0]+lp[1]+lp[2];
    long q=q2+q3, Q=(long)a*(a+1)/2, rA=Q-q, U=(long)a*(a+1)*(a+2)/6, uu=u3+u4, tA=U-uu, F=C3(a+1), p=a-3;
    if(rA<=3) nrA[rA]++;
    chk(0, (u3==u0+u1 && k==k0+k1 && q2==n0+lsum && !badstruct)?0:-1);
    chk(1, badq?-1:0);
    long D3=(long)(a+2)*q-3*uu, LC=(long)(a+1)*(q2+u3)-4*k;
    chk(3, D3==3*tA-(long)(a+2)*rA?0:-1);
    long WA=0; { long FA=0; for(int r=0;r<m;r++){ if(r&&isE[r]) continue; int allA=1; for(int q4=0;q4<d;q4++) if(X[r][q4]&&cls[q4]!=0) allA=0; if(allA){ FA++; WA+=(long)(a+1)*((M-ap[r])/m); } } WA-=(M/m)*FA; }
    chk(2, WA==-F+LC-(long)(a-3)*rA+4*tA?0:-1);
    if(WA<0) nWAneg++;
    /* arcs */
    long H0=H-L; long J=0,JA=0,JH=0,JHA=0,qc=0;
    for(int r=1;r<m;r++){ if(!intr[r]) continue; int inY=((r>=H&&r<theta&&r<m)||(r>=1&&r<theta-m)); int inYH=((r>=H&&r<H+H0&&r<m)||(r>=1&&r<H+H0-m));
      if(inY){ J++; if(intrA[r]) JA++; int deg=0,nl=0; for(int q4=0;q4<d;q4++){ deg+=X[r][q4]; if(low[q4]) nl+=X[r][q4]; } if(deg==2&&nl==2&&r<theta-m) qc++; }
      if(inYH){ JH++; if(intrA[r]) JHA++; } }
    long P=(a-1)+LC+2*q2+k-2*JA;
    long delta=H-2*L; long PH=(a-1)+LC+2*q2+k+delta-2*JHA;
    long G=(long)cc*(cc+e+1)+(long)e*(3*a+2*b-1)+(long)(cc+e)*(q3+s3+t3);
    long A2=(long)(a-1)*(b+1)+G+LC+(long)b*u3+(long)(cc+e)*(2*q2+u3)+D3;
    long F1=A2+(b+2)*q2+k-2*J, F2=A2+(b+2)*q2+k-(-delta+2*JH);
    long CEf=G+(long)(cc+e)*(2*q2+u3)-6L*cc;            /* C/E part, fixed arc (outside C cost 2*3c) */
    long CEh=G+(long)(cc+e)*(2*q2+u3)-2L*cc*(3+lsum+rA); /* C/E part, H0 arc */
    long F1n=F1-CEf, F2n=F2-CEh;                          /* pure + b parts only */
    long Sl=0, CS=0; for(int i=0;i<3;i++){ Sl+=lp[i]*(a+2-lp[i]); CS+=C2(lp[i]+1); }
    /* GEN-COUNT, GLOC */
    chk(4, 3+n0+c0+k0+p*n0-u1+CS-JA);
    chk(5, (long)b*(3+n0)+3L*cc-(J-JA));
    { long Phi=D3+(a-1)-6-2*c0+(7-a)*n0+Sl+(a+1)*u0-5*k0+(a+3)*u1-3*k1+(long)b*(a-1+q2+u3-6-2*n0)+G+(long)(cc+e)*(2*q2+u3)-6L*cc;
      chk(6, F1-Phi); }
    chk(7, 6*u0-4*k0); chk(8, 5*u1-3*k1);
    chk(9, P+5L*a-15);
    if(a>=13 && q>=6 && q<=Q-3) chk(10, D3-(6L*a-18));
    if(a>=13 && rA>=3 && WA<0){ chk(11, q-6); chk(12, P+D3-(a-3)); chk(13, F1n); }
    /* END */
    if(H>=2){ long JHh=0; long hc2=(H+1)/2;
      for(int r=1;r<m;r++) if(intr[r]){ int in=((r>=H&&r<H+hc2&&r<m)||(r>=1&&r<H+hc2-m)); if(in) JHh++; }
      long prev=H-2*hc2+2*JHh; int mono=1; long Hh;
      for(Hh=hc2;Hh<H-1;Hh++){ int res=(int)((H+Hh)%m); if(res!=0&&intr[res]) JHh++; long et=H-2*(Hh+1)+2*JHh; if(et>prev) mono=0; prev=et; }
      chk(14, mono?0:-1);
      long JHm1=JHh; /* now J_{h-1} */
      long eend=2-H+2*JHm1; if(3*delta<eend) eend=3*delta;
      long ls=eend-(b+2)*q2-k; if(ls<0) ls=0; chk(15, W-(A2-ls)); }
    long r=rA, e0=lsum+rA;

    long R=0, exc=0, nwin=0; for(int i=0;i<d;i++) if(cls[i]==0&&!low[i]){ if(tof[i]<theta-2*L) R++; if(tof[i]<H0) exc++; if(tof[i]>=H-L&&tof[i]<theta-2*L) nwin++; }
    if(a>=13){
      if(lsum>=6) chk(16, F1n);
      if(r<=2&&lsum<=5){
        long t0=10-c0;
        chk(17, 13+qc+k0+n0*R-u1+CS-JA);
        chk(18, u0+t0-qc);
        chk(19, (a+1)*u0-5*k0+3*t0-2*qc);
        long Arl=(7+lsum-2*r)*a-9+2*lsum-lsum*lsum-5*r;
        chk(20, P+D3-(Arl-12*R));
        chk(21, lsum+r-exc);
        long Brl=(5+5*lsum+7*r)*a-15-17*lsum-13*r+2*C3(lsum+r+2);
        chk(22, 19+lsum+e0+C3(e0+2)+(6+3*e0)*(a-3)+k-JHA);
        chk(23, PH-(delta-Brl));
        { long n=R-lsum-r; if(n<0) n=0; long w=(delta+1)/2; chk(24, (2*w-2+2*r*(r+1))-n*(n-1)); chk(25, (2*w-2+2*r*(r+1))-nwin*(nwin-1)); }
        long Dr = r==0?0 : r*(4*a-3*r-1)/2;
        if(r>=1) chk(26, D3-Dr);
        if(lsum>=5-2*r){ long tgt = r==0?0 : (r==1?10:9); chk(27, P+D3-tgt); chk(28, F1n); }
        long Ahat = r==0? Arl : (7+r+lsum)*a-21+2*lsum-lsum*lsum-r*(3*r+7)/2;
        chk(29, P+D3-(Ahat-12*R));
        long Bhat=Brl-Dr; chk(30, PH+D3-(delta-Bhat));
        chk(31, (long)b*(3+lsum+r+q2)+(long)cc*(3+lsum+r)-(JH-JHA));
        static const int TAB[3][6]={{16,26,33,37,41,43},{32,37,40,43,45,47},{39,42,44,46,47,49}};
        if(a>=TAB[r][lsum]) chk(32, F1n>F2n?F1n:F2n);
        /* section 27 */
        long tf = r==0?0 : (r==1? a : 2*a-1);
        chk(34, tA-tf);
        long eps=tA-tf; long w=(delta+1)/2;
        { long ns=R-lsum-2*r; if(ns<0) ns=0; long nw=R-r; if(nw<0) nw=0;
          chk(35, 2*(3*w-2)-(2*Hn(ns)-lam2(ns)*eps));
          chk(36, 2*(3*delta-2)-(2*Hn(nw)-lam2(nw)*eps)); }
        { long nc=R-lsum-r; if(nc<0) nc=0; chk(37, (3*w-2)-(C3(nc+2)-tA)); chk(38, (3*delta-2)-(C3(R+2)-tA)); chk(39, (2*delta-2+2*r*(r+1))-R*(R-1)); }
        if(lsum<=4-2*r){ nFINapp++;
          long Fr=15-5L*a+Sl+D3, Fc=a-27+(a+3)*n0+Sl-2*n0*R-(a+2)*r, Fw=a-39+(a+3)*n0+Sl-2*n0*R+D3;
          long Bf=a-7-n0+lsum; if(a==13&&Bf<1) Bf=1; long Bh=a-7-n0-3*lsum-2*r;
          long Bbig=2*(13+n0+lsum+e0+C3(e0+2)+(n0+3*e0)*(a-3))-(a-1)-(a+3)*(n0+lsum);
          int a13excl = (a==13 && a-7-n0+lsum<1 && beta==6 && u3==0); /* closed separately (check 46) */
          if(!a13excl){ chk(40, F1n-(Fr+(long)b*Bf)); chk(41, F1n-(Fc+(long)b*Bf)); chk(42, F1n-(Fw+(long)b*Bf)); }
          chk(43, F2n-(delta-Bbig+D3+(long)b*Bh)); }
      }
      if(r<=2&&cc+e>0) chk(44, F1);
      chk(48, CEf); if(r<=2) chk(49, CEh);
      if(a>=41&&r<=2) chk(33, F1n>F2n?F1n:F2n);
      chk(45, (long)b*(3+beta)+3L*cc-(J-JA));
      { long sj=(3*delta+1)/2; long nj=3+R-r; if(nj<0) nj=0; long epsM=mac2(q)-uu;
        if(r<=2){ long tf = r==0?0 : (r==1? a : 2*a-1); chk(50, 2*(3*sj-2)-(2*Hn(nj)-lam2(nj)*(tA-tf))); }
        chk(51, 2*(3*sj-2)-(2*Hn(nj)-lam2(nj)*epsM));
        chk(52, (3*sj-2)-(C3(3+R+2)-tA)); }
      if(a==13&&n0==6&&lsum==0&&beta==6&&u3==0) chk(46, P+D3);
    }
  }
  printf("seed=%s GR=%d samp=%d tested(three low A, a>=%d, 3m<c<=4m)=%ld  W_A<0: %ld  rA=0,1,2,3: %ld %ld %ld %ld  FIN-applicable %ld\n  by a:",argv[1],GR,SAMP,AMIN,tested,nWAneg,nrA[0],nrA[1],nrA[2],nrA[3],nFINapp);
  for(int i=7;i<64;i++) if(byA[i]) printf(" %d:%ld",i,byA[i]); printf("\n");
  for(int i=0;i<NCHK;i++) printf("  %-44s applicable %8ld  fails %6ld  min slack %ld\n",nm[i],applic[i],fails[i],applic[i]?minsl[i]:0);
  return 0; }
