/* Exact six-base certificate for ONE-RELAY. Compile/run on fejer only.
 * Residues at the proposed deficit phase. The cubic is u^3, its pair
 * residue is 2, rho0=2u-2, and all maximal-pair positive carries excluded.
 * Every unit set is examined; best pair per remaining residue minimizes A.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static int k,e,m,rho,nu,u,yr,U[12],pool[128],np;
static uint64_t nodes,prune_e,prune_A,leaves,complete;
static int amin=1000000;

static void dfs(int n,int next){
    nodes++;
    int occupied[128]={0},best[128];
    for(int r=0;r<m;r++)best[r]=-1;
    occupied[rho]=occupied[yr]=1;
    for(int i=0;i<n;i++)occupied[U[i]]=1;
    int allsum=0;
    for(int i=0;i<n;i++)for(int j=i;j<n;j++){
        int S=U[i]+U[j];allsum+=S;
        int w=S-rho, carry=w<0?-1:w/m, r=(w%m+m)%m;
        if(occupied[r] || carry==1 || (r>=nu && carry!=-1))continue;
        if(r==2){if(U[i]==u && U[j]==u)best[r]=S;}
        else if(S>best[r])best[r]=S;
    }
    int q=0,prescost=0;
    for(int r=0;r<m;r++)if(best[r]>=0){q++;prescost+=best[r];}
    int missing=n*(n+1)/2-q,A=allsum-prescost;
    if(missing>e){prune_e++;return;}
    if(A>m-1-2*(k-1)){prune_A++;return;}
    if(n==k){
        leaves++;
        if(q!=m-k-2)return;
        complete++;
        if(A<amin)amin=A;
        /* Any complete leaf here would be an actual MaxCL violation.
           Print full selected pair data and STOP immediately. */
        printf("STOP: actual violation k=%d e=%d m=%d rho=%d u=%d A=%d S=%d U=",k,e,m,rho,u,A,A+2*(k-1)-m);
        for(int i=0;i<k;i++)printf("%d,",U[i]);
        printf(" pairs=");
        for(int i=0;i<k;i++)for(int j=i;j<k;j++){
            int S=U[i]+U[j],r=(S-rho+m)%m;
            if(S==best[r])printf("(%d,%d),",U[i],U[j]);
        }
        printf("\n");fflush(stdout);exit(2);
    }
    for(int j=next;j<=np-(k-n);j++){
        U[n]=pool[j];dfs(n+1,j+1);
    }
}

int main(void){
    const int base[6][2]={{6,3},{7,3},{6,4},{7,4},{8,4},{9,4}};
    for(int z=0;z<6;z++){
        k=base[z][0];e=base[z][1];m=k+k*(k+1)/2+2-e;
        nodes=prune_e=prune_A=leaves=complete=0;amin=1000000;
        int us=0;
        for(u=5;u<=(m+3)/4;u++){
            rho=2*u-2;nu=m-rho;yr=m-u+4;
            U[0]=0;U[1]=1;U[2]=u;np=0;
            for(int r=2;r<nu;r++)if(r!=2 && r!=u && r!=rho)pool[np++]=r;
            us++;dfs(3,0);
        }
        printf("k=%d e=%d m=%d u_cases=%d nodes=%llu prune_e=%llu prune_A=%llu leaves=%llu complete=%llu\n",
               k,e,m,us,(unsigned long long)nodes,(unsigned long long)prune_e,
               (unsigned long long)prune_A,(unsigned long long)leaves,(unsigned long long)complete);
        fflush(stdout);
    }
    puts("PASS: no violating complete residue set in the six exact bases");
    return 0;
}
