#include "multi_low.h"
int main(int argc,char **argv){
 assert(argc==2);FILE *f=fopen(argv[1],"r");assert(f);
 int m,d;assert(fscanf(f,"%d%d",&m,&d)==2);
 int *n=malloc(d*sizeof(int)),*deg=malloc(m*sizeof(int)),*F=calloc((size_t)4*m,sizeof(int));
 for(int j=0;j<d;j++)assert(fscanf(f,"%d",n+j)==1);
 for(int i=0;i<m;i++){assert(fscanf(f,"%d",deg+i)==1&&deg[i]<=4);for(int j=0;j<deg[i];j++)assert(fscanf(f,"%d",F+4*i+j)==1);}
 fclose(f);p7sparse(m,d,F,deg,n);multiverify(m,d,F,deg,n);p7summary();multisummary();free(n);free(deg);free(F);
}
