/* Independent finite a=6 count certificate. Fejer only, nice.
 * Uses loss variables at their caps, rather than the Python enumeration
 * of actual counts. Every range is bounded explicitly (b<=11).
 */
#include <stdio.h>
#include <stdint.h>
#include <assert.h>
static long long counts[8];
static int choose2(int n){return n*(n-1)/2;}
static int choose3(int n){return n*(n-1)*(n-2)/6;}
static int P(int d){return choose3(d+3);}
static int H(int d){return P(d)+2*choose3(d+1);}
static int twiceL(int s){if(s==2)return 2;if(s==3)return 4;if(s==4)return 8;return 3*(s-(s%3!=0));}
static int gcd(int x,int y){while(y){int z=x%y;x=y;y=z;}return x;}
static int pack(int m,int s,int r){
 int HH=H(s-1);
 if(2*m<2*HH-twiceL(s)*r)return 1;
 if(s>=6&&s%3==0){int k=s/3;if(2*m<2*HH-(3*s-6)*r-6*(k-1)*gcd(k,m))return 1;}
 return 0;
}
static int grow2(int n){int r=1;while(choose2(r+1)<=n)r++;int rem=n-choose2(r);return choose3(r+1)+choose2(rem+1);}
static int goodface(int m,const int *bad,int t,int t3,int vc,int vtotal,int w,int z){
 /* BB pairs indexed 00,01,11; all eight possible I3 subsets. */
 int pi[3]={0,0,1},pj[3]={0,1,1};
 for(int mask=0;mask<8;mask++){
  if(__builtin_popcount((unsigned)mask)!=t3)continue;
  int wc=0;
  for(int j=0;j<3;j++)if(mask&(1<<j)){int p=bad[pi[j]]>bad[pj[j]]?bad[pi[j]]:bad[pj[j]];wc+=6-p;}
  int zc=((mask&1)?1:0)+((mask&3)==3)+((mask&6)==6)+((mask&4)?1:0);
  if(w>wc||z>zc)continue;
  int good=(!bad[0]&&(mask&1))||(!bad[1]&&(mask&4));
  if(!good)return 0;
  int omitted=t+vc-vtotal+wc-w+zc-z;
  if(!pack(m,8,omitted))return 0;
 }
 return 1;
}
int main(void){
 const int ucap[5]={0,1,2,4,5},kcap[6]={0,1,2,3,5,6};
 const int nbad[9]={0,1,1,1,1,1,1,2,2};
 const int b1[9]={0,1,2,3,4,5,6,1,1},b2[9]={0,0,0,0,0,0,0,1,2};
 int profile_count=0;
 for(int q2=0;q2<=4;q2++)for(int u3=0;u3<=ucap[q2];u3++)for(int k=0;k<=kcap[u3];k++){
  int low=7*(q2+u3)-4*k;
  for(int t=0;low+4*t<35;t++){
   profile_count++;int budget=34-low-4*t,q3=21-q2;
   for(int b=0;b<=11;b++){
    int B=choose2(b+1),Z=choose3(b+2),d=6+b;
    for(int pat=0;pat<9;pat++){
     int nb=nbad[pat];if(nb>b)continue;
     int bad[12]={0};bad[0]=b1[pat];bad[1]=b2[pat];
     int p=b1[pat]+b2[pat],s3=6*b-p;
     int neigh=(b1[pat]*(27-3*b1[pat])+b2[pat]*(27-3*b2[pat]))/2;
     if(neigh+b*u3>budget)continue;
     int lost=0;for(int j=0;j<nb;j++)lost+=21-choose2(7-bad[j]);
     int losses[80],ix=0;
     for(int j=0;j<b;j++)for(int z=j;z<b;z++)losses[ix++]=bad[j]>bad[z]?bad[j]:bad[z];
     for(int j=0;j<B;j++)for(int z=j+1;z<B;z++)if(losses[z]>losses[j]){int tmp=losses[j];losses[j]=losses[z];losses[z]=tmp;}
     int suffix[80]={0};for(int j=B-1;j>=0;j--)suffix[j]=suffix[j+1]+losses[j];
     int maxlow=nb*q2;if(maxlow>lost)maxlow=lost;
     for(int lowlost=0;lowlost<=maxlow;lowlost++){
      int v2c=b*q2-lowlost,v3c=b*q3-lost+lowlost;if(v2c<0||v3c<0)continue;
      for(int rab=0;rab<=p;rab++)for(int rbb=0;rbb<=B&&4*rbb<=budget;rbb++)for(int t4=0;t4<=B-rbb;t4++){
       int q=rbb+t4,t3=B-q,wc=6*t3-suffix[q],wshadow=(b+1)*s3/2;
       if(wc>wshadow)wc=wshadow;
       int zc=grow2(t3),zshadow=q?Z-b:Z;if(zc>zshadow)zc=zshadow;
       if(wc<0||zc<0)continue;
       int fixed=p+b*u3+4*rab+4*rbb;
       int dv=2*b*q2+b*q3+7*s3-4*v2c-3*v3c;
       int dw=6*t3+(b+1)*s3-3*wc,dz=(b+2)*t3-3*zc;
       assert(dv>=0&&dw>=0&&dz>=0);
       int left=budget-fixed-dv-dw-dz;if(left<0)continue;
       for(int x2=0;x2<=v2c&&4*x2<=left;x2++)
       for(int x3=0;x3<=v3c&&4*x2+3*x3<=left;x3++)
       for(int xw=0;xw<=wc&&4*x2+3*(x3+xw)<=left;xw++)
       for(int xz=0;xz<=zc&&4*x2+3*(x3+xw+xz)<=left;xz++){
        int v2=v2c-x2,v3=v3c-x3,w=wc-xw,z=zc-xz;
        int r=t+b*q2-v2+b*q3-v3+6*B-w+Z-z,quad=rab+rbb;
        int m=P(d)-quad-r+k;counts[0]++;
        if(2*m<2*H(6)-twiceL(7)*t){counts[1]++;continue;}
        if(!quad&&2*m<2*H(d)-twiceL(d+1)*r){counts[2]++;continue;}
        if(!quad&&pack(m,d+1,r)){counts[3]++;continue;}
        if(quad){
         int forced=quad*d-choose2(quad);
         if(r<forced){counts[4]++;continue;}
         if(d-quad>=1&&2*m<2*H(d-quad)-twiceL(d-quad+1)*(r-forced)){counts[5]++;continue;}
        }
        if(b==2&&goodface(m,bad,t,t3,b*21-lost,v2+v3,w,z)){counts[6]++;continue;}
        counts[7]++;printf("SURVIVOR q2=%d u3=%d k=%d t=%d b=%d pat=%d rab=%d rbb=%d t4=%d m=%d r=%d\n",q2,u3,k,t,b,pat,rab,rbb,t4,m,r);
       }
      }
     }
    }
   }
  }
 }
 printf("A6_FINITE profiles=%d bmax=11 critical=%lld A=%lld global=%lld HP=%lld forced=%lld deleted=%lld good_B=%lld survivors=%lld\n",profile_count,counts[0],counts[1],counts[2],counts[3],counts[4],counts[5],counts[6],counts[7]);
 assert(profile_count==75&&counts[7]==0);
}
