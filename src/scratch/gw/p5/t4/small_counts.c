/* Independent direct-delta audit for a=7,...,13. Run only on fejer. */
#include <stdio.h>
#include <assert.h>
typedef long long I;
static I C(I n,int k){if(n<k)return 0;I v=1;for(int j=1;j<=k;j++)v=v*(n-j+1)/j;return v;}
static I mac(I q,int deg){I out=0;int top=1000;for(int d=deg;d;d--){int z=d-1;while(z+1<top&&C(z+1,d)<=q)z++;out+=C(z+1,d+1);q-=C(z,d);top=z;}assert(q==0);return out;}
static I H(I n){return n*(C(n,2)+1);}
static I lam2(int n){if(n<2)return 0;if(n==2)return 2;if(n==3)return 4;if(n==4)return 8;return n%3?3*(n-1):3*n;}
static I mn(I x,I y){return x<y?x:y;}
static I mx(I x,I y){return x>y?x:y;}
static I isq(I n){I z=0;while((z+1)*(z+1)<=n)z++;return z;}
static I cd(I n,I d){I z=n/d;if(n%d>0)z++;return z;}
static I mingap(int d,I lo,I hi){
 I best=1000000000000LL;if(lo>hi)return best;
 for(int j=0;j<=d;j++){
  I base=C(j+1,2),ss=mx(0,lo-base),tt=mn(j,hi-base);if(ss>tt)continue;
  I v=(d-j)*base+(d+2)*ss-3*C(ss+1,2);if(v<best)best=v;
  v=(d-j)*base+(d+2)*tt-3*C(tt+1,2);if(v<best)best=v;
 }
 return best;
}
int main(void){
 for(int a=7;a<=13;a++){
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
        I bc=u+mn(2*r,2*a-r);assert(bc>=0);
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
            I ng=mx(0,a+1-r),er=C(r+1,2);
            I ml=cd(2*H(ng)-lam2(ng)*ep,2);
            I mlp=H(a+1)-4*er-9*((a+1)*er+(r+1)*ep+C(ep,2));ml=mx(ml,mlp);
            if(ml>maxm)continue;
            upper=mn(upper,maxm-2);
            for(int de=1;de<=upper;de++){
             if(3*de<(a-1)*(b+1)+(a+1)*(q2+u)+D3+(b+2)*q2+b*u-3*k+1)continue;
             I w=(de+1)/2,ns=mx(0,R-l-2*r),nw=mx(0,R-r),nc=mx(0,R-l-r),nj=mx(0,al+R-r),sj=(3*de+1)/2;
             if(nc*(nc-1)>de-1+2*r*(r+1))continue;
             if(2*H(ns)-lam2(ns)*ep>2*(3*w-2))continue;
             if(C(nc+2,3)-t>3*w-2)continue;
             if(2*H(nw)-lam2(nw)*ep>2*(3*de-2))continue;
             if(C(R+2,3)-t>3*de-2)continue;
             if(R*(R-1)>2*de-2+2*r*(r+1))continue;
             if(2*H(nj)-lam2(nj)*ep>2*(3*sj-2))continue;
             if(C(al+R+2,3)-t>3*sj-2)continue;
             I nn=al+R,er=C(r+1,2),psp=H(nn)-4*er-9*(nn*er+(r+1)*ep+C(ep,2));
             if(psp>3*sj-2)continue;
             surv++;
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
  }
  printf("a=%d base=%lld u=%lld packing_profiles=%lld surviving_delta_tuples=%lld\n",a,base,ucount,packing,surv);assert(!surv);
 }
}
