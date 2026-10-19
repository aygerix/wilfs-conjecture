/* P5e: extend the direct-delta audit; optional AMBIENT-C hypothesis.
   argv: amin amax Cnumerator Cdenominator. Cnumerator<0 means unconditional.
   The hypothetical bound is used ONLY on interval sets, never cyclic sets.
   Run only on fejer. Output is a count relaxation, not actual semigroups. */
#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
typedef long long I;
static I C(I n,int k){if(n<k)return 0;I v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}
static I mac(I q,int deg){I out=0;int top=1000;for(int d=deg;d;d--){int z=d-1;while(z+1<top&&C(z+1,d)<=q)z++;out+=C(z+1,d+1);q-=C(z,d);top=z;}assert(q==0);return out;}
static I H(I n){return n*(C(n,2)+1);}
static I lam2(int n){if(n<2)return 0;if(n==2)return 2;if(n==3)return 4;if(n==4)return 8;return n%3?3*(n-1):3*n;}
static I mn(I x,I y){return x<y?x:y;}
static I mx(I x,I y){return x>y?x:y;}
static I isq(I n){I z=0;while((z+1)*(z+1)<=n)z++;return z;}
static I cd(I n,I d){I z=n/d;if(n%d>0)z++;return z;}
static I sp2(int n,I ep){return mx(2*H(n)-lam2(n)*ep,2*H(n)-18*C(ep+1,2));}
/* Missing-pair graph: z=t-d*r+C(r,2) bounds disjoint edge pairs
   plus triangles. A zero z forces a common endpoint. */
static I cover(I r,I z){
 if(!r)return 0;
 assert(z>=0);
 if(!z)return 1;
 I nu=(1+isq(1+8*z))/2,out=mn(r,nu);
 I dm=1+cd(C(r,2)-z,r);
 if(dm>=3)out=mn(out,1+z/(dm-2));
 return out;
}
static I exception_cover(I a,I al,I r,I rll,I l,I k){
 if(!r)return !k&&!rll?mn(a-al,l):-1;
 if(r>a*k-C(k,2))return -1;
 I out=-1,p=a-al;
 for(I cl=mx(0,k-p);cl<=mn(al,k);cl++){
  if(rll>al*cl-C(cl,2))continue;
  if(cl<al)out=mx(out,mn(p,l+mn(k-cl,mn(r-rll,r-k+1))));
  if(cl){I dl=mx(0,rll-(al*(cl-1)-C(cl-1,2))),rem=r-k+1-dl;
   if(rem>=0)out=mx(out,mn(p,l+mn(r-rll,rem)));
  }
 }
 return out;
}
static I mingap(int d,I lo,I hi){
 I best=1000000000000LL;if(lo>hi)return best;
 for(int j=0;j<=d;j++){
  I base=C(j+1,2),ss=mx(0,lo-base),tt=mn(j,hi-base);if(ss>tt)continue;
  I v=(d-j)*base+(d+2)*ss-3*C(ss+1,2);if(v<best)best=v;
  v=(d-j)*base+(d+2)*tt-3*C(tt+1,2);if(v<best)best=v;
 }
 return best;
}
/* Every return of 0 is an exact necessary-profile exclusion by MIX-PACK.
   Endpoint deletion uses the enlarged unit set {0}+A+B. */
static int mixpack(int a,int b,int r,I q,I q2,I t,I u,I k,I wa,I hot,I D3){
 int d=a+b;I Q=C(d+1,2),M=-wa-hot-1-b*u;
 if(M<0)return 0;
 I ss=mx(0,(I)a*b-M);
 I tt=mx(0,cd((I)b*ss+(I)a*b-M,2*a));
 I low=q+ss+tt;
 for(I qg=Q-r;qg>=low;qg--){
  I mg=mac(qg,2),gap=(d+2)*qg-3*mg;
  if(gap>M+2*(a-1)*r||gap>D3+M)continue;
  I ep=(D3+M-gap)/3,rg=Q-qg,zt=C(d+2,3)-mg+ep-d*rg+C(rg,2),zz=zt-mx(0,t-a*r);
  if(zz<0)continue;
  I cv=mn(d,cover(rg,zz)),nn=d+1,er=C(rg+1,2),lower=1000000000000LL;
  for(I cv0=rg?1:0;cv0<=cv;cv0++){
   I ep0=mn(ep,zt-C(cv0,2));if(ep0<0)continue;I n=nn-cv0;
   I lb=mx(cd(sp2(n,ep0),2),H(nn)-4*er-9*(nn*er+(rg+1)*ep0+C(ep0,2)));
   if(lb<lower)lower=lb;
  }
  I upper=-1,co=qg+q2+u;
  /* The caller supplies a conservative global cardinality upper bound. */
  I base=C(d+3,3)-r*(1+b)-t+k;
  I ub0=mn(base,1+d+Q-r+mg+k);
  for(I cc=0;cc*(cc+1+co)<=M;cc++){
   I left=M-cc*(cc+1+co),ee=left/(3*a+2*b+cc+co);
   upper=mx(upper,ub0+cc*(d+1)+ee);
  }
  if(lower<=upper)return 1;
 }
 return 0;
}
int main(int argc,char **argv){
 int amin=argc>1?atoi(argv[1]):14,amax=argc>2?atoi(argv[2]):amin;
 I cn=argc>3?atoll(argv[3]):-1,cd0=argc>4?atoll(argv[4]):1;
 int use_erepair=getenv("P5E_EREPAIR")?atoi(getenv("P5E_EREPAIR")):3;
 assert(cd0>0);
 printf("amin=%d amax=%d ambient_numerator=%lld ambient_denominator=%lld\n",amin,amax,cn,cd0);fflush(stdout);
 for(int a=amin;a<=amax;a++){
  I Q=C(a+1,2),U=C(a+2,3),F=C(a+1,3),base=0,ucount=0,packing=0,surv=0;
  for(int al=3;al<=a;al++){
   int p=a-al;I qa=C(al+1,2),ua=C(al+2,3);
   for(int r=0;r<=Q;r++){
    I q=Q-r,tf=U-mac(q,2);
    for(int n0=mx(0,qa-r);n0<=qa;n0++)for(int l=0;l<=al*p;l++){
     int q2=n0+l;
     if(q2>q||3*(a+1)*q2+(a+17)*r>=3*F)continue;
     I tm=(F-(a+1)*q2+(a-3)*r-1)/4;
     if(F-(a+1)*q2+(a-3)*r-1<0||tf>tm)continue;
     base++;int E=mn(p,l+r);
     assert(q+q2+2>=2*(al+E));
     I S=0;if(p){int full=l/p,z=l%p;S=full*p*(a+2-p)+z*(a+2-z);}
     for(int t=tf;t<=tm;t++){
      I ep=t-tf,D3=3*t-(a+2)*r;
      for(int u0=0;u0<=ua;u0++){
       I k0=mn(mac(u0,3),(al+3)*u0/4);
       I u1max=mn(mn(p*n0,(al+1)*l/2),mn(U-t-u0,mac(q2,2)-u0));
       for(int u1=0;u1<=u1max;u1++){
        I k1=(al+2)*u1/3,k=k0+k1,u=u0+u1,lc=(a+1)*(q2+u)-4*k;
        assert(lc>=(a+1)*q2);
        I wa=-F+lc-(a-3)*r+4*t;
        if(wa>=0)continue;ucount++;
        I bc=u+mx(0,mn(2*r,2*a-r));
        I clow=mx(mx(u0,ua-t),ua-al*(qa-n0)-ep),chi=mn(mac(n0,2),U-t-u1);
        for(int c0=clow;c0<=chi;c0++){
         int t0=ua-c0,betamax=0;
         for(int be=0;be<=n0;be++)if(ua-mac(qa-be,2)<=u0+t0)betamax=be;
         for(int branch=0;branch<1+(betamax>0);branch++){
          int be=branch?betamax:0;I hot=0;
          if(be){I local=1000000;for(int ee=0;ee<=E;ee++){I n=p-ee,rhh=mx(0,r-(qa-n0)-mx(0,ee-l));local=mn(local,C(n+2,3)-n*rhh-ep);}hot=mx(0,mx(C(p-E+2,3)-t+t0,local));if(wa+hot>=0)continue;}
          I bf=a-1+q2+u-2*al-2*be,bh=a-1+q2+u-2*(al+E+l+mn(n0,u0+t0));
          I CH=al+n0+c0+l+E+C(E+2,3)+(n0+al*E)*p;
          I B=2*CH-(a-1)-(a+3)*q2-(a+1)*u+5*k;
          I ff=a-1-2*al-2*be-2*c0+(a+3)*n0+S+(a+1)*u0-5*k0+(a+3)*u1-3*k1+D3;
          for(int R=0;R<=p;R++){
           I fix=ff-2*n0*R;if(fix>=0&&bf>=0)continue;
           I bm=mx(3,mx((-wa-hot+1)/2,isq(2*F+1)-a));if(bc)bm=mn(bm,(-wa-hot-1)/bc);
           if(bf>0){if(fix>=0)continue;bm=mn(bm,(-fix-1)/bf);}
           assert(bm<1000000000);
           for(int b=0;b<=bm;b++){
            if(fix+b*bf>=0)continue;packing++;
            I upper=B-D3-b*bh-1;
            I budget=-wa-hot-b*bc-1,maxm=-1;
            I fullbudget=-wa-hot-1;
            if(fullbudget<mingap(a+b,q,C(a+b+1,2)-r-1)-2*(a-1)*r){
             I rem=fullbudget-b*u-2*b*r,mf=-1,basecost=q+q2+u+a*b+C(b+1,2);
             if(rem<0)continue;
             for(int cc=0;cc*(cc+1+basecost)<=rem;cc++){
              I left=rem-cc*(cc+1+basecost),ee=left/(3*a+2*b+cc+basecost);
              I mm=C(a+b+3,3)-r*(1+b)-t+k+cc*(a+b+1)+ee;if(mm>mf)mf=mm;
             }
             I missing=t+b*r+rem/3,eg=missing-(C(a+b+2,3)-mac(C(a+b+1,2)-r,2));
             if(eg<0)continue;
             I nf=mx(0,a+b+1-r),nf0=a+b+1,er0=C(r+1,2);
             I lf=mx(cd(2*H(nf)-lam2(nf)*eg,2),H(nf0)-4*er0-9*(nf0*er0+(r+1)*eg+C(eg,2)));
             if(lf>mf)continue;
            }
            for(int cc=0;cc*(cc+1+q+q2+u)<=budget;cc++){
             I left=budget-cc*(cc+1+q+q2+u),ee=left/(3*a+2*b+cc+q+q2+u);
             I mm=C(a+b+3,3)-r*(1+b)-t+k+cc*(a+b+1)+ee;if(mm>maxm)maxm=mm;
            }
            I cvA=cover(r,t-a*r+C(r,2)-mx(0,t0-al*(qa-n0)));
            I ng=mx(0,a+1-cvA),er=C(r+1,2);
            I ml=cd(2*H(ng)-lam2(ng)*ep,2);
            I mlp=H(a+1)-4*er-9*((a+1)*er+(r+1)*ep+C(ep,2));ml=mx(ml,mlp);
            if(ml>maxm)continue;
            upper=mn(upper,maxm-2);
            I delta_floor=mx(1,cd((a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*k+1,3));
            int anycover=0;
            for(I kk0=r?1:0;kk0<=mn(a,cvA);kk0++){
             I ep0=mn(ep,t-a*r+C(r,2)-C(kk0,2));if(ep0<0)continue;
             I ex0=use_erepair==0?E:use_erepair==1?mn(p,l+(r?r-kk0+1:0)):use_erepair==2?mn(p,l+(r?mn(r-(qa-n0),r-kk0+1):0)):exception_cover(a,al,r,qa-n0,l,kk0);
             if(ex0<0)continue;
             I ch0=al+n0+c0+l+ex0+C(ex0+2,3)+(n0+al*ex0)*p;
             I bh0=a-1+q2+u-2*(al+ex0+l+mn(n0,u0+t0));
             I up0=2*ch0-(a-1)-(a+3)*q2-(a+1)*u+5*k-D3-b*bh0-1;
             if(delta_floor<=mn(upper,up0))anycover=1;
            }
            if(!anycover)continue;
            int mpchecked=0,mpok=0,firstde=0,lastde=0;
            for(int de=delta_floor;de<=upper;de++){
             if(3*de<(a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*k+1)continue;
             I w=(de+1)/2,ns=mx(0,R-l-r-cvA),nw=mx(0,R-cvA),nc=mx(0,R-l-r),nj=mx(0,al+R-cvA),sj=(3*de+1)/2;
             if(nc*(nc-1)>de-1+2*r*(r+1))continue;
             if(2*H(ns)-lam2(ns)*ep>2*(3*w-2))continue;
             if(C(nc+2,3)-t>3*w-2)continue;
             if(2*H(nw)-lam2(nw)*ep>2*(3*de-2))continue;
             if(C(R+2,3)-t>3*de-2)continue;
             if(R*(R-1)>2*de-2+2*r*(r+1))continue;
             if(2*H(nj)-lam2(nj)*ep>2*(3*sj-2))continue;
             if(cn>=0){
              if(cd0*H(ns)-cn*ep>cd0*(3*w-2))continue;
              if(cd0*H(nw)-cn*ep>cd0*(3*de-2))continue;
              if(cd0*H(nj)-cn*ep>cd0*(3*sj-2))continue;
             }
             if(C(al+R+2,3)-t>3*sj-2)continue;
             I nn=al+R,er=C(r+1,2),psp=H(nn)-4*er-9*(nn*er+(r+1)*ep+C(ep,2));
             if(psp>3*sj-2)continue;
             int linked=0;
             I ztotal=t-a*r+C(r,2);
             for(I cc0=r?1:0;cc0<=mn(a,cvA);cc0++){
              I ep0=mn(ep,ztotal-C(cc0,2));if(ep0<0)continue;
              I ex0=use_erepair==0?E:use_erepair==1?mn(p,l+(r?r-cc0+1:0)):use_erepair==2?mn(p,l+(r?mn(r-(qa-n0),r-cc0+1):0)):exception_cover(a,al,r,qa-n0,l,cc0);
              if(ex0<0)continue;
              I ch0=al+n0+c0+l+ex0+C(ex0+2,3)+(n0+al*ex0)*p;
              I bh0=a-1+q2+u-2*(al+ex0+l+mn(n0,u0+t0));
              I up0=2*ch0-(a-1)-(a+3)*q2-(a+1)*u+5*k-D3-b*bh0-1;
              if(de>up0)continue;
              I nn0=a+1-cc0;
              I ml0=mx(cd(sp2(nn0,ep0),2),H(a+1)-4*er-9*((a+1)*er+(r+1)*ep0+C(ep0,2)));
              if(ml0>maxm)continue;
              I ns0=mx(0,R-l-r-cc0),nw0=mx(0,R-cc0),nj0=mx(0,al+R-cc0);
              if(sp2(ns0,ep0)>2*(3*w-2))continue;
              if(sp2(nw0,ep0)>2*(3*de-2))continue;
              if(sp2(nj0,ep0)>2*(3*sj-2))continue;
              I ps0=H(nn)-4*er-9*(nn*er+(r+1)*ep0+C(ep0,2));
              if(ps0>3*sj-2)continue;
              if(cn>=0&&(cd0*H(ns0)-cn*ep0>cd0*(3*w-2)||cd0*H(nw0)-cn*ep0>cd0*(3*de-2)||cd0*H(nj0)-cn*ep0>cd0*(3*sj-2)))continue;
              linked=1;break;
             }
             if(!linked)continue;
             if(!mpchecked){mpchecked=1;mpok=mixpack(a,b,r,q,q2,t,u,k,wa,hot,D3);}
             if(!mpok)continue;
             surv++;
             if(!firstde)firstde=de;lastde=de;
             if(surv<=20)fprintf(stderr,"SURV a=%d alpha=%d r=%d n0=%d l=%d t=%d eps=%lld u0=%d u1=%d c0=%d beta=%d R=%d b=%d delta=%d upper=%lld WA=%lld\n",a,al,r,n0,l,t,ep,u0,u1,c0,be,R,b,de,upper,wa);
            }
            if(firstde)printf("PROFILE a=%d alpha=%d r=%d n0=%d l=%d t=%d eps=%lld u0=%d u1=%d c0=%d beta=%d R=%d b=%d first=%d last=%d k=%lld cv=%lld WA=%lld\n",a,al,r,n0,l,t,ep,u0,u1,c0,be,R,b,firstde,lastde,k,cvA,wa);
           }
          }
         }
        }
       }
      }
     }
    }
   }
  }
  printf("a=%d base=%lld u=%lld packing_profiles=%lld surviving_delta_tuples=%lld\n",a,base,ucount,packing,surv);fflush(stdout);
 }
}
