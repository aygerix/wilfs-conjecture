from sympy import *
b,n,z,w,A,N=symbols('b n z w A N')
H=lambda x: x*(x*(x-1)/2+1)
print("B-SF0 expand", expand(H(b-2)-11*(b-2)**2))
f=expand(H(b-2)-11*(b-2)**2-Rational(3,8)*b**3)
print(" f(128)",f.subs(b,128), " f increasing beyond 128:", all(f.subs(b,x)>0 for x in range(128,3000)), solve(diff(f,b),b))
print(" (163/128)^3/6 =",Rational(163,128)**3/6, float(Rational(163,128)**3/6), "<7/20", Rational(163,128)**3/6<Rational(7,20))
print(" upper sum", float(Rational(163,128)**3/6+Rational(1,512)+Rational(1,256)), "< 3/8")
print(" lin-term check 320b+256<3b^2 at 128:", 320*128+256<3*128**2)
c10=Rational(1,2)*Rational(15,16)**3-Rational(131,2*384)-Rational(5,2*16**3)
print("B-SF10 lower coeff", c10, c10==Rational(2959,12288), c10>Rational(9,40))
print(" (137/128)^3/6", float(Rational(137,128)**3/6), Rational(137,128)**3/6<Rational(21,100))
print(" upper sum", float(Rational(21,100)+Rational(1,8*16**3)+Rational(1,2048)), "<", 9/40)
print(" lin check", 2048*(Rational(17,16)*384+1)/12 < 384**2)
print("B-RARE", Rational(2959,12288)-Rational(7,512), Rational(2959,12288)-Rational(7,512)==Rational(2791,12288), Rational(2791,12288)>Rational(9,40))
p1=Rational(46609,16000)*N**3-Rational(304927,800)*N**2+Rational(49,5)*N+2
p2=Rational(22599,16000)*N**3-Rational(304927,800)*N**2+Rational(49,5)*N+2
print("BASE polys positive from 480:", min(p1.subs(N,x) for x in range(480,2000))>0, min(p2.subs(N,x) for x in range(480,2000))>0, [float(r) for r in real_roots(Poly(p2*16000,N))])
print("MATCH", Rational(46609,16000)*480-Rational(1117739,800))
g=w**3+5*w**2-46*w/9+Rational(44,27)
print("g identity", simplify(g-(1+w**2)/4-(w**3+Rational(19,4)*(w-Rational(92,171))**2+Rational(29,6156)))==0)
q=A**3-1908*A**2-2240*A-896
print("BFREE-LIGHT", expand(q.subs(A,1910+z)), [float(r) for r in real_roots(Poly(q,A))])
q2=19*A**3-68708*A**2-80648*A-32256
print("BFREE-RARE", expand(q2.subs(A,3618+z)), [float(r) for r in real_roots(Poly(q2,A))])
