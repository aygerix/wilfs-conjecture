/* Lead's independent check of codex P5c Theorem T2.2 (exactly two low A directions), P5_REPORT.md sections 20-23.
   Setting: 3m<c<=4m, M=c+m-1, h=c-3m, unit offsets t=n-m; A:[1,h) B:[h,h+m) C:[h+m,h+2m) E:[h+2m,h+3m).
   Cell of degree j: tau=v-jm.  Low A: 2t<h.  x,y = the two low directions, L=t_x<=t_y.
   Fixed arc theta=ceil(3h/2), Y=[h,min(theta,m)) u [1,theta-m); H0=h-L, Y_H=[h,min(h+H0,m)) u [1,h+H0-m).
   Allowed occupants: q3 (AA tau>=h), B/C/E units, s4 (AB tau>=m+h), t4 (BB tau>=m+h).  J = other occupants, J_A pure-A.
   Checks every displayed inequality of sections 20-23 under its hypotheses, plus I-LOW for both arcs and PAY2.
   Tile = grlex (GR=1) or lex (GR=0) normal forms.  Samplers: 0 random offsets, 1 high offsets clustered near h-L
   (exercises R, SIDON2), 2 high offsets spread in [ceil(h/2),h).   usage: lead_t22_check seed trials mmin mmax GR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 2400
#define DM 64
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[DM], X[MM][DM]; static long mg[DM];
#define NCHK 32
static const char *nm[NCHK]={"struct u3=u0+u1,k=k0+k1,q2=n0+l","quartic tau<h & <=1 high","2L-SH","2L-COUNT","2L-ROUGH","2L-STARS","2L-MISS D3","2L-MISS P+D3",
 "COLD2","FIX J_A count","2L-FIX","exceptional<=l","2L-HCOUNT","2L-HIGHARC","SIDON2","ALT2","OUT2","OUT2b","HOUT2","I-LOW fixed","I-LOW H0","PAY2 max","PAY2-F bound","PAY2 fixed (rA>0|l>=2, a>=8)","Wilf",
 "","","","","","",""};
static long fails[NCHK], applic[NCHK], minsl[NCHK];
static void chk(int i,long slack,int m,long W){ applic[i]++; if(slack<minsl[i]) minsl[i]=slack; if(slack<0){ fails[i]++; if(fails[i]<=3){ printf("FAIL %s slack=%ld m=%d W=%ld gens:",nm[i],slack,m,W); for(int a=0;a<DM&&mg[a];a++) ; printf("\n"); } } }
static long C2(long x){ return x*(x-1)/2; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+17; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]); int SAMP=argc>6?atoi(argv[6]):-1;
  for(int i=0;i<NCHK;i++) minsl[i]=1L<<40; long tested=0, nrA0=0, nWAneg=0, nWAneg0=0, nB7=0, nB7b3=0, nB7neg=0;
  for(long tr=0;tr<T;tr++){
    int m=mmin+rnd()%(mmax-mmin+1); int h=8+rnd()%(m-8>0?m-8:1); if(h>=m) h=m-1; long Ct=3L*m+h;
    int samp=SAMP>=0?SAMP:(int)(rnd()%5); int na=7+rnd()%10, nb=rnd()%4, ncc=rnd()%3, ne=rnd()%3; int g0=0;
    if(samp==5){ /* B_3 A-face: all multiset sums of size <=3 distinct mod m (Eliahou-Fromentin type), two low, rest high */
      h=m/4+rnd()%(3*m/4); if(h>=m) h=m-1; if(h<16) continue; Ct=3L*m+h; na=7+rnd()%6;
      int Lx=1+rnd()%((h-1)/2), Ly=Lx+rnd()%((h-1)/2-Lx+1); if(2*Ly>=h) continue;
      static int T[64]; int nt=0; T[nt++]=Lx; T[nt++]=Ly; int tries=0; int lo2=(h+1)/2;
      static unsigned char used[4*2400];
      while(nt<na && tries<3000){ tries++; int t=lo2+rnd()%(h-lo2>0?h-lo2:1); if(t>=h) continue; int okk=1;
        for(int i=0;i<nt&&okk;i++) if(T[i]==t) okk=0; if(!okk) continue;
        int nn=nt+1; T[nt]=t; memset(used,0,m);
        for(int i=0;i<nn&&okk;i++){ int r1=(T[i])%m; if(used[r1]) okk=0; used[r1]=1; }
        for(int i=0;i<nn&&okk;i++) for(int j=i;j<nn&&okk;j++){ int r2=(T[i]+T[j])%m; if(used[r2]) okk=0; used[r2]=1; }
        for(int i=0;i<nn&&okk;i++) for(int j=i;j<nn&&okk;j++) for(int k2=j;k2<nn&&okk;k2++){ int r3=(T[i]+T[j]+T[k2])%m; if(used[r3]) okk=0; used[r3]=1; }
        if(used[0]) okk=0;
        if(okk) nt++; }
      if(nt<7) continue; for(int i=0;i<nt;i++) gens[g0++]=m+T[i];
      for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m; for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m; for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m; }
    else if(samp>=3){ /* Sidon A-face: full quadratic, few low-high I2 pairs */
      if(samp==4){ h=m/2+rnd()%(m/2); if(h>=m) h=m-1; } else { h=8+rnd()%(m/3>8?m/3-8:1); } Ct=3L*m+h; na=7+rnd()%4;
      int Lx=1+rnd()%((h-1)/2), Ly=Lx+rnd()%((h-1)/2-Lx+1); if(2*Ly>=h) continue;
      static int T[64]; int nt=0; T[nt++]=Lx; T[nt++]=Ly; int tries=0; int lo2=h-Lx; if(rnd()%3==0) lo2=(h+1)/2;
      while(nt<na && tries<4000){ tries++; int t=lo2+rnd()%(h-lo2>0?h-lo2:1); if(t>=h||2*t<h) continue; int okk=1;
        for(int i=0;i<nt&&okk;i++) if(T[i]==t) okk=0;
        /* pairwise sums distinct mod m, and not equal to an offset mod m */
        for(int i=0;i<=nt&&okk;i++) for(int j=i;j<=nt&&okk;j++){ int si=(i==nt?t:T[i])+(j==nt?t:T[j]);
          for(int i2=0;i2<=nt&&okk;i2++) for(int j2=i2;j2<=nt&&okk;j2++){ if(i2==i&&j2==j) continue; int s2=(i2==nt?t:T[i2])+(j2==nt?t:T[j2]); if((si-s2)%m==0) okk=0; }
          for(int k2=0;k2<=nt&&okk;k2++){ int tk=(k2==nt?t:T[k2]); if((si-tk)%m==0) okk=0; } }
        if(okk) T[nt++]=t; }
      if(nt<7) continue; for(int i=0;i<nt;i++) gens[g0++]=m+T[i];
      for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m; for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m; for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m; }
    else {
    int Lx=1+rnd()%((h-1)/2), Ly=Lx+rnd()%((h-1)/2-Lx+1); if(2*Ly>=h) continue; gens[g0++]=m+Lx; gens[g0++]=m+Ly;
    int lo=(h+1)/2, hi=h-1; if(hi<lo) continue;
    for(int k=2;k<na;k++){ int t;
      if(samp==1){ int H0=h-Lx; int w=(3*h+1)/2-2*Lx-H0; if(w<1) w=1; t=H0+rnd()%w; if(t>hi) t=hi; if(t<lo) t=lo; }
      else t=lo+rnd()%(hi-lo+1);
      gens[g0++]=m+t; }
    for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m;
    for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m;
    for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    for(int r=1;r<m;r++){ long f=Ct+((r-Ct%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3L*m && c<=4L*m)) continue;
    long H=c-3L*m; static int isE[MM];
    int d=0, ok=1, e=0; memset(mg,0,sizeof mg); for(int r=1;r<m;r++){ isE[r]=0; int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; }
        if(!dec){ if(ap[r]-m>=H+2*m){ e++; isE[r]=1; } else { if(d>=DM){ok=0;break;} mg[d++]=ap[r]; } } }
    if(!ok) continue;
    int cls[DM], low[DM]; int a=0,b=0,cc=0,nlow=0, xl=-1, yl=-1; long tof[DM];
    for(int i=0;i<d;i++){ long tt=mg[i]-m; tof[i]=tt; low[i]=0; if(tt<H){cls[i]=0;a++; if(2*tt<H){ low[i]=1; nlow++; }} else if(tt<H+m){cls[i]=1;b++;} else {cls[i]=2;cc++;} }
    if(a<7||nlow!=2) continue;
    for(int i=0;i<d;i++) if(low[i]){ if(xl<0) xl=i; else yl=i; } if(tof[yl]<tof[xl]){ int tmp=xl; xl=yl; yl=tmp; }
    long L=tof[xl];
    int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
    for(int q=0;q<d;q++) X[0][q]=0;
    for(int ii=1;ii<m&&ok;ii++){ int r=ord[ii]; long w=ap[r]; if(isE[r]){ for(int q=0;q<d;q++) X[r][q]=0; continue; } int found=0,bdeg=1<<30; static int best[DM],cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int t2=(int)((w-mg[j])%m); if(ap[t2]==w-mg[j]){ int cd=0; for(int q=0;q<d;q++){ cand[q]=X[t2][q]+(q==j); cd+=cand[q]; }
        int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int q=0;q<d;q++) if(cand[q]!=best[q]){ better=cand[q]>best[q]; break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found) ok=0; else for(int q=0;q<d;q++) X[r][q]=best[q]; }
    if(!ok) continue;
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)(d+e)*l-g;
    tested++; chk(24,W,m,W);
    /* counts */
    long q2=0,q3=0,u3=0,u4=0,k=0,s3=0,t3=0,n0=0,lx=0,ly=0,u0=0,u1=0,k0=0,k1=0,beta=0,c0=0; int badq=0, badstruct=0;
    long hc=(H+1)/2, theta=(3*H+1)/2;
    for(int r=1;r<m;r++){ if(isE[r]) continue; int deg=0,nA=0,nB=0,nC=0,nE=0,nl=0; for(int q=0;q<d;q++){ int xq=X[r][q]; deg+=xq; if(!xq) continue; if(cls[q]==0) nA+=xq; else if(cls[q]==1) nB+=xq; else if(cls[q]==2) nC+=xq; else nE+=xq; if(low[q]) nl+=xq; }
      long tau=ap[r]-(long)deg*m;
      if(deg==2&&nA==2){ if(tau<H) q2++; else q3++; }
      if(deg==3&&nA==3){ if(tau<H){ u3++; if(nl<=1) badstruct=1; } else u4++; }
      if(deg==4){ k++; if(nA!=4||tau>=H||nl<3) badq=1; if(nl==4) k0++; if(nl==3) k1++; }
      if(deg==2&&nA==1&&nB==1&&tau<m+H) s3++;
      if(deg==2&&nB==2&&tau<m+H) t3++;
      if(deg==2&&nl==2){ n0++; if(tau<hc) beta++; }
      if(deg==2&&nA==2&&nl==1&&tau<H){ if(X[r][xl]==1) lx++; else ly++; }
      if(deg==3&&nl==3){ c0++; if(tau<H) u0++; }
      if(deg==3&&nl==2&&nA==3&&tau<H) u1++; }
    long q=q2+q3, Q=(long)a*(a+1)/2, rA=Q-q, lsum=lx+ly, p=a-2;
    chk(0, (u3==u0+u1 && k==k0+k1 && q2==n0+lsum && !badstruct)?0:-1, m,W);
    chk(1, badq?-1:0, m,W);
    chk(2, (5*u0-4*k0<4*u1-3*k1? 5*u0-4*k0 : 4*u1-3*k1), m,W);
    long D3=(long)(a+2)*q-3*(u3+u4), LC=(long)(a+1)*(q2+u3)-4*k;
    /* arcs */
    long H0=H-L, ThH=H+H0; long J=0,JA=0,JH=0,JHA=0, qc=0;
    for(int r=1;r<m;r++){ int inY=((r>=H&&r<theta&&r<m)||(r>=1&&r<theta-m)); int inYH=((r>=H&&r<ThH&&r<m)||(r>=1&&r<ThH-m)); if(!inY&&!inYH) continue; if(isE[r]) continue; /* E units are allowed occupants */
      int deg=0,nA=0,nB=0,allA=1,nl=0; for(int q4=0;q4<d;q4++){ int xq=X[r][q4]; deg+=xq; if(!xq) continue; if(cls[q4]==0) nA+=xq; else { allA=0; if(cls[q4]==1) nB+=xq; } if(low[q4]) nl+=xq; }
      long tau=ap[r]-(long)deg*m; int allowed=0;
      if(deg==2&&nA==2&&tau>=H) allowed=1; if(deg==1&&!allA) allowed=1; if(deg==2&&nA==1&&nB==1&&tau>=m+H) allowed=1; if(deg==2&&nB==2&&tau>=m+H) allowed=1;
      if(allowed) continue;
      if(inY){ J++; if(allA) JA++; if(deg==2&&nl==2&&r>=1&&r<theta-m) qc++; }
      if(inYH){ JH++; if(allA) JHA++; } }
    long P=(a-1)+LC+2*q2+k-2*JA;
    chk(3, 6+(p+1)*n0+k0-u1+C2(lx+1)+C2(ly+1)-JA, m,W);
    chk(4, P-(a-13+(5-a)*n0+lx*(a+2-lx)+ly*(a+2-ly)), m,W);
    if(lsum>=2) chk(5, P-2, m,W);
    if(rA>0&&q>=2){ chk(6, D3-(2*a-2), m,W); chk(7, P+D3, m,W); }
    long delta=H-2*L; long R=0, exc=0; for(int i=0;i<d;i++) if(cls[i]==0&&!low[i]){ if(tof[i]<theta-2*L) R++; if(tof[i]<H0) exc++; }
    long PH=(a-1)+LC+2*q2+k+delta-2*JHA;
    if(rA==0&&lsum<=1){ nrA0++;
      long t0=4-c0; chk(8, (a+1)*u0-5*k0+3*t0-2*qc, m,W);
      chk(9, 2+qc+4+k0+3*R-u1+lsum-JA, m,W);
      chk(10, P+D3-(4*a-4+(a+1)*lsum-6*R), m,W);
      chk(11, lsum-exc, m,W);
      chk(12, 9+3*p+(2*p+3)*lsum+k-JHA, m,W);
      chk(13, PH-(delta-(2*a-2)-(3*a-5)*lsum), m,W);
      { long n=R-lsum; if(n<0) n=0; long w=(delta+1)/2; chk(14, (2*w-2)-n*(n-1), m,W); }
      chk(15, (P+D3>=0||PH>=0)?0:-1, m,W);
      chk(18, b*(2+lsum+q2)+(long)cc*(2+lsum)-(JH-JHA), m,W); }
    chk(16, b*(2+n0)+2L*cc-(J-JA), m,W);
    chk(17, b*(2+beta)+2L*cc-(J-JA), m,W);
    { long WA=0, FA=0; for(int r=0;r<m;r++){ if(r&&isE[r]) continue; int allA=1; for(int q4=0;q4<d;q4++) if(X[r][q4]&&cls[q4]!=0) allA=0; if(allA){ FA++; WA+=(long)(a+1)*((M-ap[r])/m); } } WA-=(M/m)*FA;
      if(WA<0){ nWAneg++; if(rA==0&&lsum<=1) nWAneg0++; }
      if(a==7&&n0==3&&q2==3&&lsum==0&&u3==0){ nB7++; if(beta==3) nB7b3++; if(WA<0) nB7neg++; } }
    long G=(long)cc*(cc+e+1)+(long)e*(3*a+2*b-1)+(long)(cc+e)*(q3+s3+t3);
    long A2=(long)(a-1)*(b+1)+G+LC+(long)b*u3+(long)(cc+e)*(2*q2+u3)+D3;
    long F1=A2+(b+2)*q2+k-2*J, F2=A2+(b+2)*q2+k-(-delta+2*JH);
    { long ls=2*J-(b+2)*q2-k; if(ls<0) ls=0; chk(19, W-(A2-ls), m,W); }
    { long ls=(-delta+2*JH)-(b+2)*q2-k; if(ls<0) ls=0; chk(20, W-(A2-ls), m,W); }
    chk(21, F1>F2?F1:F2, m,W);
    chk(22, F1-(P+D3+(long)b*(a-1+q2+u3-2*(2+n0))+G+(long)(cc+e)*(2*q2+u3)-4L*cc), m,W);
    if((rA>0||lsum>=2)&&a>=8) chk(23, F1, m,W);
  }
  printf("seed=%s GR=%d tested(two low A, a>=7, 3m<c<=4m)=%ld  (rA=0,l<=1: %ld) W_A<0: %ld (of which rA=0,l<=1: %ld)  B7: %ld (beta=3: %ld, W_A<0: %ld)\n",argv[1],GR,tested,nrA0,nWAneg,nWAneg0,nB7,nB7b3,nB7neg);
  for(int i=0;i<25;i++) printf("  %-36s applicable %8ld  fails %6ld  min slack %ld\n",nm[i],applic[i],fails[i],applic[i]?minsl[i]:0);
  return 0; }
