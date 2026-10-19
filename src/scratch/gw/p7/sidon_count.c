/* Independent integer count for the explicit offset construction. */
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char**argv){
 int p=argc>1?atoi(argv[1]):127;
 if(p<3||p>10000)return 2;
 int*A=malloc(p*sizeof(int));
 for(int i=0;i<p;i++)A[i]=1+2*p*i+(i*i%p);
 int L=A[p-1],Q=p*(p+1)/2;
 int*pair=calloc(2*L+1,sizeof(int));
 unsigned char*unit=calloc(3*L+1,1),*triple=calloc(3*L+1,1);
 for(int i=0;i<p;i++)unit[A[i]]=1;
 int np=0,nt=0;
 for(int i=0;i<p;i++)for(int j=i;j<p;j++){
  int s=A[i]+A[j];
  if(pair[s]){fprintf(stderr,"PAIR COLLISION\n");return 2;}
  pair[s]=1;np++;
 }
 for(int i=0;i<p;i++)for(int j=i;j<p;j++)for(int l=j;l<p;l++){
  int s=A[i]+A[j]+A[l];
  if(!unit[s]&&!triple[s]){triple[s]=1;nt++;}
 }
 int holes=0;for(int i=3;i<=3*L;i++)if(!triple[i])holes++;
 printf("{\"p\":%d,\"L\":%d,\"Q\":%d,\"pairs\":%d,\"triples_outside_A\":%d,\"H1_slack\":%d,\"triple_holes_in_3_to_3L\":%d}\n",p,L,Q,np,nt,2*L+Q-nt,holes);
 free(A);free(pair);free(unit);free(triple);return np==Q?0:2;
}
