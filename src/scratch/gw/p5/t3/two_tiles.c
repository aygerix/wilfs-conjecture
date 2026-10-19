/* Residue-complete, full-AA adversaries for T2.2. Run only on fejer.
 * Every generated core is a down-set; holes are filled by E axes.
 */
#include "multi_low.h"
#include <string.h>
#define TM 20001
#define TA 40
static uint64_t ts;
static unsigned long long tr(void){ts^=ts<<13;ts^=ts>>7;ts^=ts<<17;return ts;}
static int pick(int lo,int hi){return lo+(int)(tr()%(hi-lo+1));}
static int t[TA],used[TM],degree7[TM],F7[4*TM],weights7[TM],where7[TA][TA][TA];
static int val7[TM],cellN;
static void cell(int deg,int i,int j,int k,int l,int v){
 int rr=v%TM;(void)rr;
 degree7[cellN]=deg;val7[cellN]=v;
 int ids[4]={i,j,k,l};for(int z=0;z<deg;z++)F7[4*cellN+z]=ids[z];cellN++;
}
int main(int argc,char **argv){
 assert(argc==6||argc==7);ts=strtoull(argv[1],0,10)*1099511628211ULL+1;
 int trials=atoi(argv[2]),mlo=atoi(argv[3]),mhi=atoi(argv[4]),amin=atoi(argv[5]),target_alpha=argc==7?atoi(argv[6]):2;assert(mhi<TM);
 int success=0,neg=0,bestWA=1000000,saved3=0;long long best_def=-1000000000,bestPD=1000000000;
 for(int it=0;it<trials;it++){
  int a=pick(amin,amin+13);if(a>=TA)continue;
  int m=pick(mlo,mhi),h=pick(m/3,m),flavor=it%4,ok=1;
  if(h<12||1+a+p7_c2(a+1)>=m)continue;
  memset(used,0,m*sizeof(int));used[0]=used[h-1]=1;
  for(int j=0;j<a;j++){
   int got=0;
   for(int attempt=0;attempt<2000;attempt++){
    int lo,hi;
    if(j==0){lo=flavor==2?1:(h+2)/3;hi=(h-1)/2;if(flavor==0)hi=lo+h/100;if(lo>hi)lo=1;}
    else if(j<target_alpha){lo=t[j-1]+1;hi=(h-1)/2;if(flavor==0&&hi>lo+h/100)hi=lo+h/100;}
    else if(j==target_alpha&&flavor==3){lo=h-t[target_alpha-1];hi=h-t[0]-1;}
    else {lo=(flavor==1)?(h+1)/2:h-t[0];hi=h-1;if(flavor==0)hi=(3*h+1)/2-2*t[1]-1;}
    if(lo>hi)break;
    int z=pick(lo,hi);if(used[z])continue;
    int rr[TA+1],nn=0;rr[nn++]=z;
    for(int k=0;k<=j;k++)rr[nn++]=(z+(k==j?z:t[k]))%m;
    int good=1;
    for(int k=0;k<nn;k++){if(used[rr[k]])good=0;for(int l=0;l<k;l++)if(rr[k]==rr[l])good=0;}
    if(!good)continue;
    t[j]=z;for(int k=0;k<nn;k++)used[rr[k]]=1;got=1;break;
   }
   if(!got){ok=0;break;}
  }
  if(!ok)continue;
  cellN=0;cell(0,0,0,0,0,0);
  for(int j=0;j<a;j++){weights7[j]=m+t[j];cell(1,j,0,0,0,weights7[j]);}
  for(int i=0;i<a;i++)for(int j=i;j<a;j++)cell(2,i,j,0,0,2*m+t[i]+t[j]);
  memset(where7,0,sizeof(where7));
  int cub[12000][3],nc=0;
  for(int i=0;i<a;i++)for(int j=i;j<a;j++)for(int k=j;k<a;k++){cub[nc][0]=i;cub[nc][1]=j;cub[nc++][2]=k;}
  for(int z=nc-1;z>0;z--){int q=pick(0,z);for(int j=0;j<3;j++){int tmp=cub[z][j];cub[z][j]=cub[q][j];cub[q][j]=tmp;}}
  int M=4*m+h-1;
  /* In flavor 0, add arc-intruding cubics first. */
  if(flavor==0){int pos=0;for(int z=0;z<nc;z++){
   int iz=t[cub[z][0]]+t[cub[z][1]]+t[cub[z][2]];
   if(iz>=h&&iz<(3*h+1)/2){for(int j=0;j<3;j++){int tmp=cub[z][j];cub[z][j]=cub[pos][j];cub[pos][j]=tmp;}pos++;}
  }}
  for(int z=0;z<nc;z++){
   int i=cub[z][0],j=cub[z][1],k=cub[z][2],v=3*m+t[i]+t[j]+t[k],r=v%m;
   if(v>M||used[r])continue;
   used[r]=1;where7[i][j][k]=1;cell(3,i,j,k,0,v);
  }
  for(int i=0;i<a;i++)for(int j=i;j<a;j++)for(int k=j;k<a;k++)for(int l=k;l<a;l++){
   int v=4*m+t[i]+t[j]+t[k]+t[l],r=v%m;
   if(v>M||used[r]||!where7[i][j][k]||!where7[i][j][l]||!where7[i][k][l]||!where7[j][k][l])continue;
   used[r]=1;cell(4,i,j,k,l,v);
  }
  int dd=a;
  for(int r=1;r<m;r++)if(!used[r]||r==h-1){
   int v=3*m+h+(r-h+m)%m;weights7[dd]=v;cell(1,dd++,0,0,0,v);used[r]=1;
  }
  assert(cellN==m);
  /* Verify residue bijection and maximum independently of p7sparse. */
  memset(used,0,m*sizeof(int));int actualM=0;
  for(int z=0;z<m;z++){int r=val7[z]%m;assert(!used[r]);used[r]=1;if(val7[z]>actualM)actualM=val7[z];}
  assert(actualM==M);
  long long before=p7_min_p;
  p7sparse(m,dd,F7,degree7,weights7);multiverify(m,dd,F7,degree7,weights7);success++;
  if(target_alpha==2&&((p7_min_p<before&&p7_min_p<0)||p7_currentPD<bestPD)){
   int isPD=p7_currentPD<bestPD;if(isPD)bestPD=p7_currentPD;
   FILE *out=fopen(isPD?"tile_fixed_negative.json":"tile_min_p.json","w");assert(out);fprintf(out,"{\"m\":%d,\"h\":%d,\"weights\":[",m,h);
   for(int j=0;j<dd;j++)fprintf(out,"%s%d",j?",":"",weights7[j]);fprintf(out,"],\"D\":[");
   for(int i=0;i<m;i++){fprintf(out,"%s[",i?",":"");for(int j=0;j<degree7[i];j++)fprintf(out,"%s%d",j?",":"",F7[4*i+j]);fprintf(out,"]");}fprintf(out,"]}\n");fclose(out);
  }
  int q2=0,u3=0,u4=0,k4=0,J=0,K=0,theta=(3*h+1)/2;
  for(int z=0;z<m;z++){
   int dg=degree7[z],pure=dg>0,tau=val7[z]-dg*m;
   for(int j=0;j<dg;j++)pure&=F7[4*z+j]<a;
   q2+=pure&&dg==2&&tau<h;u3+=pure&&dg==3&&tau<h;u4+=pure&&dg==3&&tau>=h;k4+=dg==4;
   int allowed=(dg==1&&!pure)||(pure&&dg==2&&tau>=h);K+=allowed;
   J+=!allowed&&p7inside(val7[z]%m,h,theta,m);
  }
  int q3=p7_c2(a+1)-q2,LC=(a+1)*(q2+u3)-4*k4;
  int WA=3*a*(a+1)+(a-3)*(q2+q3)-4*(u3+u4)+LC;
  neg+=WA<0;
  if(target_alpha==3&&WA<0&&!saved3){
   FILE *out=fopen("three_tile_fixture.json","w");assert(out);fprintf(out,"{\"m\":%d,\"h\":%d,\"weights\":[",m,h);
   for(int j=0;j<dd;j++)fprintf(out,"%s%d",j?",":"",weights7[j]);fprintf(out,"],\"D\":[");
   for(int i=0;i<m;i++){fprintf(out,"%s[",i?",":"");for(int j=0;j<degree7[i];j++)fprintf(out,"%s%d",j?",":"",F7[4*i+j]);fprintf(out,"]");}fprintf(out,"]}\n");fclose(out);saved3=1;
  }
  int e=dd-a;long long G=e*(3*a-1LL)+e*q3;
  long long Astar=(a-1LL)+G+LC+e*(2*q2+u3)+3*(p7_c3(a+2)-u3-u4);
  long long def=2*J-(Astar+2*q2+k4);if(def>best_def)best_def=def;
  if(WA<bestWA){bestWA=WA;if(WA<0){printf("new_negative_WA m=%d h=%d a=%d e=%d q2=%d u3=%d u4=%d k=%d WA=%d offsets=",m,h,a,e,q2,u3,u4,k4,WA);for(int j=0;j<a;j++)printf("%s%d",j?",":"",t[j]);puts("");fflush(stdout);}}
  (void)K;
 }
 printf("two_tiles seed=%s trials=%d successful=%d negative_WA=%d best_WA=%d closest_fixed_deficit=%lld\n",argv[1],trials,success,neg,bestWA,best_def);p7summary();multisummary();
}
