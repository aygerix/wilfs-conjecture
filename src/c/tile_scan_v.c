/* tile_scan_v.c (2026-10-18): src/c/tile_scan.c with two changes, written by the e = 4 chain referee and adopted by the lead.
 *  (1) coordinate type CT (default uint8_t; build with -DCT=uint16_t for m >= 256: with uint8_t, any coordinate 256 wraps
 *      silently, so tiles can be lost or corrupted when m >= 257) and MAXM settable with -DMAXM=...;
 *  (2) completeness certificate: per lattice, the doubled areas of all traversed cone polygons (projected to the simplex
 *      x+y+z = 1) are summed mod 2^61-1. Cones of distinct tiles are disjoint and the fan covers the simplex, so the
 *      traversal found every tile iff the exact sum is 1; 'AREACHECK ... area-defects 0' reports it (a mod-p check: a
 *      wrong exact sum is missed only if it is congruent to 1 mod 2^61-1). LATSTEP=k env: only every k-th lattice.
 * Build: cc -O2 -DMAXM=300 -DCT=uint16_t -o tsv16 tile_scan_v.c -lpthread -lm */
/* tile_scan.c: C port of src/scratch/tile_scan_HM.py (complete scan of non-two-face 3-D Apery tiles, e = 4).
 * Same enumeration as src/tile_enum.py (Groebner-fan flip traversal over the positive weight simplex, one lattice
 * Lam_r per canonical residue triple), same statistics:
 *   HT:     H(D) >= m-1         (H as in src/scratch/heightH.py)
 *   MAXSUM: M3 = sum_{y in Max(D)} (|y|+3) <= 2m+1   (as in src/scratch/tile_maxsum.py)
 * Differences from the Python, all exact (no floating point anywhere):
 *  - cone polygons are kept as cyclic lists of integer constraint normals (vertex = cross product of neighbours),
 *    so all arithmetic is in int64 instead of Fractions;
 *  - a flip across edge E (normal n, midpoint q) computes the tile of q + eps*(-n) for infinitesimal eps by the
 *    lexicographic monomial order (q.x, -n.x, |x|, lex x) instead of halving a rational eps.  The Groebner fan
 *    restricted to the positive orthant is a polyhedral fan, so q lies in the relative interior of exactly one edge of
 *    exactly one neighbouring cell and this lands in it; it is still checked that q is in the closure of the new cone;
 *  - lattices are processed in parallel (pthreads), results are reduced in the Python's lattice order.
 * HT failures are NOT LP-certified here (tile_lp.py needs the cone polygon); they are printed as HT-fail lines with
 * the tile so they can be certified in Python.  'LP-pending' counts them.
 * usage: tile_scan m0 m1 [threads] [M]      (M = MAXSUM only, skip H) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <stdatomic.h>
#include <time.h>

typedef int64_t i64;
#ifndef MAXM
#define MAXM 255
#endif
#ifndef CT
#define CT uint8_t
#endif
#define MAXC (3*MAXM + 8)

static int M, MONLY;
#define PMOD 2305843009213693951ULL  /* 2^61 - 1 */
static uint64_t mulm(uint64_t a, uint64_t b) { return (uint64_t)(((unsigned __int128)a * b) % PMOD); }
static uint64_t powm(uint64_t a, uint64_t e) { uint64_t r = 1; a %= PMOD; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static uint64_t modi(i64 x) { i64 r = x % (i64)PMOD; if (r < 0) r += PMOD; return (uint64_t)r; }
static int LATSTEP = 1;

static int (*LAT)[3]; static int NLAT;

typedef struct { i64 k1, k2; int deg; CT x[3]; } Key;
static int kcmp(const Key *a, const Key *b) {
    if (a->k1 != b->k1) return a->k1 < b->k1 ? -1 : 1;
    if (a->k2 != b->k2) return a->k2 < b->k2 ? -1 : 1;
    if (a->deg != b->deg) return a->deg < b->deg ? -1 : 1;
    for (int i = 0; i < 3; i++) if (a->x[i] != b->x[i]) return a->x[i] < b->x[i] ? -1 : 1;
    return 0;
}

/* tile (class g -> exponent T[3g..3g+2]) of the monomial order (p1.x, p2.x, |x|, lex x) on Z^3 / Lam_r */
static void tile_for(const int *r, const i64 *p1, const i64 *p2, CT *T) {
    int m = M; Key best[MAXM]; char have[MAXM], done[MAXM];
    struct { Key k; int g; } heap[3*MAXM + 4]; int hn = 0;
    memset(have, 0, m); memset(done, 0, m);
    Key z = {0, 0, 0, {0, 0, 0}}; best[0] = z; have[0] = 1;
    heap[hn].k = z; heap[hn].g = 0; hn++;
    while (hn) {
        Key k = heap[0].k; int g = heap[0].g;
        hn--; { int i = 0; for (;;) { int c = 2*i + 1; if (c >= hn) break;
            if (c + 1 < hn && kcmp(&heap[c+1].k, &heap[c].k) < 0) c++;
            if (kcmp(&heap[hn].k, &heap[c].k) <= 0) break; heap[i] = heap[c]; i = c; } heap[i] = heap[hn]; }
        if (done[g]) continue;
        done[g] = 1; T[3*g] = k.x[0]; T[3*g+1] = k.x[1]; T[3*g+2] = k.x[2];
        for (int a = 0; a < 3; a++) {
            int h = (g + r[a]) % m; if (done[h]) continue;
            Key k2 = k; k2.k1 += p1[a]; k2.k2 += p2[a]; k2.deg++; k2.x[a]++;
            if (!have[h] || kcmp(&k2, &best[h]) < 0) {
                best[h] = k2; have[h] = 1;
                int i = hn++; while (i) { int pa = (i - 1)/2; if (kcmp(&heap[pa].k, &k2) <= 0) break; heap[i] = heap[pa]; i = pa; }
                heap[i].k = k2; heap[i].g = h;
            }
        }
    }
}

static inline int cls(const int *r, int a, int b, int c) { return (int)(((i64)r[0]*a + (i64)r[1]*b + (i64)r[2]*c) % M); }
static inline int inD(const CT *T, const int *r, int a, int b, int c) {
    if (a < 0 || b < 0 || c < 0) return 0;
    int g = cls(r, a, b, c); return T[3*g] == a && T[3*g+1] == b && T[3*g+2] == c;
}

/* cone constraints: v = q - rep(q) over minimal non-elements q;  cone = {p : p.v > 0} */
static int constraints(const int *r, const CT *T, i64 (*V)[3]) {
    int n = 0;
    for (int g = 0; g < M; g++) for (int a = 0; a < 3; a++) {
        int q[3] = {T[3*g], T[3*g+1], T[3*g+2]}; q[a]++;
        int skip = 0; for (int b = 0; b < a; b++) if (q[b]) skip = 1;   /* generate each q once */
        if (skip || inD(T, r, q[0], q[1], q[2])) continue;
        int ok = 1;
        for (int b = 0; b < 3 && ok; b++) if (q[b]) { q[b]--; ok = inD(T, r, q[0], q[1], q[2]); q[b]++; }
        if (!ok) continue;
        int h = cls(r, q[0], q[1], q[2]);
        for (int i = 0; i < 3; i++) V[n][i] = q[i] - T[3*h+i];
        n++;
    }
    return n;
}

static void cross(const i64 *a, const i64 *b, i64 *o) {
    o[0] = a[1]*b[2] - a[2]*b[1]; o[1] = a[2]*b[0] - a[0]*b[2]; o[2] = a[0]*b[1] - a[1]*b[0];
    if (o[0] + o[1] + o[2] < 0) { o[0] = -o[0]; o[1] = -o[1]; o[2] = -o[2]; }
}
static inline i64 dot(const i64 *a, const i64 *b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; }

/* polygon = cyclic list of normals P[0..k-1]; vertex j = P[j] x P[j+1].  Returns k, or -1 if degenerate. */
static int cone_polygon(i64 (*V)[3], int nv, i64 (*P)[3]) {
    i64 Q[MAXC][3]; int k = 3;
    memset(P, 0, sizeof(i64)*9); P[0][0] = P[1][1] = P[2][2] = 1;
    for (int c = 0; c < nv; c++) {
        i64 d[MAXC]; int neg = 0, pos = 0;
        for (int j = 0; j < k; j++) { i64 X[3]; cross(P[j], P[(j+1) % k], X); d[j] = dot(V[c], X); neg |= d[j] < 0; pos |= d[j] > 0; }
        if (!neg) continue;
        if (!pos) return -1;
        char surv[MAXC]; int j0 = -1;
        for (int j = 0; j < k; j++) { surv[j] = d[(j + k - 1) % k] > 0 || d[j] > 0; if (surv[j] && j0 < 0) j0 = j; }
        int nk = 0;
        for (int t = 0; t < k; t++) {
            int j = (j0 + t) % k; if (!surv[j]) continue;
            memcpy(Q[nk++], P[j], sizeof(i64)*3);
            if (!(surv[(j+1) % k] && d[j] >= 0)) memcpy(Q[nk++], V[c], sizeof(i64)*3);
        }
        k = nk; memcpy(P, Q, sizeof(i64)*3*k);
        if (k > MAXC - 4) { fprintf(stderr, "polygon too large\n"); exit(2); }
    }
    return k;
}

/* ---- per-lattice hash set of tiles ---- */
typedef struct { CT *arena; int n, cap; int *tab; int tcap; } TSet;
static uint64_t thash(const CT *T) { uint64_t h = 1469598103934665603ULL; for (int i = 0; i < 3*M; i++) { h ^= T[i]; h *= 1099511628211ULL; } return h; }
static int tset_add(TSet *s, const CT *T) {   /* returns 1 if new */
    if (2*(s->n + 1) > s->tcap) {
        int nc = s->tcap ? 2*s->tcap : 1024; int *nt = malloc(sizeof(int)*nc); memset(nt, -1, sizeof(int)*nc);
        for (int i = 0; i < s->n; i++) { uint64_t h = thash(s->arena + (size_t)3*M*i) & (nc - 1); while (nt[h] >= 0) h = (h + 1) & (nc - 1); nt[h] = i; }
        free(s->tab); s->tab = nt; s->tcap = nc;
    }
    uint64_t h = thash(T) & (s->tcap - 1);
    while (s->tab[h] >= 0) { if (!memcmp(s->arena + (size_t)3*M*s->tab[h], T, 3*M*sizeof(CT))) return 0; h = (h + 1) & (s->tcap - 1); }
    if (s->n == s->cap) { s->cap = s->cap ? 2*s->cap : 256; s->arena = realloc(s->arena, (size_t)3*M*s->cap*sizeof(CT)); }
    memcpy(s->arena + (size_t)3*M*s->n, T, 3*M*sizeof(CT)); s->tab[h] = s->n++;
    return 1;
}

typedef struct {
    long long n, nn, fails, msbad; int have; i64 worst; i64 wms; int wk; uint64_t area; int done;
    char *failtxt; size_t failsz;
} Res;
static Res *RES;

static void stats(const int *r, const CT *T, Res *R) {
    int m = M;
    R->n++;
    for (int a = 0; a < 3; a++) for (int b = a + 1; b < 3; b++) {
        int v[3] = {0, 0, 0}; v[a] = v[b] = 1; if (!inD(T, r, v[0], v[1], v[2])) return;
    }
    R->nn++;
    int ord[MAXM], cnt[3*MAXM + 2] = {0}, deg[MAXM];
    for (int g = 0; g < m; g++) { deg[g] = T[3*g] + T[3*g+1] + T[3*g+2]; cnt[deg[g]]++; }
    for (int d = 3*MAXM; d >= 0; d--) cnt[d] += cnt[d+1];
    for (int g = 0; g < m; g++) ord[--cnt[deg[g]]] = g;          /* ord[0..] by decreasing degree */
    int ht[MAXM], top[3][MAXM]; i64 M3 = 0; int nmax = 0;
    for (int t = 0; t < m; t++) {
        int g = ord[t], best = 0;
        for (int i = 0; i < 3; i++) {
            int h = (g + r[i]) % m;
            int in = T[3*h] == T[3*g] + (i == 0) && T[3*h+1] == T[3*g+1] + (i == 1) && T[3*h+2] == T[3*g+2] + (i == 2);
            if (in) { if (ht[h] + 1 > best) best = ht[h] + 1; top[i][g] = top[i][h]; } else top[i][g] = g;
        }
        ht[g] = best;
        if (!best) { M3 += deg[g] + 3; nmax++; }
    }
    i64 ms = 2*m + 1 - M3;
    if (ms < 0) R->msbad++;
    if (!R->have || ms < R->wms) { R->wms = ms; R->wk = nmax; }
    if (MONLY) { R->have = 1; return; }
    i64 H = 0; for (int g = 0; g < m; g++) for (int i = 0; i < 3; i++) H += ht[top[i][g]];
    i64 sl = H - (m - 1);
    if (sl < 0) {
        R->fails++;
        char buf[16384]; int p = snprintf(buf, sizeof buf, "    HT-fail (LP-pending) (%lld, (%d, %d, %d)) D=", (long long)sl, r[0], r[1], r[2]);
        for (int g = 0; g < m && p < (int)sizeof buf - 40; g++) p += snprintf(buf + p, sizeof buf - p, "(%d,%d,%d)", T[3*g], T[3*g+1], T[3*g+2]);
        p += snprintf(buf + p, sizeof buf - p, "\n");
        R->failtxt = realloc(R->failtxt, R->failsz + p + 1); memcpy(R->failtxt + R->failsz, buf, p + 1); R->failsz += p;
    }
    if (!R->have || sl < R->worst) R->worst = sl;
    R->have = 1;
}

static void do_lattice(int li) {
    const int *r = LAT[li]; int m = M; Res *R = &RES[li];
    if (li % LATSTEP) return; R->done = 1;
    TSet S = {0}; size_t TS = 3*m*sizeof(CT);
    static const i64 start[3] = {1998998, 1995992, 1984013}, zero[3] = {0, 0, 0};  /* = Python's start point * 5979003 */
    CT *T = malloc(TS), *T2 = malloc(TS);
    int scap = 1024, sn = 0; unsigned char *stack = malloc(TS*scap);
    i64 (*V)[3] = malloc(sizeof(i64)*3*MAXC), (*V2)[3] = malloc(sizeof(i64)*3*MAXC), (*P)[3] = malloc(sizeof(i64)*3*MAXC);
    tile_for(r, start, zero, T); memcpy(stack, T, TS); sn = 1;
    while (sn) {
        memcpy(T, stack + TS*(--sn), TS);
        if (!tset_add(&S, T)) continue;
        int nv = constraints(r, T, V), k = cone_polygon(V, nv, P);
        if (k < 3) { fprintf(stderr, "degenerate cone m=%d r=(%d,%d,%d)\n", m, r[0], r[1], r[2]); exit(3); }
        stats(r, T, R);
        i64 X[MAXC][3], s[MAXC];
        for (int j = 0; j < k; j++) { cross(P[j], P[(j+1) % k], X[j]); s[j] = X[j][0] + X[j][1] + X[j][2]; }
        { long double sa = 0; uint64_t am = 0;
          for (int j = 0; j < k; j++) { int jn = (j + 1) % k;
            long double xj = (long double)X[j][0]/s[j], yj = (long double)X[j][1]/s[j], xn = (long double)X[jn][0]/s[jn], yn = (long double)X[jn][1]/s[jn];
            sa += xj*yn - xn*yj;
            i64 det = X[j][0]*X[jn][1] - X[jn][0]*X[j][1];
            uint64_t den = mulm(modi(s[j]), modi(s[jn]));
            am = (am + mulm(modi(det), powm(den, PMOD - 2))) % PMOD; }
          if (sa < 0) am = (PMOD - am) % PMOD;
          R->area = (R->area + am) % PMOD; }
        for (int j = 0; j < k; j++) {          /* edge j: normal P[j], endpoints X[j-1], X[j] */
            int jp = (j + k - 1) % k; i64 mid[3], neg[3];
            for (int i = 0; i < 3; i++) { mid[i] = X[jp][i]*s[j] + X[j][i]*s[jp]; neg[i] = -P[j][i]; }
            if (!mid[0] || !mid[1] || !mid[2]) continue;               /* boundary of the positive simplex */
            tile_for(r, mid, neg, T2);
            if (!memcmp(T, T2, TS)) { fprintf(stderr, "flip stayed inside m=%d\n", m); exit(4); }
            int nv2 = constraints(r, T2, V2);
            for (int c = 0; c < nv2; c++) if (dot(V2[c], mid) < 0) { fprintf(stderr, "flip missed closure m=%d\n", m); exit(5); }
            if (sn == scap) { scap *= 2; stack = realloc(stack, TS*scap); }
            memcpy(stack + TS*(sn++), T2, TS);
        }
    }
    free(S.arena); free(S.tab); free(T); free(T2); free(stack); free(V); free(V2); free(P);
}

static atomic_int NEXT;
static void *worker(void *u) { (void)u; int i; while ((i = atomic_fetch_add(&NEXT, 1)) < NLAT) do_lattice(i); return NULL; }

static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* canonical residues: sorted triple of distinct nonzero residues, gcd with m = 1, lexicographically minimal among
 * sorted(u * r mod m) over units u   (= tile_enum.canonical_residues, in the same sorted order) */
static void lattices(int m) {
    int units[MAXM], nu = 0; for (int u = 1; u < m; u++) if (gcd(u, m) == 1) units[nu++] = u;
    int cap = 1024; NLAT = 0; LAT = malloc(sizeof(int)*3*cap);
    for (int a = 1; a < m; a++) for (int b = a + 1; b < m; b++) for (int c = b + 1; c < m; c++) {
        if (gcd(gcd(gcd(a, b), c), m) != 1) continue;
        int canon = 1;
        for (int t = 0; t < nu && canon; t++) {
            int u = units[t], x = u*a % m, y = u*b % m, z = u*c % m, w;
            if (x > y) { w = x; x = y; y = w; } if (y > z) { w = y; y = z; z = w; } if (x > y) { w = x; x = y; y = w; }
            if (x < a || (x == a && (y < b || (y == b && z < c)))) canon = 0;
        }
        if (!canon) continue;
        if (NLAT == cap) { cap *= 2; LAT = realloc(LAT, sizeof(int)*3*cap); }
        LAT[NLAT][0] = a; LAT[NLAT][1] = b; LAT[NLAT][2] = c; NLAT++;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: tile_scan m0 m1 [threads] [M]\n"); return 1; }
    int m0 = atoi(argv[1]), m1 = atoi(argv[2]), nth = argc > 3 ? atoi(argv[3]) : 1;
    MONLY = argc > 4 && argv[4][0] == 'M';
    if (getenv("LATSTEP")) LATSTEP = atoi(getenv("LATSTEP"));
    if (m1 > MAXM) { fprintf(stderr, "m <= %d\n", MAXM); return 1; }
    for (int m = m0; m <= m1; m++) {
        struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0);
        M = m; lattices(m); RES = calloc(NLAT, sizeof(Res));
        atomic_store(&NEXT, 0);
        pthread_t th[256]; if (nth > 256) nth = 256;
        for (int i = 0; i < nth; i++) pthread_create(&th[i], NULL, worker, NULL);
        for (int i = 0; i < nth; i++) pthread_join(th[i], NULL);
        long long n = 0, nn = 0, fails = 0, msbad = 0; int wi = -1, mi = -1;
        for (int i = 0; i < NLAT; i++) {
            Res *R = &RES[i]; n += R->n; nn += R->nn; fails += R->fails; msbad += R->msbad;
            if (!R->nn) continue;
            if (!MONLY && (wi < 0 || R->worst < RES[wi].worst)) wi = i;
            if (mi < 0 || R->wms < RES[mi].wms) mi = i;
        }
        { int bad = 0, nd = 0; for (int i = 0; i < NLAT; i++) if (RES[i].done) { nd++; if (RES[i].area != 1) { bad++; if (bad <= 3) fprintf(stdout, "AREA-DEFECT m=%d r=(%d,%d,%d)\n", m, LAT[i][0], LAT[i][1], LAT[i][2]); } }
          printf("AREACHECK m=%d lattices-checked %d area-defects %d\n", m, nd, bad); }
        clock_gettime(CLOCK_MONOTONIC, &t1);
        double el = (t1.tv_sec - t0.tv_sec) + 1e-9*(t1.tv_nsec - t0.tv_nsec);
        printf("m=%d: tiles %lld, non-two-face %lld, HT fails %lld, LP-pending %lld; min H-(m-1) ", m, n, nn, fails, fails);
        if (wi >= 0) printf("(%lld, (%d, %d, %d))", (long long)RES[wi].worst, LAT[wi][0], LAT[wi][1], LAT[wi][2]); else printf("None");
        printf("; MAXSUM fails %lld, min slack 2m+1-M3 ", msbad);
        if (mi >= 0) printf("(%lld, (%d, %d, %d), %d)", (long long)RES[mi].wms, LAT[mi][0], LAT[mi][1], LAT[mi][2], RES[mi].wk); else printf("None");
        printf(" [%.1fs, %d lattices, %d threads]\n", el, NLAT, nth);
        for (int i = 0; i < NLAT; i++) if (RES[i].failtxt) { fputs(RES[i].failtxt, stdout); free(RES[i].failtxt); }
        fflush(stdout);
        free(RES); free(LAT);
    }
    return 0;
}
