/* Exact ordinary-sum audit of A/B direction cores in actual primary tiles. */
#ifndef P5G_CHECKS_H
#define P5G_CHECKS_H
static long long pgcores[2],pgv[2],pgr[2],pgsfmax[2],pgcomplete[2],pgpair[2];
static long long pgC2(long long x){return x*(x-1)/2;}
static void pgcore(int m,int h,int d,const int *FF,const int *deg,const int *weights,int cl){
 int ids[128],idx[128],t[128],n=0;
 assert(d<1000000);
 for(int j=0;j<d;j++)if((weights[j]+m-h)/m==cl){assert(n<128);ids[n]=j;t[n++]=weights[j]-m;}
 if(n<2)return;
 for(int j=0;j<n;j++){idx[j]=j;for(int k=0;k<j;k++)if(t[idx[j]]<t[idx[k]]){int z=idx[j];idx[j]=idx[k];idx[k]=z;}}
 int sorted[128],newids[128];for(int j=0;j<n;j++){sorted[j]=t[idx[j]];newids[j]=ids[idx[j]];}
 memcpy(t,sorted,n*sizeof(int));memcpy(ids,newids,n*sizeof(int));
 int *map=malloc(d*sizeof(int));for(int j=0;j<d;j++)map[j]=-1;for(int j=0;j<n;j++)map[ids[j]]=j;
 unsigned char retained[128][128]={{0}};long long present=0;
 for(int z=0;z<m;z++)if(deg[z]==2){
  int i=map[FF[4*z]],j=map[FF[4*z+1]];if(i<0||j<0)continue;
  int val=weights[FF[4*z]]+weights[FF[4*z+1]],band=(val+m-h)/m;
  if(cl==1||band==3)retained[i][j]=retained[j][i]=1;
 }
 int span=t[n-1]-t[0]+1,sz=3*span+3;
 int *off=calloc(2*span+3,sizeof(int)),*diff=calloc(span+1,sizeof(int));
 int *f=calloc(sz,sizeof(int)),*rep=calloc(sz,sizeof(int)),*legal=calloc(sz,sizeof(int));
 int *centre=calloc(2*span+3,sizeof(int)),*proper=calloc(sz,sizeof(int));
 unsigned char *sig=calloc(sz,1);
 for(int i=0;i<n;i++)t[i]-=sorted[0];
 long long r=0;int D=0,G=1,Gall=0;
 for(int i=0;i<n;i++){
  int de=0;for(int j=0;j<n;j++)if(j!=i&&!retained[i][j])de++;
  if(de>D)D=de;
  for(int j=i+1;j<n;j++)if(retained[i][j])assert(++off[t[i]+t[j]]==1);
  else{r++;centre[t[i]+t[j]]++;}
 }
 for(int i=0;i<n;i++)for(int j=0;j<i;j++)diff[t[i]-t[j]]++;
 for(int x=0;x<span;x++)assert(diff[x]<=2*D+2);
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)rep[2*t[i]+t[j]]++;
 for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
  int v=t[i]+t[j]+t[k];f[v]++;
  if(retained[i][j]&&retained[i][k]&&retained[j][k])legal[v]++;
 }
 for(int z=0;z<m;z++)if(deg[z]==3){
  int i=map[FF[4*z]],j=map[FF[4*z+1]],k=map[FF[4*z+2]];
  if(i>=0&&j>=0&&k>=0&&i!=j&&i!=k&&j!=k){
   assert(retained[i][j]&&retained[i][k]&&retained[j][k]);present++;
  }
 }
 long long total=0,rp=0,eta=0,fp=0,fr=0;
 for(int x=0;x<sz;x++){total+=legal[x];if(legal[x]>G)G=legal[x];if(f[x]>Gall)Gall=f[x];rp+=pgC2(rep[x]);fp+=pgC2(f[x]);fr+=(long long)f[x]*rep[x];}
 for(int x=0;x<2*span;x++)eta+=pgC2(centre[x]);
 long long v=total-present;assert(v>=0);assert(rp<=(2*D+2)*pgC2(n));
 for(int i=0;i<n;i++)for(int j=i;j<n;j++)for(int k=0;k<n;k++)if(k!=i&&k!=j){
  int x=t[i]+t[j]-t[k]+span;sig[x]=1;if(i<j&&retained[i][j])proper[x]++;
 }
 long long cp=0,overlap=0,ns=0;
 for(int i=0;i<n;i++){overlap+=proper[t[i]+span];sig[t[i]+span]=1;}
 for(int x=0;x<sz;x++){cp+=pgC2(proper[x]);ns+=sig[x];}
 assert(overlap<=(D+1)*n);assert(cp<=9*fp+6*fr+4*rp);
 long long H=n*(pgC2(n)+1),loss=H-ns,dd=2*D+2;
 assert(loss<=n*(n-1)+r*(n-2)+cp+overlap);
 long long rhs2=9LL*G*v+2LL*(6*G+4*D+5)*n*n;
 rhs2+=2LL*(9*G+6*dd+7)*n*r+18*dd*pgC2(r)+18LL*n*eta;
 rhs2-=2LL*(3*D+4)*n+4*r;
 assert(2*loss<=rhs2);assert(ns<=3*span-2);
 pgcores[cl-1]++;pgv[cl-1]+=v>0;pgr[cl-1]+=r>0;
 if(Gall>pgsfmax[cl-1])pgsfmax[cl-1]=Gall;
 pgcomplete[cl-1]+=present==(long long)n*(n-1)*(n-2)/6;
 pgpair[cl-1]+=D==0;
 free(map);free(off);free(diff);free(f);free(rep);free(legal);free(centre);free(proper);free(sig);
}
static void pgverify(int m,int d,const int *FF,const int *deg,const int *weights){
 int M=0;for(int z=0;z<m;z++){int v=0;for(int j=0;j<deg[z];j++)v+=weights[FF[4*z+j]];if(v>M)M=v;}
 int h=M-4*m+1;assert(1<=h&&h<=m);
 pgcore(m,h,d,FF,deg,weights,1);pgcore(m,h,d,FF,deg,weights,2);
}
static void pgsummary(void){
 for(int j=0;j<2;j++)printf("P5g_core=%c cores=%lld positive_legal_defect=%lld missing_offpairs=%lld sf_max=%lld all_offpairs=%lld all_SF_present=%lld FAILURES=0\n",j?'B':'A',pgcores[j],pgv[j],pgr[j],pgsfmax[j],pgpair[j],pgcomplete[j]);
}
#endif
