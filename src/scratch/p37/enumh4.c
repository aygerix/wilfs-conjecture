/* enumh4: exhaustive enumeration of the exact-MILP domain of kunz_cert_milp.py --open --h4 (lead, 2026-10-21).
 * Domain: multiplicity m, embedding dimension e (d = e-1 generators besides m), every Kunz coordinate k_s in [1, K]
 * (all Apery elements < (K+1)m), c >= 4m+1, 3e < m, Apery height >= 4 (some tight pair with two non-generator parts).
 * Every S in the domain is generated exactly once: d distinct nonzero residues s_1 < .. < s_d and levels k_b in [1, K],
 * g_b = m k_b + s_b, kept iff each g_b is a minimal generator (g_b = w_{s_b} and no tight pair sums to s_b).
 * RT2 (and RT, R, TX) depend only on the key (conductor residue r, q = k_r, set of tight pairs), so each distinct key is
 * written once (hex key, representative generators, number of S with that key, min W over them).  W is exact (integers).
 * usage: ./enumh4 m e K part nparts outfile        (process 'part' of 'nparts' handles residue combinations idx % nparts) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define MAXM 24
typedef struct { uint64_t b[4]; uint8_t r, q; } Key;
typedef struct { Key k; int used; long cnt; long minW; int G[8]; } Ent;
static Ent *tab; static long tsz, tn;
static uint64_t hk(const Key *k){ uint64_t h = 1469598103934665603ULL; const uint8_t *p = (const uint8_t *)k;
  for (size_t i = 0; i < sizeof(Key); i++){ h ^= p[i]; h *= 1099511628211ULL; } return h; }
static int keq(const Key *a, const Key *b){ return memcmp(a, b, sizeof(Key)) == 0; }
static void grow(void);
static void ins(const Key *k, long W, const int *G, int ng){
  if (2 * (tn + 1) > tsz) grow();
  uint64_t h = hk(k) & (tsz - 1);
  while (tab[h].used){ if (keq(&tab[h].k, k)){ tab[h].cnt++; if (W < tab[h].minW){ tab[h].minW = W; memcpy(tab[h].G, G, ng * sizeof(int)); } return; } h = (h + 1) & (tsz - 1); }
  tab[h].used = 1; tab[h].k = *k; tab[h].cnt = 1; tab[h].minW = W; memcpy(tab[h].G, G, ng * sizeof(int)); tn++;
}
static void grow(void){ long os = tsz; Ent *ot = tab; tsz = os ? 2 * os : (1L << 16); tab = calloc(tsz, sizeof(Ent)); tn = 0;
  for (long i = 0; i < os; i++) if (ot[i].used){ uint64_t h = hk(&ot[i].k) & (tsz - 1); while (tab[h].used) h = (h + 1) & (tsz - 1); tab[h] = ot[i]; tn++; }
  free(ot); }
int main(int argc, char **argv){
  if (argc < 7){ fprintf(stderr, "usage: ./enumh4 m e K part nparts outfile\n"); return 1; }
  int m = atoi(argv[1]), e = atoi(argv[2]), K = atoi(argv[3]), part = atoi(argv[4]), np = atoi(argv[5]); int d = e - 1;
  if (m > MAXM || d < 1 || d > 7 || 3 * e >= m) { fprintf(stderr, "bad parameters\n"); return 1; }
  int pid[MAXM][MAXM]; int npairs = 0;
  for (int i = 1; i < m; i++) for (int j = i; j < m; j++) pid[i][j] = ((i + j) % m) ? npairs++ : -1;
  if (npairs > 256) return 1;
  int s[8], kk[8]; long ncomb = 0, ncand = 0, nS = 0; long minW = 1L << 60; int minWG[8] = {0};
  int lim = (K + 1) * m;
  for (int i = 0; i < d; i++) s[i] = i + 1;
  while (1){
    if (ncomb++ % np == part){
      for (int i = 0; i < d; i++) kk[i] = 1;
      while (1){
        ncand++;
        /* Apery set by Dijkstra on residues, aborting when an element reaches (K+1)m */
        int w[MAXM], done[MAXM], G[8]; for (int x = 0; x < m; x++){ w[x] = 1 << 29; done[x] = 0; } w[0] = 0;
        for (int b = 0; b < d; b++) G[b] = m * kk[b] + s[b];
        int ok = 1;
        for (int it = 0; it < m; it++){
          int u = -1; for (int x = 0; x < m; x++) if (!done[x] && (u < 0 || w[x] < w[u])) u = x;
          if (w[u] >= lim){ ok = 0; break; }
          done[u] = 1;
          for (int b = 0; b < d; b++){ int v = w[u] + G[b], t = v % m; if (v < w[t]) w[t] = v; }
        }
        if (ok){
          /* minimality of every chosen generator */
          for (int b = 0; b < d && ok; b++) if (w[s[b]] != G[b]) ok = 0;
          int isgen[MAXM] = {0}; for (int b = 0; b < d; b++) isgen[s[b]] = 1;
          Key key; memset(&key, 0, sizeof key); int h4 = 0;
          if (ok){
            for (int i = 1; i < m && ok; i++) for (int j = i; j < m; j++){
              int t = (i + j) % m; if (!t) continue;
              if (w[i] + w[j] == w[t]){ if (isgen[t]){ ok = 0; break; }
                int p = pid[i][j]; key.b[p >> 6] |= 1ULL << (p & 63); if (!isgen[i] && !isgen[j]) h4 = 1; }
            }
          }
          if (ok){
            int r = 0; for (int x = 1; x < m; x++) if (w[x] > w[r]) r = x;
            long c = w[r] - m + 1;
            if (c >= 4L * m + 1 && h4){
              long g = 0; for (int x = 1; x < m; x++) g += w[x] / m;
              long W = (long)e * (c - g) - c; nS++;
              if (W < minW){ minW = W; memcpy(minWG, G, sizeof G); }
              key.r = (uint8_t)r; key.q = (uint8_t)(w[r] / m); ins(&key, W, G, d);
            }
          }
        }
        int i = d - 1; while (i >= 0 && kk[i] == K){ kk[i] = 1; i--; } if (i < 0) break; kk[i]++;
      }
    }
    int i = d - 1; while (i >= 0 && s[i] == m - d + i) i--; if (i < 0) break; s[i]++; for (int j = i + 1; j < d; j++) s[j] = s[j - 1] + 1;
  }
  FILE *f = fopen(argv[6], "w");
  for (long i = 0; i < tsz; i++) if (tab[i].used){
    Ent *E = &tab[i]; fprintf(f, "%d %d", E->k.r, E->k.q);
    for (int x = 0; x < 4; x++) fprintf(f, " %016llx", (unsigned long long)E->k.b[x]);
    fprintf(f, " | %ld %ld |", E->cnt, E->minW); fprintf(f, " %d", m); for (int b = 0; b < d; b++) fprintf(f, " %d", E->G[b]); fprintf(f, "\n"); }
  fclose(f);
  printf("m=%d e=%d K=%d part=%d/%d candidates=%ld S_in_domain=%ld distinct_keys=%ld minW=%ld at <%d", m, e, K, part, np, ncand, nS, tn, minW, m);
  for (int b = 0; b < d; b++) printf(",%d", minWG[b]); printf(">\n");
  return 0;
}
