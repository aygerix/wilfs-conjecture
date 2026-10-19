/* General multi-low local payment, end-arc monotonicity, and ASR. */
#ifndef P7_MULTI_LOW_H
#define P7_MULTI_LOW_H
#include "two_low.h"
static long long mg_count,mg_multi,mg_triple,mg_triple_gap,mg_phi_closed,mg_asr_gain,mg_end_gain;
static long long mg_frontier,mg_frontier_end,mg_best_frontier=-1000000000000LL;
static long long mg_three_refined,mg_three_near,mg_three_stars;
static long long mg_joint,mg_cold,mg_psp;
static long long p7L2(int z){if(z<=1)return 0;if(z==2)return 2;if(z==3)return 4;if(z==4)return 8;return z%3?3*(z-1):3*z;}
static long long p7Mac(long long q){long long j=0;while(p7_c2(j+2)<=q)j++;return p7_c3(j+2)+p7_c2(q-p7_c2(j+1)+1);}
static void multiverify(int m,int d,const int *F,const int *degs,const int *n){
 int M=0;for(int i=0;i<m;i++){int v=0;for(int j=0;j<degs[i];j++)v+=n[F[4*i+j]];if(v>M)M=v;}
 if(M/m!=4)return;
 p7_failF=F;p7_failDeg=degs;
 int h=M-4*m+1,cut=2*h-m;if(cut<0)cut=0;
 int a=0,b=0,c=0,e=0,alpha=0,p=0,L=m;
 int *cl=calloc(d,sizeof(int)),*lo=calloc(d,sizeof(int)),*links=calloc(d,sizeof(int));
 for(int j=0;j<d;j++){
  cl[j]=(n[j]+m-h)/m;a+=cl[j]==1;b+=cl[j]==2;c+=cl[j]==3;e+=cl[j]==4;
  if(cl[j]==1){lo[j]=2*(n[j]-m)<h;alpha+=lo[j];p+=3*(n[j]-m)>=2*h;if(n[j]-m<L)L=n[j]-m;}
 }
 int q2=0,q3=0,u3=0,u4=0,k=0,s=0,t=0,J=0,JA=0,JE=0,J0=0,JA0=0,extra=0,hot=0,SR=0,V2=0,V3=0,WW=0,ZZ=0;
 int n0=0,c0=0,u0=0,u1=0,k0=0,k1=0,betaLL=0;
 int theta=(3*h+1)/2;
 long long ell=0,g=0;
 unsigned char *bad=calloc(m,1),*seen=calloc(m,1);
 for(int i=0;i<m;i++){
  int v=0,dg=degs[i],A=0,B=0,C=0,LL=0;
  for(int j=0;j<dg;j++){int z=F[4*i+j];v+=n[z];A+=cl[z]==1;B+=cl[z]==2;C+=cl[z]==3;LL+=lo[z];}
  int band=(v+m-h)/m,tau=v-dg*m,r=v%m;
  p7need(!seen[r],"multi residue injection",m,d,NULL,n);seen[r]=1;
  ell+=(M-v)/m;g+=v/m;
  q2+=dg==2&&A==2&&band==2;q3+=dg==2&&A==2&&band==3;
  u3+=dg==3&&A==3&&band==3;u4+=dg==3&&A==3&&band==4;k+=dg==4;
  s+=dg==2&&A==1&&B==1&&band==3;t+=dg==2&&B==2&&band==3;
  if(dg==2&&A==2&&band==2){if(LL==2){n0++;betaLL+=tau<theta-h;}else for(int j=0;j<dg;j++)if(lo[F[4*i+j]])links[F[4*i+j]]++;}
  c0+=dg==3&&LL==3;
  if(dg==3&&A==3&&band==3){if(LL==3)u0++;else u1++;}
  if(dg==4){if(LL==4)k0++;else k1++;}
  hot+=dg==3&&A==3&&tau>=2*h;
  extra+=(dg==0||(A==dg&&tau<h))&&tau>=cut;
  if(dg==2&&B==2&&band==3)SR++;
  if(dg==2&&B==1&&C==1)SR++;
  if(dg==3&&A==2&&B==1){int bv=0;for(int j=0;j<dg;j++)if(cl[F[4*i+j]]==2)bv=n[F[4*i+j]];if((v-bv+m-h)/m==3){SR++;V3++;}else V2++;}
  if(dg==3&&((A==1&&B==2)||B==3))SR++;
  if(dg==3&&A==1&&B==2)WW++;
  if(dg==3&&B==3)ZZ++;
  int allowed=(dg==1&&A==0)||(dg==2&&A==2&&band==3)||(dg==2&&A==1&&B==1&&band==4)||(dg==2&&B==2&&band==4);
  bad[r]=!allowed;
  if(!allowed&&p7inside(r,h,theta,m)){J++;JA+=A==dg;}
  if(h>=2&&!allowed&&p7inside(r,h,2*h-1,m))JE++;
  if(!allowed&&p7inside(r,h,2*h-L,m)){J0++;JA0+=A==dg;}
 }
 long long q=q2+q3,ra=p7_c2(a+1)-q,D3=(a+2)*q-3*(u3+u4),LC=(a+1LL)*(q2+u3)-4*k;
 long long WA=3LL*a*(a+1)+(a-3)*q-4*(u3+u4)+LC;
 long long T=a*b-s+c*(c+1LL)+e*(3*a+2*b+c)+(c+e)*(2*q2+q3+s+t+u3)+b*u3;
 long long W=d*ell-g,HIGH=LC+p7_c3(p+2)-p7_c3(a+1)+5*ra+D3+T;
 p7need(W>=0,"WILF all actual instances",m,d,NULL,n);
 p7need(SR+hot+extra<=m-h,"ASR general",m,d,NULL,n);
 p7need(W>=WA+T+hot+extra&&W>=HIGH+extra,"ASR transfer",m,d,NULL,n);
 mg_count++;mg_asr_gain+=extra>0;
 if(h>=2){
  int jh=0;for(int j=0;j<(h+1)/2;j++){int r=(h+j)%m;if(r)jh+=bad[r];}
  int last=h-2*((h+1)/2)+2*jh;
  for(int HH=(h+1)/2+1;HH<h;HH++){
   int r=(h+HH-1)%m;if(r)jh+=bad[r];
   int eta=h-2*HH+2*jh;p7need(eta<=last,"end-arc monotonicity",m,d,NULL,n);last=eta;
  }
  p7need(jh==JE,"end-arc count",m,d,NULL,n);
  mg_end_gain+=2-h+2*JE<2*J;
 }
 if(a>=3){
  long long Dmix=b*(q+q2)+(a+1LL)*s-4*V2-3*V3+a*t+(b+1LL)*s-3*WW+(b+2LL)*t-3*ZZ;
  long long qglob=q+s+t,DeltaG=(a+b+2LL)*qglob-3*p7Mac(qglob);
  p7need(Dmix>=DeltaG-2*(a-1LL)*ra,"uniform MIX-GAP",m,d,NULL,n);
  int pp=a-alpha;
  long long stars=0,tri=0;for(int j=0;j<d;j++)if(lo[j]){stars+=links[j]*(a+2LL-links[j]);tri+=p7_c2(links[j]+1);}
  p7need(u3==u0+u1&&k==k0+k1,"general low split",m,d,NULL,n);
  p7need(JA<=alpha+n0+c0+k0+pp*n0-u1+tri,"general intruder count",m,d,NULL,n);
  p7need(J-JA<=b*(alpha+n0)+alpha*c,"general outside count",m,d,NULL,n);
  long long G=c*(c+e+1LL)+e*(3*a+2*b-1LL)+(c+e)*(q3+s+t);
  long long Phi=D3+a-1-2*alpha-2*c0+(2*alpha+1LL-a)*n0+stars
    +(a+1LL)*u0-5*k0+(a+3LL)*u1-3*k1
    +b*(a-1LL+q2+u3-2*alpha-2*n0)+G+(c+e)*(2*q2+u3)-2*alpha*c;
  long long Astar=(a-1LL)*(b+1)+G+LC+b*u3+(c+e)*(2*q2+u3)+D3;
  long long pay=Astar+(b+2LL)*q2+k-2*J;
  p7need(pay>=Phi,"GLOC expansion",m,d,NULL,n);
  long long loss=2*J-(b+2LL)*q2-k;if(loss<0)loss=0;
  p7need(W>=Astar-loss,"general I-LOW",m,d,NULL,n);
  if(Phi>=0){p7need(W>=0,"GLOC Wilf",m,d,NULL,n);mg_phi_closed++;}
  if(alpha){
   int l=0,R=0,rr=(int)ra;for(int j=0;j<d;j++){l+=links[j];R+=cl[j]==1&&!lo[j]&&n[j]-m<theta-2*L;}
   int ns=R-l-2*rr,nw=R-rr,delta=h-2*L,w=(delta+1)/2;if(ns<0)ns=0;if(nw<0)nw=0;
   long long em=p7Mac(q)-u3-u4;
   p7need(em>=0,"uniform legal-cubic defect",m,d,NULL,n);
   p7need(2LL*(3*w-2)>=2LL*ns*(p7_c2(ns)+1)-p7L2(ns)*em,"uniform short WINDOW-SP",m,d,NULL,n);
   p7need(2LL*(3*delta-2)>=2LL*nw*(p7_c2(nw)+1)-p7L2(nw)*em,"uniform wide WINDOW-SP",m,d,NULL,n);
   int ex=l+rr;if(ex>pp)ex=pp;
   long long CH=alpha+n0+c0+l+ex+p7_c3(ex+2)+(n0+1LL*alpha*ex)*pp;
   long long Psi=delta+a-1+(a+3LL)*q2+D3+(a+1LL)*u3-5*k-2*CH
      +b*(a-1LL+q2+u3-2*(alpha+ex+q2))+G+(c+e)*(2*q2+u3)-2LL*c*(alpha+ex);
   long long hp=Astar+(b+2LL)*q2+k+delta-2*J0;
   p7need(JA0<=CH+k&&J0-JA0<=b*(alpha+ex+q2)+c*(alpha+ex),"uniform HLOC counts",m,d,NULL,n);
   p7need(hp>=Psi,"uniform HLOC expansion",m,d,NULL,n);
   /* New sections 31 onward. */
   int tA=p7_c3(a+2)-u3-u4,t0=p7_c3(alpha+2)-c0,betah=0;
   for(int ii=0;ii<m;ii++)if(degs[ii]==2){int x=F[4*ii],y=F[4*ii+1];if(lo[x]&&lo[y]&&n[x]+n[y]-2*m<h-L)betah++;}
   p7need(1LL*alpha*betaLL<=3LL*(u0+t0),"COLD low incidence",m,d,NULL,n);
   p7need(1LL*(alpha+2)*betaLL<=3LL*(u0+t0),"COLD weighted incidence",m,d,NULL,n);
   p7need(p7_c3(alpha+2)-p7Mac(p7_c2(alpha+1)-betaLL)<=u0+t0,"COLD-MAC",m,d,NULL,n);
   p7need(t0<=alpha*(p7_c2(alpha+1)-n0)+em,"LOC-LOW",m,d,NULL,n);
   p7need(betah<=u0+t0,"H0 cold-pair extension",m,d,NULL,n);
   p7need(J-JA<=b*(alpha+betaLL)+alpha*c,"refined fixed outside",m,d,NULL,n);
   p7need(J0-JA0<=b*(alpha+ex+betah+l)+c*(alpha+ex),"refined H0 outside",m,d,NULL,n);
   long long JR=alpha+betaLL+c0+k0+n0*R-u1+tri;
   p7need(JA<=JR,"refined fixed R count",m,d,NULL,n);
   long long FR=D3+a-1-2*alpha-2*betaLL-2*c0+(a+3LL)*n0+stars-2LL*n0*R+(a+1LL)*u0-5*k0+(a+3LL)*u1-3*k1;
   long long PP=a-1+LC+2*q2+k-2*JA;
   p7need(PP+D3>=FR,"exact R payment",m,d,NULL,n);
   if(alpha>=3&&1LL*(alpha+2)*(4*a-5*alpha-11)>=24&&a+1>=alpha){
    long long FC=D3+a-1-2*alpha-2*p7_c3(alpha+2)+(a+3LL)*n0+stars-2LL*n0*R;
    p7need(PP+D3>=FC,"COLD-FIX retains D3",m,d,NULL,n);mg_cold++;
   }
   int nj=alpha+R-rr;if(nj<0)nj=0;int sj=(3*delta+1)/2;
   p7need(2LL*(3*sj-2)>=2LL*nj*(p7_c2(nj)+1)-p7L2(nj)*em,"JOINT-SP",m,d,NULL,n);
   p7need(p7_c3(alpha+R+2)-tA<=3*sj-2,"JOINT-COUNT",m,d,NULL,n);mg_joint++;
   p7need(2LL*u1<=(alpha+1LL)*l,"LLH low-high shadow",m,d,NULL,n);
   if(betaLL){
    long long hc=1000000000LL;
    for(int ee=0;ee<=ex;ee++){
     int nh=pp-ee,rh=rr-(p7_c2(alpha+1)-n0)-(ee>l?ee-l:0);if(rh<0)rh=0;
     long long z=p7_c3(nh+2)-nh*rh-em;if(z<hc)hc=z;
    }
    long long hd=p7_c3(pp-ex+2)-tA+t0;if(hd>hc)hc=hd;if(hc<0)hc=0;
    p7need(hot>=hc,"COLD-HIGH localized",m,d,NULL,n);
   }
   long long bc=2*rr;if(2*a-rr<bc)bc=2*a-rr;
   p7need(W-WA-hot-extra>=b*(u3+bc),"uniform B neighbor transfer retaining ASR",m,d,NULL,n);
   int aminT=h,amaxT=0;for(int j=0;j<d;j++)if(cl[j]==1){int tv=n[j]-m;if(tv<aminT)aminT=tv;if(tv>amaxT)amaxT=tv;}
   long long Ej=p7_c2(rr+1),ep=em;
   long long psp=1LL*a*(p7_c2(a)+1)-4*Ej-9*(a*Ej+(rr+1)*ep+p7_c2(ep));
   p7need(3LL*(amaxT-aminT+1)-2>=psp,"missing-pair signed packing",m,d,NULL,n);mg_psp++;
   long long hLoss=-delta+2*J0-(b+2LL)*q2-k;if(hLoss<0)hLoss=0;
   p7need(W>=Astar-hLoss,"uniform HLOC I-LOW",m,d,NULL,n);
  }
  if(alpha>=3){
   mg_multi++;
   if(alpha==3){
    mg_triple++;
    if(a>=13){
     long long PP=a-1+LC+2*q2+k-2*JA;int l=0;for(int j=0;j<d;j++)l+=links[j];
     if(c+e>0&&WA<0)p7need(pay>=0,"three-low C/E payment",m,d,NULL,n);
     if(a==13&&n0==6&&l==0&&WA<0){
      if(u3||betaLL<=5)p7need(a-1+q2+u3-6-2*betaLL>=1,"a13 effective b payment",m,d,NULL,n);
      else {p7need(c0==0&&PP+D3>=0,"a13 saturated beta payment",m,d,NULL,n);}
     }
     p7need(PP>=15-5*a,"three-low rough all",m,d,NULL,n);
     if(l>=6){p7need(PP>=0,"three-low star payment",m,d,NULL,n);if(WA<0)mg_three_stars++;}
     if(ra<=2&&l>=5-2*ra){
      p7need(PP+D3>=0,"three-low gap star payment",m,d,NULL,n);
      if(WA<0){p7need(pay>=0,"three-low gap star full payment",m,d,NULL,n);mg_three_stars++;}
     }
     if(ra<=2&&l<=5){
      mg_three_refined++;int rr=(int)ra,R=0;for(int j=0;j<d;j++)R+=cl[j]==1&&!lo[j]&&n[j]-m<theta-2*L;
      int nn=R-l-rr;if(nn<0)nn=0;int delta=h-2*L;
      p7need(nn*(nn-1)<=delta-1+2*rr*(rr+1),"three-low partial Sidon",m,d,NULL,n);
      long long ta=p7_c3(a+2)-u3-u4,forced=rr==0?0:rr==1?a:2*a-1,local=ta-forced;
      int ns=R-l-2*rr,nw=R-rr,w=(delta+1)/2;if(ns<0)ns=0;if(nw<0)nw=0;
      p7need(local>=0,"forced missing cubic budget",m,d,NULL,n);
      p7need(2LL*(3*w-2)>=2LL*ns*(p7_c2(ns)+1)-p7L2(ns)*local,"short local SP",m,d,NULL,n);
      p7need(2LL*(3*delta-2)>=2LL*nw*(p7_c2(nw)+1)-p7L2(nw)*local,"wide local SP",m,d,NULL,n);
      p7need(3*w-2>=p7_c3(nn+2)-ta&&3*delta-2>=p7_c3(R+2)-ta,"window cubic cardinality",m,d,NULL,n);
      p7need(R*(R-1)<=2*delta-2+2*rr*(rr+1),"wide partial Sidon",m,d,NULL,n);
      long long Fl=(7LL+l-2*rr)*a-9+2*l-l*l-5*rr;
      long long Bl=(5LL+5*l+7*rr)*a-15-17*l-13*rr+2*p7_c3(l+rr+2);
      long long PH=a-1+LC+2*q2+k+delta-2*JA0;
      p7need(PP+D3>=Fl-12*R,"three-low fixed refinement",m,d,NULL,n);
      p7need(PH>=delta-Bl,"three-low high refinement",m,d,NULL,n);
      p7need(J0-JA0<=b*(3+l+rr+q2)+c*(3+l+rr),"three-low high outside",m,d,NULL,n);
      long long dm=rr*(4LL*a-3*rr-1)/2;
      p7need(D3>=dm,"near-full exact Macaulay gap",m,d,NULL,n);
      long long Fs=rr?(7LL+l+rr)*a-21+2*l-l*l-rr*(3*rr+7)/2:Fl;
      long long Bs=Bl-dm;
      p7need(PP+D3>=Fs-12*R,"three-low retained-gap refinement",m,d,NULL,n);
      p7need(PH+D3>=delta-Bs,"three-low retained high gap",m,d,NULL,n);
      static const int AT[3][6]={{16,26,33,37,41,43},{32,37,40,43,45,47},{39,42,44,46,47,49}};
      if(a>=AT[rr][l]){
       p7need(PP+D3>=0||PH+D3>=0,"three-low arc alternative",m,d,NULL,n);
       long long highpay=Astar+(b+2LL)*q2+k+delta-2*J0;
       p7need(pay>=0||highpay>=0,"three-low full payment",m,d,NULL,n);if(WA<0)mg_three_near++;
      }
     }
     if(a>=16&&WA<0){long long highpay=Astar+(b+2LL)*q2+k+h-2*L-2*J0;p7need(pay>=0||highpay>=0,"complete alpha3 a>=16",m,d,NULL,n);}
    }
    if(a>=13&&ra>=3&&WA<0){
     mg_triple_gap++;
     p7need(q>=6&&D3>=6*a-18,"MG6",m,d,NULL,n);
     p7need(a-1+LC+2*q2+k-2*JA>=15-5*a,"three-low rough",m,d,NULL,n);
     p7need(Phi>=a-3,"three-low missing-pair payment",m,d,NULL,n);
     p7need(W>=0,"three-low theorem",m,d,NULL,n);
    }
   }
   if(a>=7&&WA<0){
    int delta=h-2*L;long long rhs=Astar+(b+2LL)*q2+k;
    long long mn=(a+1LL)*q2;if(mn>p7_c3(a+1))mn=p7_c3(a+1);
    long long old=3LL*delta-((a-1LL)*(b+1)+G+mn+(b+2LL)*q2+b*u3+k+(c+e)*(2*q2+u3));
    if(old>mg_best_frontier)mg_best_frontier=old;
    if(old>0){mg_frontier++;if(2-h+2*JE>rhs&&WA+T+hot+extra<0&&HIGH+extra<0&&Phi<0)mg_frontier_end++;}
   }
  }
 }
 free(cl);free(lo);free(links);free(bad);free(seen);
}
static void multisummary(void){
 printf("MULTI primary=%lld alpha_ge3=%lld alpha3=%lld alpha3_gap_theorem=%lld GLOC_nonnegative=%lld ASR_extra_positive=%lld end_arc_improves=%lld old_frontier=%lld surviving_frontier=%lld closest_old_frontier=%lld\n",mg_count,mg_multi,mg_triple,mg_triple_gap,mg_phi_closed,mg_asr_gain,mg_end_gain,mg_frontier,mg_frontier_end,mg_best_frontier);
 printf("THREE refined_checks=%lld negative_stars_paid=%lld negative_nearfull_paid=%lld\n",mg_three_refined,mg_three_stars,mg_three_near);
 printf("NEW joint=%lld cold_fix=%lld missing_pair_packing=%lld\n",mg_joint,mg_cold,mg_psp);
}
#endif
