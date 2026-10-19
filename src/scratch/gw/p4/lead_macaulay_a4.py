# Lead's independent check of the a=4 stability table (P4_REPORT sec. 12): for q2=0..10,
# min over 0<=u<=q2^{<2>} (and u<=20) of 5*q2+5*u-4*min(u^{<3>},35); Macaulay upper operator h^{<j>}.
from math import comb
def macaulay_upper(h, j):
    # j-binomial expansion h = C(a_j,j)+C(a_{j-1},j-1)+..., return sum C(a_i+1,i+1)
    res = 0; i = j
    while h > 0 and i > 0:
        a = i
        while comb(a+1, i) <= h: a += 1
        res += comb(a+1, i+1); h -= comb(a, i); i -= 1
    return res
# sanity: in 4 variables h_1=4 -> h_2<=10
assert macaulay_upper(4,1)==10 and macaulay_upper(10,2)==20 and macaulay_upper(20,3)==35
row=[]
for q2 in range(11):
    best=None
    for u in range(0, min(macaulay_upper(q2,2),20)+1):
        k=min(macaulay_upper(u,3),35)
        val=5*q2+5*u-4*k
        best=val if best is None else min(best,val)
    row.append(best)
print("minima:", row)
print("report:", [0,5,10,15,20,24,20,25,29,25,10])
# brute-force the six negative profiles with r=0 (all ten AA present): WA=-10+5(q2+u3)-4k+4t, t=20-u3-u4>=0
neg=[]
for q2 in range(11):
    for u3 in range(0,min(macaulay_upper(q2,2),20)+1):
        for k in range(0,min(macaulay_upper(u3,3),35)+1):
            for t in range(0,20-u3+1):
                WA=-10+5*(q2+u3)-4*k+4*t
                if WA<0: neg.append((q2,10-q2,u3,20-u3-t,k,WA))
print("negative profiles (q2,q3,u3,u4,k,WA):", neg)
