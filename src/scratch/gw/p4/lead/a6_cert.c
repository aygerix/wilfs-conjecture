/* Lead's independent check of the (A6.1) weight certificate (P4_REPORT sec.18).
   m=74, rho in {0,1}, h=m-rho. Six A weights n_i=m+t_i, 1<=t_1<...<t_6<h.
   One omitted AA pair; all 20 other pairs have t_i+t_j>=h (all present AA in I3, q2=0).
   Lower cells: 0, 6 units, 20 AA: need 27 distinct residues mod m.
   Eligible cubics: not divisible by omitted pair, T=t_i+t_j+t_k<=m+h-1.
   Necessary: #eligible>=47, some eligible with T==m+h-1, lower U eligible residues = Z/m. */
#include <stdio.h>
#include <string.h>
int main(void){
  const int m=74;
  for(int rho=0;rho<=1;rho++){
    int h=m-rho; long lower_ok=0, enough=0, enough_max=0, cover=0; int bestunc=1000;
    int t[6];
    for(t[1]=(h+1)/2;t[1]<h;t[1]++) for(t[2]=t[1]+1;t[2]<h;t[2]++) for(t[3]=t[2]+1;t[3]<h;t[3]++)
    for(t[4]=t[3]+1;t[4]<h;t[4]++) for(t[5]=t[4]+1;t[5]<h;t[5]++)
    for(t[0]=1;t[0]<t[1];t[0]++){
      int small = (2*t[0]<h);
      if(small && t[0]+t[1]<h) continue;
      for(int a=0;a<6;a++) for(int b=a;b<6;b++){
        if(small && !(a==0&&b==0)) continue;
        /* check pair constraint */
        int ok=1;
        for(int i=0;i<6&&ok;i++) for(int j=i;j<6;j++){ if(i==a&&j==b) continue; if(t[i]+t[j]<h){ok=0;break;} }
        if(!ok) continue;
        char seen[80]; memset(seen,0,sizeof seen);
        int cnt=0; seen[0]=1; cnt=1; ok=1;
        for(int i=0;i<6&&ok;i++){int r=t[i]%m; if(seen[r]) ok=0; else {seen[r]=1;cnt++;}}
        for(int i=0;i<6&&ok;i++) for(int j=i;j<6;j++){ if(i==a&&j==b) continue; int r=(t[i]+t[j])%m; if(seen[r]){ok=0;break;} seen[r]=1;cnt++; }
        if(!ok) continue;
        lower_ok++;
        int nel=0, hasmax=0; char cov[80]; memcpy(cov,seen,sizeof seen);
        for(int i=0;i<6;i++) for(int j=i;j<6;j++) for(int k=j;k<6;k++){
          /* divisible by omitted pair {a,b}? */
          int div=0;
          int ms[3]={i,j,k};
          if(a==b){ int c=0; for(int z=0;z<3;z++) if(ms[z]==a) c++; if(c>=2) div=1; }
          else { int ca=0,cb=0; for(int z=0;z<3;z++){ if(ms[z]==a) ca++; if(ms[z]==b) cb++; } if(ca&&cb) div=1; }
          if(div) continue;
          int T=t[i]+t[j]+t[k];
          if(T>m+h-1) continue;
          nel++; if(T==m+h-1) hasmax=1; cov[T%m]=1;
        }
        if(nel<47) continue;
        enough++;
        if(!hasmax) continue;
        enough_max++;
        int unc=0; for(int r=0;r<m;r++) if(!cov[r]) unc++;
        if(unc<bestunc) bestunc=unc;
        if(unc==0) cover++;
        printf("rho=%d t=(%d,%d,%d,%d,%d,%d) omit=(%d,%d) eligible=%d uncovered=%d\n",rho,t[0],t[1],t[2],t[3],t[4],t[5],a+1,b+1,nel,unc);
      }
    }
    printf("RHO %d: lower-injective choices=%ld enough-eligible=%ld +max=%ld full-cover=%ld best_uncovered=%d\n",rho,lower_ok,enough,enough_max,cover,bestunc);
  }
  return 0;
}
