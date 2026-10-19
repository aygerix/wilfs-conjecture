/* Lead's independent instance check of codex P5d (P5_REPORT sections 31-39), for every number alpha>=3 of low A
   directions.  Setting as lead_t23_check.c: 3m<c<=4m, M=c+m-1, h=c-3m, offsets t=n-m; A:[1,h) B:[h,h+m)
   C:[h+m,h+2m) E:[h+2m,h+3m) (E units flagged, outside the tile).  Low A: 2t<h, L = least low offset.
   Fixed arc theta=ceil(3h/2), Y=[h,min(theta,m)) u [1,theta-m); H0=h-L, Y_H=[h,min(h+H0,m)) u [1,h+H0-m).
   Allowed occupants: q3, B/C/E units, s4, t4.  J/J_A = intruders / pure-A intruders.
   Tile = grlex (GR=1) or lex (GR=0) normal forms.
   Samplers: 0 random lows/highs, 1 highs clustered in [h-L,theta-2L), 9 lows in [h/4,h/2) & highs in [h-L,h)
   (near-full faces, W_A<0), 10 like 9 with extra B directions (B-heavy).
   usage: lead_t5_check seed trials mmin mmax GR samp amin alphamin alphamax */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 6000
#define DM 72
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[DM+16], X[MM][DM]; static long mg[DM]; static int isE[MM], intr[MM], intrA[MM];
#define NCHK 50
static const char *nm[NCHK]={
 "struct u3=u0+u1,k=k0+k1,q2=n0+l",        /*0*/
 "A-ID / D3 identities",                    /*1*/
 "GEN-COUNT J_A (general alpha)",           /*2*/
 "GLOC F1>=Phi (general alpha)",            /*3*/
 "OUT-f J-J_A<=b(alpha+beta)+alpha c",      /*4*/
 "OUT-H J_H-J_HA<=b(alpha+E+l+beta_H)+c(alpha+E)", /*5*/
 "H-COLD beta_H<=min(n0,u0+t0)",            /*6*/
 "COLD (alpha+2)beta<=3(u0+t0)",            /*7*/
 "COLD-MAC u0+t0>=U-(Q-beta)^<2>",          /*8*/
 "LOC-LOW t0<=alpha r_LL+eps",              /*9*/
 "LOC-LOW c0<=n0^<2>",                      /*10*/
 "LLH 2u1<=(alpha+1)l",                     /*11*/
 "LLH u1<=n0(a-alpha)",                     /*12*/
 "sharp J_A (beta,R count)",                /*13*/
 "R-EXACT P+D3 lower bound",                /*14*/
 "COLD-FIX (under COLD-SIGN)",              /*15*/
 "J_HA<=C_H+k",                             /*16*/
 "H0 payment >= DELTA-UP form",             /*17*/
 "fixed payment >= P+D3+bB_f+Omega_f",      /*18*/
 "COLD-HIGH H3>=H_cold (beta>=1)",          /*19*/
 "B-NEIGH W-W_A-H3-X_SR>=b[u3+min(2r,2a-r)]", /*20*/
 "MIX Macaulay #ABcubics<=qg^<2>-(t-ar)",   /*21*/
 "MIX-GAP Dv+Dw+Dz>=Delta(qg)-2(a-1)r",     /*22*/
 "m_up cardinality",                        /*23*/
 "global SP m>=H(a+1-r)-lambda eps",        /*24*/
 "global PSP m>=...",                       /*25*/
 "JOINT-SP general",                        /*26*/
 "JOINT-COUNT general",                     /*27*/
 "JOINT PSP (interval)",                    /*28*/
 "END-ETA I-LOW",                           /*29*/
 "HOT-ALL W>=W_A+T+H3+X_SR (T>=0 dropped)", /*30*/
 "S >= S_min (star minimum)",               /*31*/
 "C/E nonneg q+q2+2>=2(alpha+E) [W_A<0]",   /*32*/
 "Wilf",                                    /*33*/
 "HARC fixed W>=F1",                        /*34*/
 "HARC H0 W>=F2",                           /*35*/
 "WINDOW-SP short",                         /*36*/
 "WINDOW-SP wide",                          /*37*/
 "WINDOW-COUNT short cubic",                /*38*/
 "WINDOW-COUNT wide cubic",                 /*39*/
 "PSID wide R(R-1)",                        /*40*/
 "PSID short",                              /*41*/
 "shadow k0<=min(u0^<3>,(alpha+3)u0/4)",    /*42*/
 "shadow 3k1<=(alpha+2)u1",                 /*43*/
 "B-NEIGH + C/E costs",                     /*44*/
 "MIX budget: W-W_A-H3-X_SR >= Dv+Dw+Dz",   /*45*/
 "completion: budget>=bu3+2br+3(mm-br)+CEfull", /*46*/
 "Gamma test: Dvwz<Gamma => complete",      /*47*/
 "MIX-PACK budget: bud >= Dvwz + b*u3",     /*48*/
 "MIX-PACK s/t: bud >= (ab-s3)+b*u3+D_w"};  /*49*/
static long fails[NCHK], applic[NCHK], minsl[NCHK];
static int curm; static long curW; static int g0;
static void chk(int i,long slack){ applic[i]++; if(slack<minsl[i]) minsl[i]=slack; if(slack<0){ fails[i]++; if(fails[i]<=3){ printf("FAIL %s slack=%ld m=%d W=%ld gens:",nm[i],slack,curm,curW); for(int k=0;k<g0;k++) printf(" %d",gens[k]); printf("\n"); } } }
static long C2(long x){ return x>=2? x*(x-1)/2 : 0; }
static long C3(long x){ return x>=3? x*(x-1)*(x-2)/6 : 0; }
static long lam2(long n){ if(n<=1) return 0; if(n==2) return 2; if(n==3) return 4; if(n==4) return 8; return (n%3==0)? 3*n : 3*(n-1); }
static long Hn(long n){ return n*(C2(n)+1); }
static long mac2(long q){ if(q<=0) return 0; long j=1; while((j+2)*(j+1)/2<=q) j++; long s=q-j*(j+1)/2; return (j+2)*(j+1)*j/6+s*(s+1)/2; }
static long C2s(long x){ return x>=2? x*(x-1)/2:0; }
static long mac3(long x){ if(x<=0) return 0; long k3=3; while((k3+1)*k3*(k3-1)/6<=x) k3++; long rem=x-k3*(k3-1)*(k3-2)/6; long r=(k3+1)*k3*(k3-1)*(k3-2)/24;
  if(rem>0){ long k2=2; while((k2+1)*k2/2<=rem) k2++; long rem2=rem-k2*(k2-1)/2; r+=(k2+1)*k2*(k2-1)/6+(rem2+1)*rem2/2; } return r; }
static long Delta(long d,long x){ return (d+2)*x-3*mac2(x); }
static long key[MM]; static int cmpk(const void*x,const void*y){ long u=key[*(const int*)x], v=key[*(const int*)y]; return u<v?-1:u>v; }
static int budget;
static int okset2(int *T,int nt,int m){ static unsigned char used[MM]; memset(used,0,m); used[0]=1;
  for(int i=0;i<nt;i++){ int r=T[i]%m; if(used[r]) return 0; used[r]=1; }
  for(int i=0;i<nt;i++) for(int j=i;j<nt;j++){ int r=(T[i]+T[j])%m; if(used[r]) return 0; used[r]=1; }
  int ex=0; for(int i=0;i<nt;i++) for(int j=i;j<nt;j++) for(int k=j;k<nt;k++){ int r=(T[i]+T[j]+T[k])%m; if(used[r]){ if(++ex>budget) return 0; } used[r]=1; }
  return 1; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+23; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]); int SAMP=atoi(argv[6]); int AMIN=atoi(argv[7]); int ALMIN=atoi(argv[8]), ALMAX=atoi(argv[9]);
  if(mmax>=MM) mmax=MM-1;
  for(int i=0;i<NCHK;i++) minsl[i]=1L<<40; long tested=0, nWAneg=0, byal[40]={0}, bya[64]={0};
  for(long tr=0;tr<T;tr++){
    int m=mmin+rnd()%(mmax-mmin+1); int h=8+rnd()%(m-8>0?m-8:1); if(h>=m) h=m-1;
    int samp=SAMP>=0?SAMP:(int)(rnd()%5); if(samp==2) samp=9; if(samp==3) samp=10; if(samp==4) samp=11;
    int al=ALMIN+rnd()%(ALMAX-ALMIN+1); int na=AMIN+rnd()%8; if(na<al+1) na=al+1+rnd()%4;
    int nb=rnd()%4, ncc=rnd()%3, ne=rnd()%3; if(samp==10) nb=2+rnd()%7; g0=0;
    static int TT[DM]; int nt=0;
    if(samp>=9){ int samp9=samp;
      h=m/5+rnd()%(3*m/10); if(h<40) continue; int lowhi=(h-1)/2; int Lm=h/4+rnd()%((lowhi-h/4+1)>0?(lowhi-h/4+1):1);
      if(rnd()%3==0) Lm=1+rnd()%lowhi;   /* sometimes small lows: cold pairs */
      budget=(rnd()%3==0)?0:(int)(rnd()%(4*na+20)); int tries=0; TT[nt++]=Lm;
      while(nt<al && tries<30000){ tries++; int t=Lm+1+rnd()%((lowhi-Lm)>0?(lowhi-Lm):1); if(t>lowhi) continue; TT[nt]=t; if(okset2(TT,nt+1,m)) nt++; }
      if(nt<al) continue; int nex=rnd()%3; tries=0;
      while(nt<na && tries<30000){ tries++; int t; if(nex>0&&rnd()%4==0){ int lo=(h+1)/2; t=lo+rnd()%((h-Lm-lo)>0?(h-Lm-lo):1); } else t=h-Lm+rnd()%Lm; if(t>=h||2*t<h) continue; TT[nt]=t; if(okset2(TT,nt+1,m)){ nt++; if(t<h-Lm) nex--; } }
      if(nt<AMIN) continue;
    } else {
      int lowhi=(h-1)/2; if(lowhi<al) continue;
      int L0=1<<30; for(int i=0;i<al;i++){ int t=1+rnd()%lowhi; TT[nt++]=t; if(t<L0) L0=t; }
      int lo=(h+1)/2, hi=h-1; if(hi<lo) continue;
      for(int k=al;k<na;k++){ int t; if(samp==1){ int H0=h-L0; int w=(3*h+1)/2-2*L0-H0; if(w<1) w=1; t=H0+rnd()%w; if(t>hi) t=hi; if(t<lo) t=lo; } else t=lo+rnd()%(hi-lo+1); TT[nt++]=t; }
    }
    if(SAMP==99){ char *gs=getenv("GENS"); m=mmin; h=1+(int)(tr%(m-1)); g0=0; nt=0; nb=ncc=ne=0; char *p=gs; while(*p){ gens[g0++]=(int)strtol(p,&p,10); while(*p==' '||*p==',') p++; } goto built; }
    for(int i=0;i<nt;i++) gens[g0++]=m+TT[i];
    if(samp==11){ nb=1+rnd()%6; int w=(m-h)/2; if(w<1) w=1; for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%w; }   /* low B: complete mixed face */
    else for(int k=0;k<nb;k++) gens[g0++]=m+h+rnd()%m;
    for(int k=0;k<ncc;k++) gens[g0++]=2*m+h+rnd()%m;
    for(int k=0;k<ne;k++) gens[g0++]=3*m+h+rnd()%m;
    built:;
    long Ct=3L*m+h;
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int bb=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(bb<0||ap[r]<ap[bb])) bb=r; if(bb<0) break; done[bb]=1; for(int k=0;k<g0;k++){ int r2=(bb+gens[k])%m; long v=ap[bb]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    for(int r=1;r<m;r++){ long f=Ct+((r-Ct%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; }
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    long c=M-m+1; if(!(c>3L*m && c<=4L*m)) continue;
    long H=c-3L*m;
    int d=0, ok=1, e=0; memset(mg,0,sizeof mg);
    for(int r=1;r<m;r++){ isE[r]=0; int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; }
        if(!dec){ if(ap[r]-m>=H+2*m){ e++; isE[r]=1; } else { if(d>=DM){ok=0;break;} mg[d++]=ap[r]; } } }
    if(!ok) continue;
    int cls[DM], low[DM], lowix[DM]; int a=0,b=0,cc=0,alpha=0; long tof[DM];
    for(int i=0;i<d;i++){ long tt=mg[i]-m; tof[i]=tt; low[i]=0; lowix[i]=-1; if(tt<H){cls[i]=0;a++; if(2*tt<H){ low[i]=1; lowix[i]=alpha++; }} else if(tt<H+m){cls[i]=1;b++;} else {cls[i]=2;cc++;} }
    if(a<AMIN||alpha<ALMIN||alpha>ALMAX) continue;
    long L=1L<<40; for(int i=0;i<d;i++) if(low[i]&&tof[i]<L) L=tof[i];
    static int ord[MM]; for(int r=0;r<m;r++){ ord[r]=r; key[r]=ap[r]*MM+r; } qsort(ord,m,sizeof(int),cmpk);
    for(int q=0;q<d;q++) X[0][q]=0;
    for(int ii=1;ii<m&&ok;ii++){ int r=ord[ii]; long w=ap[r]; if(isE[r]){ for(int q=0;q<d;q++) X[r][q]=0; continue; } int found=0,bdeg=1<<30; static int best[DM],cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int t2=(int)((w-mg[j])%m); if(ap[t2]==w-mg[j]&&!isE[t2]){ int cd=0; for(int q=0;q<d;q++){ cand[q]=X[t2][q]+(q==j); cd+=cand[q]; }
        int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int q=0;q<d;q++) if(cand[q]!=best[q]){ better=cand[q]>best[q]; break; } } }
        if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found) ok=0; else for(int q=0;q<d;q++) X[r][q]=best[q]; }
    if(!ok) continue;
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)(d+e)*l-g;
    curm=m; curW=W; tested++; chk(33,W); if(alpha<40) byal[alpha]++; if(a<64) bya[a]++;
    long p=a-alpha, hc=(H+1)/2, theta=(3*H+1)/2, H0=H-L, delta=H-2*L;
    long nABB=0; long q2=0,q3=0,u3=0,u4=0,k=0,s3=0,t3=0,n0=0,u0=0,u1=0,k0=0,k1=0,beta=0,betaH=0,c0=0,H3=0,ncubAB=0,v2=0; static long lp[DM]; memset(lp,0,sizeof lp); int badstruct=0;
    long sigma = 2*H-m>0? 2*H-m : 0; long XSR=0;
    for(int r=1;r<m;r++){ intr[r]=0; intrA[r]=0; if(isE[r]) continue; int deg=0,nA=0,nB=0,nC=0,nl=0,lowf=-1; for(int q=0;q<d;q++){ int xq=X[r][q]; deg+=xq; if(!xq) continue; if(cls[q]==0) nA+=xq; else if(cls[q]==1) nB+=xq; else nC+=xq; if(low[q]){ nl+=xq; lowf=lowix[q]; } }
      long tau=ap[r]-(long)deg*m;
      if(deg==2&&nA==2){ if(tau<H) q2++; else q3++; }
      if(deg==3&&nA==3){ if(tau<H){ u3++; if(nl<=1) badstruct=1; } else u4++; if(tau>=2*H) H3++; }
      if(deg==4){ k++; if(nA!=4||tau>=H||nl<3) badstruct=1; if(nl==4) k0++; if(nl==3) k1++; }
      if(deg==2&&nA==1&&nB==1&&tau<m+H) s3++;
      if(deg==2&&nB==2&&tau<m+H) t3++;
      if(deg==3&&nA==1&&nB==2) nABB++;
      if(deg==3&&nA+nB==3){ ncubAB++; if(nA==2&&nB==1){ /* AAB: AA divisor tau */ long tA=0; for(int q=0;q<d;q++) if(cls[q]==0) tA+=X[r][q]*tof[q]; if(tA<H) v2++; } }
      if(deg==2&&nl==2){ n0++; if(tau<hc) beta++; if(tau<H0) betaH++; }
      if(deg==2&&nA==2&&nl==1&&tau<H) lp[lowf]++;
      if(deg==3&&nl==3){ c0++; if(tau<H) u0++; }
      if(deg==3&&nl==2&&nA==3&&tau<H) u1++;
      if(nA==deg && deg<=4 && tau<H && tau>=sigma && (deg<=1 || (deg==2&&tau<H) || (deg==3&&tau<H) || deg==4)) XSR++;
      int allA=(nA==deg); int allowed=0;
      if(deg==2&&nA==2&&tau>=H) allowed=1; if(deg==1&&!allA) allowed=1; if(deg==2&&nA==1&&nB==1&&tau>=m+H) allowed=1; if(deg==2&&nB==2&&tau>=m+H) allowed=1;
      if(!allowed){ intr[r]=1; intrA[r]=allA; } }
    if(sigma==0) XSR++;  /* the zero cell, tau=0 >= sigma */
    long lsum=0, CS=0, S=0; for(int i=0;i<alpha;i++){ lsum+=lp[i]; CS+=C2(lp[i]+1); S+=lp[i]*(a+2-lp[i]); }
    long q=q2+q3, Q=(long)a*(a+1)/2, r=Q-q, U=(long)a*(a+1)*(a+2)/6, uu=u3+u4, tA=U-uu, F=C3(a+1);
    long Qal=(long)alpha*(alpha+1)/2, Ual=(long)alpha*(alpha+1)*(alpha+2)/6, t0=Ual-c0, rLL=Qal-n0, epsM=mac2(q)-uu;
    long E=lsum+r<p? lsum+r : p;
    chk(0,(u3==u0+u1&&k==k0+k1&&q2==n0+lsum&&!badstruct)?0:-1);
    long D3=(long)(a+2)*q-3*uu, LC=(long)(a+1)*(q2+u3)-4*k;
    long WA=0; { long FA=0; for(int x=0;x<m;x++){ if(x&&isE[x]) continue; int allA=1; for(int q4=0;q4<d;q4++) if(X[x][q4]&&cls[q4]!=0) allA=0; if(allA){ FA++; WA+=(long)(a+1)*((M-ap[x])/m); } } WA-=(M/m)*FA; }
    chk(1,(D3==3*tA-(long)(a+2)*r && WA==-F+LC-(long)(a-3)*r+4*tA)?0:-1);
    if(WA<0) nWAneg++;
    long J=0,JA=0,JH=0,JHA=0;
    for(int x=1;x<m;x++){ if(!intr[x]) continue; int inY=((x>=H&&x<theta&&x<m)||(x>=1&&x<theta-m)); int inYH=((x>=H&&x<H+H0&&x<m)||(x>=1&&x<H+H0-m));
      if(inY){ J++; if(intrA[x]) JA++; } if(inYH){ JH++; if(intrA[x]) JHA++; } }
    long R=0; for(int i=0;i<d;i++) if(cls[i]==0&&!low[i]&&tof[i]<theta-2*L) R++;
    long P=(a-1)+LC+2*q2+k-2*JA;
    long G=(long)cc*(cc+e+1)+(long)e*(3*a+2*b-1)+(long)(cc+e)*(q3+s3+t3);
    long A2=(long)(a-1)*(b+1)+G+LC+(long)b*u3+(long)(cc+e)*(2*q2+u3)+D3;
    long F1=A2+(b+2)*q2+k-2*J, F2=A2+(b+2)*q2+k-(-delta+2*JH);
    chk(2, alpha+n0+c0+k0+p*n0-u1+CS-JA);
    { long Phi=D3+(a-1)-2*alpha-2*c0+(2*alpha+1-a)*n0+S+(a+1)*u0-5*k0+(a+3)*u1-3*k1+(long)b*(a-1+q2+u3-2*alpha-2*n0)+G+(long)(cc+e)*(2*q2+u3)-2L*alpha*cc; chk(3,F1-Phi); }
    chk(4,(long)b*(alpha+beta)+(long)alpha*cc-(J-JA));
    chk(5,(long)b*(alpha+E+lsum+betaH)+(long)cc*(alpha+E)-(JH-JHA));
    { long mn=n0<u0+t0?n0:u0+t0; chk(6,mn-betaH); }
    chk(7,3*(u0+t0)-(alpha+2)*beta);
    chk(8,u0+t0-(Ual-mac2(Qal-beta)));
    chk(9,alpha*rLL+epsM-t0);
    chk(10,mac2(n0)-c0);
    chk(11,(alpha+1)*lsum-2*u1);
    chk(12,n0*p-u1);
    chk(13,alpha+beta+c0+k0+n0*R-u1+CS-JA);
    long Rex=D3+a-1-2*alpha-2*beta-2*c0+(a+3)*n0+S-2*n0*R+(a+1)*u0-5*k0+(a+3)*u1-3*k1;
    chk(14,P+D3-Rex);
    if(alpha>=3 && a+1>=alpha && (alpha+2)*(4L*a-5*alpha-11)>=24) chk(15,P+D3-(D3+a-1-2*alpha-2*Ual+(a+3)*n0+S-2*n0*R));
    long CH=alpha+n0+c0+lsum+E+C3(E+2)+(n0+alpha*E)*p;
    chk(16,CH+k-JHA);
    { long BH=a-1+q2+u3-2*(alpha+E+lsum+betaH); long OmH=G+(long)(cc+e)*(2*q2+u3)-2L*(alpha+E)*cc;
      chk(17,F2-(delta+a-1+(a+3)*q2+D3+(a+1)*u3-5*k-2*CH+(long)b*BH+OmH)); }
    { long Bf=a-1+q2+u3-2*alpha-2*beta; long Omf=G+(long)(cc+e)*(2*q2+u3)-2L*alpha*cc; chk(18,F1-(P+D3+(long)b*Bf+Omf)); }
    if(beta>=1){ long Hc=0; long v1=C3(p-E+2)-tA+t0; if(v1>Hc) Hc=v1; long mn=1L<<50;
      for(long j=0;j<=E;j++){ long nj=p-j; long rj=r-rLL-(j-lsum>0?j-lsum:0); if(rj<0) rj=0; long v=C3(nj+2)-nj*rj-epsM; if(v<mn) mn=v; }
      if(mn>Hc) Hc=mn; chk(19,H3-Hc); }
    { long br=u3+(2*r<2*a-r?2*r:2*a-r); if(br>=0) chk(20,(W-WA-H3-XSR)-(long)b*br); }
    long d0=a+b, qg=q+s3+t3;
    chk(21,mac2(qg)-(tA-(long)a*r)-ncubAB);
    { long Dvwz=(d0+2)*qg-3*ncubAB+((long)b*q2-v2)-D3; chk(22,Dvwz-(Delta(d0,qg)-2L*(a-1)*r)); }
    { long mup=C3(a+b+3)-r*(1+b)-tA+k+(long)cc*(a+b+1)+e; chk(23,mup-m); }
    { long ng=a+1-r; if(ng<0) ng=0; chk(24,2L*m-(2*Hn(ng)-lam2(ng)*epsM)); }
    { long er=C2(r+1); long low=Hn(a+1)-4*er-9*((long)(a+1)*er+(r+1)*epsM+C2(epsM)); chk(25,m-low); }
    long sj=(3*delta+1)/2;
    { long nj=alpha+R-r; if(nj<0) nj=0; chk(26,2*(3*sj-2)-(2*Hn(nj)-lam2(nj)*epsM)); }
    chk(27,(3*sj-2)-(C3(alpha+R+2)-tA));
    { long n=alpha+R; long er=C2(r+1); long low=Hn(n)-4*er-9*(n*er+(r+1)*epsM+C2(epsM)); chk(28,(3*sj-2)-low); }
    if(H>=2){ long JHh=0; long hc2=(H+1)/2;
      for(int x=1;x<m;x++) if(intr[x]){ int in=((x>=H&&x<H+hc2&&x<m)||(x>=1&&x<H+hc2-m)); if(in) JHh++; }
      for(long Hh=hc2;Hh<H-1;Hh++){ int res=(int)((H+Hh)%m); if(res!=0&&intr[res]) JHh++; }
      long eend=2-H+2*JHh; if(3*delta<eend) eend=3*delta; long ls=eend-(b+2)*q2-k; if(ls<0) ls=0; chk(29,W-(A2-ls)); }
    chk(30,W-(WA+H3+XSR));
    { long Smin=0; if(p>0){ long kk=lsum/p, z=lsum%p; Smin=kk*p*(a+2-p)+z*(a+2-z); } chk(31,S-Smin); }
    if(SAMP==99 && q+q2+2-2*(alpha+E)<0) printf("h0=%d m=%d a=%d alpha=%d b=%d c=%d e=%d h=%ld q=%ld q2=%ld r=%ld l=%ld E=%ld WA=%ld W=%ld eps=%ld\n",h,m,a,alpha,b,cc,e,H,q,q2,r,lsum,E,WA,W,epsM);
    if(WA<0) chk(32,q+q2+2-2*(alpha+E));   /* claimed only where W_A<0 (certificate base states) */
    chk(34,W-F1); chk(35,W-F2);
    { long w=(delta+1)/2; long ns=R-lsum-2*r; if(ns<0) ns=0; long nw=R-r; if(nw<0) nw=0; long nc=R-lsum-r; if(nc<0) nc=0;
      chk(36,2*(3*w-2)-(2*Hn(ns)-lam2(ns)*epsM)); chk(37,2*(3*delta-2)-(2*Hn(nw)-lam2(nw)*epsM));
      chk(38,(3*w-2)-(C3(nc+2)-tA)); chk(39,(3*delta-2)-(C3(R+2)-tA));
      chk(40,2*delta-2+2*r*(r+1)-R*(R-1)); chk(41,2*w-2+2*r*(r+1)-nc*(nc-1)); }
    { long K0=mac3(u0); long K0b=(alpha+3)*u0/4; if(K0b<K0) K0=K0b; chk(42,K0-k0); chk(43,(alpha+2)*u1-3*k1); }
    { long d0x=a+b, qgx=q+s3+t3; long Dvwz=(d0x+2)*qgx-3*ncubAB+((long)b*q2-v2)-D3; long bud=W-WA-H3-XSR; chk(45,bud-Dvwz);
      long BBn=(long)b*(b+1)/2; int complete=(s3==(long)a*b && t3==BBn);
      chk(48,bud-Dvwz-(long)b*u3);
      { long Dw=(long)a*t3+(long)(b+1)*s3-3*nABB; chk(49,bud-((long)a*b-s3)-(long)b*u3-Dw); }
      /* Gamma(d0,q,r) */ long hi=(d0x+1)*d0x/2-r-1, gam=1L<<50; for(long x=q;x<=hi;x++){ long v=(d0x+2)*x-3*mac2(x); if(v<gam) gam=v; } if(gam<(1L<<50)) gam-=2L*(a-1)*r;
      if(Dvwz<gam) chk(47,complete?0:-1);
      if(complete && b>=1){ long formal=(long)Q*b+(long)a*BBn+C3(b+2); long presmix=ncubAB-uu; long mm=formal-presmix; long co=q+q2+u3+(long)a*b+BBn;
        long CEf=(long)cc*(cc+1+co)+(long)e*(3*a+2*b+cc+co); chk(46,bud-(long)b*u3-2L*b*r-3*(mm-(long)b*r)-CEf); } }
    { long br=u3+(2*r<2*a-r?2*r:2*a-r); if(br<0) br=0; chk(44,(W-WA-H3-XSR)-(long)b*br-(long)cc*(cc+1+q+q2+u3)-(long)e*(3*a+2*b+cc+q+q2+u3)); }
  }
  printf("seed=%s GR=%d samp=%d a>=%d alpha in [%d,%d]: tested=%ld  W_A<0: %ld\n  by alpha:",argv[1],GR,SAMP,AMIN,ALMIN,ALMAX,tested,nWAneg);
  for(int i=0;i<40;i++) if(byal[i]) printf(" %d:%ld",i,byal[i]); printf("\n  by a:"); for(int i=0;i<64;i++) if(bya[i]) printf(" %d:%ld",i,bya[i]); printf("\n");
  for(int i=0;i<NCHK;i++) printf("  %-48s applicable %8ld  fails %6ld  min slack %ld\n",nm[i],applic[i],fails[i],applic[i]?minsl[i]:0);
  return 0; }
