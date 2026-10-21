/* Near-perfect height-3 residue covers (lead, 2026-10-20).
   For d residues 0 < s_1 < ... < s_d < m: the cells z of Delta_2 (|z| <= 2, including 0) have distinct residues
   z.s mod m, and the cells of Delta_3 cover Z/m.  Prints every such s (the number of missing cubics is C(d+3,3) - m).
   usage: nearcov d m */
#include <stdio.h>
#include <stdlib.h>
int d, m, s[8], cnt;
void test(void) {
    static int seen[256]; int k, a, b, c, n2 = 0, cov = 0;
    for (k = 0; k < m; k++) seen[k] = 0;
    seen[0] = 1; cov = 1;
    for (a = 0; a < d; a++) { int r = s[a] % m; if (seen[r]) return; seen[r] = 1; cov++; }
    for (a = 0; a < d; a++) for (b = a; b < d; b++) { int r = (s[a] + s[b]) % m; if (seen[r]) return; seen[r] = 1; cov++; }
    for (a = 0; a < d; a++) for (b = a; b < d; b++) for (c = b; c < d; c++) {
        int r = (s[a] + s[b] + s[c]) % m; if (!seen[r]) { seen[r] = 2; cov++; } }
    if (cov < m) return;
    cnt++;
    printf("m=%d d=%d s=", m, d); for (k = 0; k < d; k++) printf("%d%c", s[k], k < d - 1 ? ',' : '\n');
    (void)n2;
}
void rec(int i, int lo) {
    if (i == d) { test(); return; }
    for (int v = lo; v < m; v++) { s[i] = v; rec(i + 1, v + 1); }
}
int main(int argc, char **argv) {
    d = atoi(argv[1]); m = atoi(argv[2]); rec(0, 1);
    fprintf(stderr, "d=%d m=%d covers=%d\n", d, m, cnt); return 0;
}
