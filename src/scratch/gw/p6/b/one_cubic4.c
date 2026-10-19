/* The sole finite base of the full-quadratic-face, one-cubic theorem.
 * k=4, Q all ten pairs, T={3 e_a}; all sorted unit labelings, m=21..27.
 * Bigger m follows from CR, k>=5 from FLAT-CR, k<=3 from H3-CORE3.
 * fejer only, nice single core; exact integer arithmetic.
 */
#include <assert.h>
#include <stdio.h>
#include <stdint.h>
typedef unsigned long long ull;
typedef long long ll;
int main(void){
 ull tot=0,tph=0;ll gm=1LL<<60;
 for(int m=21;m<=27;m++){
  ull vectors=0,bases=0,instances=0,phases=0;ll mn=1LL<<60;
  for(int a=1;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++)for(int e=c+1;e<m;e++){
   vectors++;int P[4]={a,b,c,e},r[15]={0,a,b,c,e},pi[10],pj[10],good=1,len=5;
   ull used=1ULL|(1ULL<<a)|(1ULL<<b)|(1ULL<<c)|(1ULL<<e);
   for(int i=0;i<4&&good;i++)for(int j=i;j<4;j++){
    int x=(P[i]+P[j])%m;if(used>>x&1){good=0;break;}
    used|=1ULL<<x;pi[len-5]=i;pj[len-5]=j;r[len++]=x;
   }
   if(!good)continue;
   assert(len==15);bases++;
   for(int var=0;var<4;var++){
    int cube=(3*P[var])%m;if(used>>cube&1)continue;
    instances++;
    for(int sig=0;sig<m;sig++){
     ll sn=0,sa=0;
     for(int j=0;j<15;j++){
      int x=(r[j]+m-sig)%m;
      if(j<5||(pi[j-5]==var&&pj[j-5]==var))sn+=x;else sa+=x;
     }
     ll S=(m-11)*sn-sa-2*((cube+m-sig)%m);
     phases++;if(S<mn)mn=S;if(S<gm)gm=S;
     if(S<0){printf("MAXCL_COUNTEREXAMPLE m=%d P=%d,%d,%d,%d var=%d sigma=%d S=%lld\n",m,a,b,c,e,var,sig,S);return 2;}
    }
   }
  }
  tot+=instances;tph+=phases;
  printf("ONE_CUBIC4 m=%d vectors=%llu pair_bases=%llu injections=%llu phases=%llu min=%lld FAILURES=0\n",m,vectors,bases,instances,phases,mn);
 }
 printf("ONE_CUBIC4_PASS injections=%llu phases=%llu min=%lld\n",tot,tph,gm);return 0;
}
