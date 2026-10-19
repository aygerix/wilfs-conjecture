/* Stress test of Conjecture CP (PROOFS "Conjecture CP"): column-reflection localization
   Delta(x) = sum_b lam(R_b x) - kappa(x), sum_x Delta = W.  CP <=> every order ideal Z of D has sum_Z Delta >= 0
   <=> deficits are paid from cells below (flow y -> x for y < x).  Also the no-sharing form NS:
   def(y) <= sum_b Delta^+(y - e_b).
   Down-set = lex (GR=0) or graded-lex (GR=1) normal forms of Ap(S,m).
   samplers: 0 band gens, 1 truncated at C (Eliahou-type), 2 uniform gens, 3 near-arithmetic n, n+s, ..., n+(d-1)s.
   usage: cp_rand seed trials mmin mmax GR [sampler(-1=all)] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MM 400
#define DM 64
#define NN (MM+2)
static int cap[NN][NN], fl[NN][NN];
static int maxflow(int n,int s,int t){ int tot=0; static int prev[NN], q[NN]; for(int i=0;i<n;i++) for(int j=0;j<n;j++) fl[i][j]=0;
  while(1){ for(int i=0;i<n;i++) prev[i]=-1; prev[s]=s; int h=0,tl=0; q[tl++]=s;
    while(h<tl&&prev[t]<0){ int u=q[h++]; for(int v=0;v<n;v++) if(prev[v]<0&&cap[u][v]-fl[u][v]>0){ prev[v]=u; q[tl++]=v; } }
    if(prev[t]<0) break; int aug=1<<30; for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; int r=cap[u][v]-fl[u][v]; if(r<aug) aug=r; }
    for(int v=t;v!=s;v=prev[v]){ int u=prev[v]; fl[u][v]+=aug; fl[v][u]-=aug; } tot+=aug; }
  return tot; }
static unsigned long long st; static unsigned long long rnd(void){ st^=st<<13; st^=st>>7; st^=st<<17; return st; }
static long ap[MM]; static int done[MM], gens[64], X[MM][DM]; static long mg[DM]; static long Dl[MM];
static int m,d; static long MAJ_t,MAJ_f,RECT_t,RECT_f,STAIR_f; static long FS_t[2],FS_f[2]; static long REG_t[6],REG_f[6],REG_td[6]; static int BIND; static long BIND_n,BIND_principal,BIND_min=1L<<40,BIND_h[16],PR_h[16],PR_neg; static long ST_def[8],ST_corner,ST_noncorner,ST_top,ST_nontop,ST_sup[16],ST_bestlow_insuff;
/* is the vector X[r]+e_a in D?  returns residue or -1 */
static int up(int r,int a){ long nv=ap[r]+mg[a]; int tr=(int)(nv%m); if(ap[tr]!=nv) return -1;
  for(int h=0;h<d;h++) if(X[tr][h]!=X[r][h]+(h==a)) return -1; return tr; }
int main(int argc,char**argv){
  st=strtoull(argv[1],0,10)*2654435761ULL+3; long T=atol(argv[2]); int mmin=atoi(argv[3]),mmax=atoi(argv[4]); int GR=atoi(argv[5]);
  int SAMP=argc>6?atoi(argv[6]):-1; BIND=getenv("BIND")!=0;
  long tested[10]={0}, cpf[10]={0}, nsf[10]={0}, wneg=0; long hist[32]={0}, histf[32]={0};
  for(long t=0;t<T;t++){
    int samp=SAMP>=0?SAMP:(int)(rnd()%4); m=mmin+rnd()%(mmax-mmin+1); int ng=2+rnd()%14; int g0=0; long C=-1;
    if(samp==0){ double lo=1.0+(rnd()%5000)/1000.0, wid=(rnd()%1000)/1000.0*lo*0.6; for(int k=0;k<ng;k++) gens[g0++]=(int)(m*(lo+wid*((rnd()%10000)/10000.0)))+1; }
    else if(samp==1){ int qq=3+rnd()%8; C=(long)qq*m-(long)(rnd()%m); int eta=2+rnd()%(qq-1); double lo=(double)C/eta, hi=(double)(C+m)/eta; if(rnd()%3==0) hi=lo+(hi-lo)*(0.3+(rnd()%700)/1000.0);
      for(int k=0;k<ng;k++){ long gv=(long)(lo+(hi-lo)*((rnd()%10000)/10000.0)); if(gv<=m) gv=m+1; gens[g0++]=(int)gv; } }
    else if(samp==2){ int span=m*(1+rnd()%8); for(int k=0;k<ng;k++) gens[g0++]=m+1+rnd()%span; }
    else if(samp==9){ char*e=getenv("GENS"); char*q=e; m=(int)strtol(q,&q,10); while(*q){ gens[g0++]=(int)strtol(q,&q,10); } T=1; }
    else { int dd=2+rnd()%5; long n0=m+1+rnd()%(m*(1+rnd()%6)); int s=1+(rnd()%3==0?rnd()%4:0); for(int k=0;k<dd;k++) gens[g0++]=(int)(n0+(long)k*s); }
    for(int r=0;r<m;r++){ ap[r]=-1; done[r]=0; } ap[0]=0;
    for(int it=0;it<m;it++){ int b=-1; for(int r=0;r<m;r++) if(!done[r]&&ap[r]>=0&&(b<0||ap[r]<ap[b])) b=r; if(b<0) break; done[b]=1; for(int k=0;k<g0;k++){ int r2=(int)((b+gens[k])%m); long v=ap[b]+gens[k]; if(ap[r2]<0||v<ap[r2]) ap[r2]=v; } }
    if(C>=0){ for(int r=1;r<m;r++){ long f=C+((r-C%m)%m+m)%m; if(ap[r]<0||f<ap[r]) ap[r]=f; } }
    int ok=1; for(int r=0;r<m;r++) if(ap[r]<0) ok=0; if(!ok) continue;
    long M=0; for(int r=0;r<m;r++) if(ap[r]>M) M=ap[r];
    d=0; for(int r=1;r<m;r++){ int dec=0; for(int s=1;s<m&&!dec;s++){ int r2=(r-s+m)%m; if(r2==0) continue; if(ap[s]+ap[r2]==ap[r]) dec=1; } if(!dec){ if(d>=DM){ok=0;break;} mg[d++]=ap[r]; } }
    if(!ok||d<2) continue;
    int ord[MM]; for(int r=0;r<m;r++) ord[r]=r; for(int i=1;i<m;i++){ int x=ord[i],j=i-1; while(j>=0&&ap[ord[j]]>ap[x]){ ord[j+1]=ord[j]; j--; } ord[j+1]=x; }
    for(int h=0;h<d;h++) X[0][h]=0;
    for(int ii=1;ii<m;ii++){ int r=ord[ii]; long w=ap[r]; int found=0, bdeg=1<<30; static int best[DM], cand[DM];
      for(int j=0;j<d;j++) if(w>=mg[j]){ int tr=(int)((w-mg[j])%m); if(ap[tr]==w-mg[j]){ int cd=0; for(int h=0;h<d;h++){ cand[h]=X[tr][h]+(h==j); cd+=cand[h]; }
          int better=!found; if(found){ if(GR&&cd<bdeg) better=1; else if(!GR||cd==bdeg){ for(int h=0;h<d;h++) if(cand[h]!=best[h]){ better=cand[h]>best[h]; break; } } }
          if(better){ memcpy(best,cand,sizeof(int)*d); bdeg=cd; found=1; } } }
      if(!found){ ok=0; break; } for(int h=0;h<d;h++) X[r][h]=best[h]; }
    if(!ok) continue;
    /* check down-set property (normal forms of a term order are a down-set; verify) */
    for(int r=1;r<m&&ok;r++) for(int a=0;a<d&&ok;a++) if(X[r][a]>0){ long pv=ap[r]-mg[a]; int pr=(int)(pv%m); if(pv<0||ap[pr]!=pv) ok=0; else for(int h=0;h<d;h++) if(X[pr][h]!=X[r][h]-(h==a)){ ok=0; break; } }
    if(!ok){ printf("NOT DOWNSET\n"); continue; }
    long g=0,l=0; for(int r=0;r<m;r++){ g+=ap[r]/m; l+=(M-ap[r])/m; } long W=(long)d*l-g;
    { static long kk[MM], ll[MM]; for(int r=0;r<m;r++){ kk[r]=ap[r]/m; ll[r]=(M-ap[r])/m; }
      for(int i=1;i<m;i++){ long x=kk[i]; int j=i-1; while(j>=0&&kk[j]<x){ kk[j+1]=kk[j]; j--; } kk[j+1]=x; }
      for(int i=1;i<m;i++){ long x=ll[i]; int j=i-1; while(j>=0&&ll[j]<x){ ll[j+1]=ll[j]; j--; } ll[j+1]=x; }
      long a=0,b=0; int bad=0; for(int k=0;k<m;k++){ a+=kk[k]; b+=ll[k]; if((long)d*b-a<0) bad=1; }
      { static long aa[4000], bb[4000]; long K=M/m; for(long j=0;j<=K+1;j++){ aa[j]=0; bb[j]=0; }
        for(int r=0;r<m;r++){ long k1=ap[r]/m, l1=(M-ap[r])/m; for(long j=1;j<=k1;j++) aa[j]++; for(long j=1;j<=l1;j++) bb[j]++; }
        int rb=0; for(int k=1;k<=m&&!rb;k++){ long A=0,B=0; for(long i=1;i<=K;i++){ A+=aa[i]<k?aa[i]:k; B+=bb[i]<k?bb[i]:k; if(A>(long)d*B){ rb=1; break; } } }
        { static long best[MM+2], nb[MM+2]; for(int z=0;z<=m;z++) best[z]=0; long mx=0;
          for(long j=1;j<=K;j++){ long run=-(1L<<40); for(int z=m;z>=0;z--){ if(best[z]>run) run=best[z]; long val=(aa[j]<z?aa[j]:z)-(long)d*(bb[j]<z?bb[j]:z); nb[z]=(j==1?val:run+val); }
            for(int z=0;z<=m;z++){ best[z]=nb[z]; if(best[z]>mx) mx=best[z]; } }
          if(mx>0){ STAIR_f++; if(STAIR_f<=5){ printf("STAIR FAIL m=%d d=%d W=%ld gens:",m,d,W); for(int a2=0;a2<d;a2++) printf(" %ld",mg[a2]); printf("\n"); } } }
        RECT_t++; if(rb){ RECT_f++; if(RECT_f<=5){ printf("RECT FAIL m=%d d=%d W=%ld gens:",m,d,W); for(int a2=0;a2<d;a2++) printf(" %ld",mg[a2]); printf("\n"); } } }
      MAJ_t++; if(bad){ MAJ_f++; if(MAJ_f<=5){ printf("MAJ FAIL m=%d d=%d W=%ld gens:",m,d,W); for(int a2=0;a2<d;a2++) printf(" %ld",mg[a2]); printf("\n"); } } }
    long tot=0; int maxdeg=0;
    for(int r=0;r<m;r++){ long De=-(ap[r]/m); int deg=0;
      for(int b=0;b<d;b++){ deg+=X[r][b]; /* climb the b-column from r */ int J=X[r][b]; int cur=r; while(1){ int nx=up(cur,b); if(nx<0) break; cur=nx; J++; }
        long vR=ap[r]+(long)(J-2*X[r][b])*mg[b]; De+=(M-vR)/m; }
      Dl[r]=De; tot+=De; if(deg>maxdeg) maxdeg=deg; }
    if(tot!=W){ printf("IDENTITY FAIL m=%d tot=%ld W=%ld\n",m,tot,W); continue; }
    if(W<0){ wneg++; printf("WILF FAIL?! m=%d\n",m); }
    int md=maxdeg<31?maxdeg:31; hist[md]++; tested[samp]++;
    long dem=0; for(int r=0;r<m;r++) if(Dl[r]<0) dem+=-Dl[r];
    /* canonical corner regions: rule 0 climb smallest index, 1 climb largest index, 2 climb direction maximizing n, 3 minimizing n,
       4 corner above x with max value, 5 corner above x with min value */
    { static long reg[MM]; static int cor[MM];
      for(int rule=0;rule<6;rule++){ for(int r=0;r<m;r++) reg[r]=0;
        for(int r=0;r<m;r++){ int cur=r;
          if(rule<4){ while(1){ int nb=-1, nx=-1; for(int a=0;a<d;a++){ int u=up(cur,a); if(u<0) continue; if(nb<0 || (rule==1) || (rule==2&&mg[a]>mg[nb]) || (rule==3&&mg[a]<mg[nb])){ if(rule==0&&nb>=0) continue; nb=a; nx=u; } } if(nb<0) break; cur=nx; } }
          else { int best=-1; for(int y=0;y<m;y++){ int corner=1; for(int b=0;b<d;b++) if(up(y,b)>=0){corner=0;break;} if(!corner) continue; int ge=1; for(int h=0;h<d;h++) if(X[y][h]<X[r][h]){ge=0;break;} if(!ge) continue; if(best<0||(rule==4&&ap[y]>ap[best])||(rule==5&&ap[y]<ap[best])) best=y; } cur=best; }
          cor[r]=cur; reg[cur]+=Dl[r]; }
        int bad=0; long mn=1L<<40; for(int r=0;r<m;r++){ if(reg[r]<mn && cor[r]==r) mn=reg[r]; if(reg[r]<0) bad=1; }
        REG_t[rule]++; if(bad) REG_f[rule]++; if(dem>0) REG_td[rule]++; } }
    /* fractional split: surplus of x shared equally among (0) deficient cells above x, (1) all corners above x; check each deficient cell covered */
    if(dem>0){ static int above[MM]; for(int mode=0;mode<2;mode++){ static double got[MM]; for(int r=0;r<m;r++) got[r]=0;
        for(int x=0;x<m;x++) if(Dl[x]>0){ int na=0; for(int y=0;y<m;y++){ above[y]=0; if(y==x) continue; int ge=1; for(int h=0;h<d;h++) if(X[y][h]<X[x][h]){ge=0;break;} if(!ge) continue;
              if(mode==0 && Dl[y]<0) above[y]=1; if(mode==1){ int corner=1; for(int b=0;b<d;b++) if(up(y,b)>=0){corner=0;break;} if(corner) above[y]=1; } na+=above[y]; }
          if(na) for(int y=0;y<m;y++) if(above[y]) got[y]+=(double)Dl[x]/na; }
        int bad=0; for(int y=0;y<m;y++) if(Dl[y]<0 && got[y]+1e-9< -Dl[y]) bad=1; FS_t[mode]++; if(bad) FS_f[mode]++; } }
    for(int r=0;r<m;r++) if(Dl[r]<0){ int corner=1; for(int b=0;b<d;b++) if(up(r,b)>=0) corner=0; long lam=(M-ap[r])/m; int sup=0; for(int b=0;b<d;b++) if(X[r][b]) sup++;
      int def=(int)(-Dl[r]); if(def>7) def=7; ST_def[def]++; if(corner) ST_corner++; else ST_noncorner++; if(lam==0) ST_top++; else ST_nontop++; if(sup<16) ST_sup[sup]++;
      /* min surplus among lower covers, number of deficient upper covers of each lower cover */
      long best=-1000; for(int a=0;a<d;a++) if(X[r][a]>0){ long pv=ap[r]-mg[a]; int pr=(int)(pv%m); if(Dl[pr]>best) best=Dl[pr]; }
      if(best< -Dl[r]) ST_bestlow_insuff++; }
    if(SAMP==9){ printf("m=%d d=%d M=%ld K=%ld W=%ld maxdeg=%d dem=%ld ndef=",m,d,M,M/m,W,maxdeg,dem); int nd=0; long mx=0; for(int r=0;r<m;r++) if(Dl[r]<0){nd++; if(-Dl[r]>mx) mx=-Dl[r];} printf("%d maxdef=%ld\n",nd,mx); }
    if(dem>0){
      /* no-sharing: def(y) <= sum_b Delta^+(y-e_b) */
      int nsbad=0; for(int r=0;r<m;r++) if(Dl[r]<0){ long s=0; for(int a=0;a<d;a++) if(X[r][a]>0){ long pv=ap[r]-mg[a]; int pr=(int)(pv%m); if(Dl[pr]>0) s+=Dl[pr]; } if(s< -Dl[r]) nsbad=1; }
      if(nsbad) nsf[samp]++;
      int n=m+2,S0=m,T0=m+1; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
      for(int r=0;r<m;r++){ if(Dl[r]>0) cap[S0][r]=(int)Dl[r]; if(Dl[r]<0) cap[r][T0]=(int)(-Dl[r]); }
      for(int x=0;x<m;x++) if(Dl[x]<0) for(int y=0;y<m;y++) if(y!=x&&Dl[y]>0){ int le=1; for(int h=0;h<d;h++) if(X[y][h]>X[x][h]){le=0;break;} if(le) cap[y][x]=1<<20; }
      int f=maxflow(n,S0,T0);
      if(f>=dem && BIND){ for(int y=0;y<m;y++) if(Dl[y]<0){ long BIGW=1<<18; long dem2=0; for(int i=0;i<n;i++) for(int j=0;j<n;j++) cap[i][j]=0;
          for(int r=0;r<m;r++){ long w=Dl[r]-(r==y?BIGW:0); if(w>0) cap[S0][r]=(int)w; if(w<0){ cap[r][T0]=(int)(-w); dem2+=-w; } }
          for(int x=0;x<m;x++) if(Dl[x]<0||x==y) for(int z=0;z<m;z++) if(z!=x&&Dl[z]>0){ int le=1; for(int h=0;h<d;h++) if(X[z][h]>X[x][h]){le=0;break;} if(le) cap[z][x]=1<<20; }
          long f2=maxflow(n,S0,T0); long mn=f2-dem2+BIGW; /* min over Z containing y */
          long pr=0; for(int z=0;z<m;z++){ int le=1; for(int h=0;h<d;h++) if(X[z][h]>X[y][h]){le=0;break;} if(le) pr+=Dl[z]; }
          BIND_n++; if(mn==pr) BIND_principal++; if(mn<BIND_min) BIND_min=mn; if(mn<16&&mn>=0) BIND_h[mn]++; if(pr<16&&pr>=0) PR_h[pr]++; if(pr<0) PR_neg++; } }
      if(f<dem){ cpf[samp]++; histf[md]++; if(cpf[samp]<=5){ printf("CP FAIL samp=%d GR=%d maxdeg=%d m=%d d=%d M=%ld K=%ld W=%ld dem=%ld flow=%d gens:",samp,GR,maxdeg,m,d,M,M/m,W,dem,f); for(int a=0;a<d;a++) printf(" %ld",mg[a]); printf("\n"); fflush(stdout);} }
    }
  }
  for(int i=1;i<32;i++) if(hist[i]) printf("maxdeg=%d tested=%ld CPfail=%ld\n",i,hist[i],histf[i]);
  if(BIND){ printf("binding: deficient cells %ld, min over Z ∋ y equals principal ideal sum in %ld; min margin %ld; margin hist:",BIND_n,BIND_principal,BIND_min); for(int i=0;i<16;i++) printf(" %ld",BIND_h[i]); printf(" | principal hist:"); for(int i=0;i<16;i++) printf(" %ld",PR_h[i]); printf(" principal<0: %ld\n",PR_neg); }
  printf("MAJ fails %ld/%ld  RECT fails %ld/%ld  STAIR fails %ld\n",MAJ_f,MAJ_t,RECT_f,RECT_t,STAIR_f);
  printf("fractional: split among deficient-above fail %ld/%ld; among corners-above fail %ld/%ld\n",FS_f[0],FS_t[0],FS_f[1],FS_t[1]);
  printf("regions:"); for(int i=0;i<6;i++) printf(" rule%d fail %ld/%ld (with deficit %ld)",i,REG_f[i],REG_t[i],REG_td[i]); printf("\n");
  printf("deficits:"); for(int i=1;i<8;i++) printf(" %d:%ld",i,ST_def[i]); printf(" | corner %ld noncorner %ld | top %ld nontop %ld | supp:",ST_corner,ST_noncorner,ST_top,ST_nontop); for(int i=0;i<16;i++) if(ST_sup[i]) printf(" %d:%ld",i,ST_sup[i]); printf(" | single best lower cover insufficient %ld\n",ST_bestlow_insuff);
  if(SAMP==9){ printf("CP %s NS %s\n",cpf[9]?"FAIL":"ok",nsf[9]?"FAIL":"ok"); return 0; }
  printf("seed=%s GR=%d tested %ld %ld %ld %ld | CP fails %ld %ld %ld %ld | NS fails %ld %ld %ld %ld | Wilf fails %ld\n",argv[1],GR,tested[0],tested[1],tested[2],tested[3],cpf[0],cpf[1],cpf[2],cpf[3],nsf[0],nsf[1],nsf[2],nsf[3],wneg);
  return 0; }
