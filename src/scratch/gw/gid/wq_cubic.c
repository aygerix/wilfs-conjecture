/* Random stress test of Conjecture WQ (e >= 4): units + window (mu, min(2mu,m-1)] pay every deficit.
   Down-set = graded-lex normal forms (GR=1) or lex (GR=0) of Ap(S,m). c_x = lam*phi + B - gamma (G-ID).
   samplers: 0 band gens, 1 truncated at C (Eliahou-type), 2 uniform gens.  usage: wq_rand seed trials mmin mmax GR */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 260
#define DM 200
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[64], isg[MM], X[MM][DM]; static long mg[DM]; static int gi[MM];
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+3; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]);
  long tested[3]={0},fails[3]={0}; long dt[16]={0}, df[16]={0}; long dmin[16]; for(int i=0;i<16;i++) dmin[i]=1L<<40; long minq[3]={1L<<40,1L<<40,1L<<40}; long wneg=0; long bigdeg=0;
  for(long t=0;t<T;t++){
    int samp=rnd()%3; int m=mmin+rnd()%(mmax-mmin+1); int ng=2+rnd()%14; int g0=0; long C=-1;
    if(samp==0){ double lo=1.0+(rnd()%5000)/1000.0, wid=(rnd()%1000)/1000.0*lo*0.6; for(int k=0;k<ng;k++) gens[g0++]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1; }
    else if(samp==1){ int qq=3+rnd()%8; C=(long)qq*m-(long)(rnd()%m); int eta=2+rnd()%(qq-1); double lo=(double)C/eta, hi=(double)(C+m)/eta; if(rnd()%3==0) hi=lo+(hi-lo)*(0.3+(rnd()%700)/1000.0);
      for(int k=0;k<ng;k++){ long gv=(long)(lo+(hi-lo)*((rnd()%10000)/10000.0)); if(gv<=m) gv=m+1; gens[g0++]=(int)gv; } }
    else { int span=m*(1+rnd()%8); for(int k=0;k<ng;k++) gens[g0++]=m+1+rnd()%span; }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(b+gens[k])%m; long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    if(C>=0){ for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    int d=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } isg[r]=!dec; if(!dec){ if(d>=DM){ok=0;break;} gi[r]=d; mg[d++]=ap[r]; } }
    if(!ok||d<3) continue;
    /* normal forms: process residues by increasing ap value */
    int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
    for(int h=0;h<d;h++) X[0][h]=0;
    for(int ii=1;ii<m;ii++){ int r=ord[ii]; long w=ap[r]; int found=0, bdeg=1<<30; static int best[DM], cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int tr=(int)((w-mg[j])%m); if(ap[tr]==w-mg[j]){ int cd=0; for(int h=0;h<d;h++){ cand[h]=X[tr][h]+(h==j); cd+=cand[h]; }
          int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int h=0;h<d;h++) if(cand[h]!=best[h]){ better=cand[h]>best[h]; break; } } }
          if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found){ ok=0; break; } for(int h=0;h<d;h++) X[r][h]=best[h]; }
    if(!ok) continue;
    long mu=M%m; long hi=(2*mu<=m-1)?2*mu:m-1; long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
    long Qwin=0,Qdebt=0,tot=0; int maxdeg=0;
    for(int r=1;r<m;r++){ long lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; int deg=0;
      for(int a=0;a<d;a++){ deg+=X[r][a]; sr+=(long)X[r][a]*(mg[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+mg[a]%m)>=m);
        long nv=ap[r]+mg[a]; int tr=(int)(nv%m); int in=(ap[tr]==nv); if(in){ for(int h=0;h<d;h++) if(X[tr][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
      long cx=lam*phi+B-sr/m; tot+=cx; if(deg>maxdeg) maxdeg=deg;
      if(deg==1 || (r>mu && r<=hi)) Qwin+=cx; else if(cx<0) Qdebt+=-cx; }
    if(tot!=W){ printf("IDENTITY FAIL\n"); }
    if(W<0){ wneg++; printf("WILF FAIL?! m=%d\n",m); }
    if(maxdeg>=4) bigdeg++;
    { int md=maxdeg<15?maxdeg:15; dt[md]++; long qq=Qwin-Qdebt; if(qq<0) df[md]++; if(qq<dmin[md]) dmin[md]=qq; }
    tested[samp]++; long q=Qwin-Qdebt; if(q<minq[samp]) minq[samp]=q;
    if(q<0 && maxdeg==3){ printf("CUBIC FAIL m=%d d=%d mu=%ld M=%ld K=%ld W=%ld Qwin=%ld Qdebt=%ld gens:",m,d,mu,M,M/m,W,Qwin,Qdebt); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n");
      for(int r=1;r<m;r++){ long lam=(M-ap[r])/m, eps=(M-ap[r])%m; long phi=0,B=0,sr=0; for(int a=0;a<d;a++){ sr+=(long)X[r][a]*(mg[a]%m); if(X[r][a]) B+=(long)X[r][a]*((eps+mg[a]%m)>=m); long nv=ap[r]+mg[a]; int tr=(int)(nv%m); int in=(ap[tr]==nv); if(in){ for(int h=0;h<d;h++) if(X[tr][h]!=X[r][h]+(h==a)){in=0;break;} } if(!in) phi+=X[r][a]+1; }
        long cx=lam*phi+B-sr/m; if(cx<0 || (r>mu&&r<=hi) || 1){ printf("   r=%3d w=%4ld lam=%ld phi=%ld B=%ld gam=%ld c=%ld x=(",r,ap[r],lam,phi,B,sr/m,cx); for(int a=0;a<d;a++) printf("%d,",X[r][a]); printf(")%s\n", r<=mu?" CROWN":(r<=hi?" WIN":"")); } } }
    if(q<0){ fails[samp]++; if(fails[samp]<=0){ printf("WQ FAIL samp=%d m=%d d=%d mu=%ld M=%ld K=%ld W=%ld Qwin=%ld Qdebt=%ld maxdeg=%d gens:",samp,m,d,mu,M,M/m,W,Qwin,Qdebt,maxdeg); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); } }
  }
  for(int i=1;i<16;i++) if(dt[i]) printf("maxdeg=%d tested=%ld WQfail=%ld minQ=%ld\n",i,dt[i],df[i],dmin[i]);
  printf("seed=%s GR=%d tested band=%ld trunc=%ld unif=%ld | WQ fails %ld %ld %ld | minQ %ld %ld %ld | maxdeg>=4: %ld | Wilf fails %ld\n",argv[1],GR,tested[0],tested[1],tested[2],fails[0],fails[1],fails[2],minq[0],minq[1],minq[2],bigdeg,wneg);
  return 0; }
