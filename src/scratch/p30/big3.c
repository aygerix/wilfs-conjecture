/* big3: S2 / S3 / TFZ / DEAD / W at P18 depth four for large m (lead, 2026-10-20).
 * S = <m, m+B>, B c [1, m-1].  Level of residue r: 1 (r in B), 2 (r in 2B), 3 (r in 3B: order 3; r+m in 2B: order 2),
 * 4 (r in 4B: order 4; r+m in 3B: order 3); otherwise depth > 4.  Carried: p = level 3 order 2, q = level 4 order 3.
 * Construction "sym": D = [0,t) u t[0,t) u t^2[0,u), 2n = u t^2, X = D u (2n-1-D), B = n + X, m = 4n,
 * plus fillers (uncovered residues) until depth <= 4.  usage: ./big3 sym t u | ./big3 list m b1 b2 ... */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int m, k, *B;
static char *lv, *od;
static int levels(void){   /* returns number of uncovered residues; fills lv, od */
  char *b1 = calloc(m, 1), *s2 = calloc(2 * m, 1), *s3 = calloc(2 * m, 1), *s4 = calloc(m, 1);
  for (int i = 0; i < k; i++) b1[B[i]] = 1;
  for (int i = 0; i < k; i++) for (int j = i; j < k; j++) s2[B[i] + B[j]] = 1;
  int *L2 = malloc(sizeof(int) * 2 * m), n2 = 0; for (int s = 0; s < 2 * m; s++) if (s2[s]) L2[n2++] = s;
  for (int a = 0; a < n2; a++) for (int i = 0; i < k; i++){ int s = L2[a] + B[i]; if (s < 2 * m) s3[s] = 1; }
  for (int s = 0; s < m; s++) if (s3[s]) for (int i = 0; i < k; i++){ int t = s + B[i]; if (t < m) s4[t] = 1; }
  int unc = 0; lv[0] = 0; od[0] = 0;
  for (int r = 1; r < m; r++){
    if (b1[r]){ lv[r] = 1; od[r] = 1; }
    else if (s2[r]){ lv[r] = 2; od[r] = 2; }
    else if (s3[r]){ lv[r] = 3; od[r] = 3; }
    else if (s2[r + m]){ lv[r] = 3; od[r] = 2; }
    else if (s4[r]){ lv[r] = 4; od[r] = 4; }
    else if (s3[r + m]){ lv[r] = 4; od[r] = 3; }
    else { lv[r] = 9; od[r] = 0; unc++; }
  }
  free(b1); free(s2); free(s3); free(s4); free(L2); return unc;
}
static int cmpi(const void *a, const void *b){ return *(const int *)a - *(const int *)b; }
int main(int argc, char **argv){
  int cap = 1 << 16; B = malloc(sizeof(int) * cap); k = 0;
  if (!strcmp(argv[1], "sym")){
    int t = atoi(argv[2]), u = atoi(argv[3]); int n2x = u * t * t, n = n2x / 2; if (n2x % 2) { n2x++; n = n2x / 2; }
    m = 4 * n; char *inX = calloc(2 * n, 1);
    for (int i = 0; i < t; i++){ inX[i] = 1; inX[i * t] = 1; } for (int l = 0; l < u; l++) inX[l * t * t] = 1;
    for (int x = 0; x < 2 * n; x++) if (inX[x]) inX[2 * n - 1 - x] |= 2;
    for (int x = 0; x < 2 * n; x++) if (inX[x]) B[k++] = n + x;
    free(inX);
  } else { m = atoi(argv[2]); for (int i = 3; i < argc; i++) B[k++] = atoi(argv[i]); }
  lv = malloc(m); od = malloc(m);
  int fill = 0;
  for (;;){ int unc = levels(); if (!unc) break;
    for (int r = 1; r < m; r++) if (lv[r] == 9){ B[k++] = r; fill++; break; } }
  qsort(B, k, sizeof(int), cmpi);
  int r4 = -1; for (int r = 0; r < m; r++) if (lv[r] == 4) r4 = r;
  if (r4 < 0){ printf("not depth four (c <= 3m)\n"); return 0; }
  int h = r4 + 1; long long c = 3LL * m + h, g = 0; for (int r = 0; r < m; r++) g += lv[r];
  long long e = k + 1, W = e * (c - g) - c;
  long long p = 0, q = 0, O = 0; for (int r = 0; r < m; r++){ O += od[r]; if (lv[r] > od[r]){ if (od[r] == 2) p++; else q++; } }
  #define LVL(v) ((int)((v) / m))
  #define ISAP(v) ((v) >= 0 && LVL(v) == lv[(v) % m])
  #define INS(v) ((v) >= 0 && LVL(v) >= lv[(v) % m])
  long long Z = 0, G = 0, Ful = 0, Ext = 0;
  for (int x = 0; x < k; x++){ long long gx = m + B[x]; int j = 0; while (j < 4 && ISAP((j + 1) * gx)) j++; Z += 4 - j; }
  for (int b = 0; b < k; b++){ long long gb = m + B[b]; int Lb = (B[b] < h) ? 3 : 2;
    for (int x = 0; x < k; x++){ long long gx = m + B[x]; int j = 0; while (j < Lb && ISAP(gb + (j + 1) * gx)) j++;
      G += Lb - j; Ful += (Lb == j); if (Lb - j > 1) Ext += Lb - j - 1; } }
  long long Lam = 0;
  for (int r = 0; r < m; r++){ long long w = (long long)lv[r] * m + r;
    for (int b = 0; b < k; b++){ long long gb = m + B[b]; int j = 0; while (INS(w - (j + 1) * gb)) j++; Lam += j; } }
  long long kk = k, d2 = 0, d3 = 0, d4 = 0, L3 = 0, Jge = 0, Pw = 0;
  for (int r = 1; r < m; r++){ if (lv[r] == 2){ d2++; for (int i = 0; i < k; i++) if (r + B[i] >= m) Jge++; } if (lv[r] == 3) d3++; if (lv[r] == 4) d4++; }
  for (int r = 0; r < h; r++) if (lv[r] <= 3) L3++;
  for (int i = 0; i < k; i++) for (int j = i; j < k; j++) if (B[i] + B[j] >= m) Pw++;
  long long STAR = Pw + Jge + kk * L3 - 4 * d4, Wq = 2 * kk * kk + 2 * kk + (kk - 2) * d2 + kk * L3 - 3 * d3 - 4 * d4;
  printf("d2=%lld d3=%lld d4=%lld L3=%lld Jge=%lld Pw=%lld STAR=%lld Wformula_ok=%d\n", d2, d3, d4, L3, Jge, Pw, STAR, Wq == W);
  printf("m=%d k=%d fill=%d h=%d c=%lld g=%lld W=%lld | p=%lld q=%lld Tc=%lld | Z=%lld G=%lld Ful=%lld Ext=%lld | S2=%lld S3=%lld TFZ=%lld | Lam-O=%lld DEAD=W-(Lam-O)=%lld\n",
    m, k, fill, h, c, g, W, p, q, p + q, Z, G, Ful, Ext, G - p - q, Z + G - p - q, kk * kk + Z - p - q - Ful, Lam - O, W - (Lam - O));
  return 0;
}
