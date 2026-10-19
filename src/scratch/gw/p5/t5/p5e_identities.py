"""Exact P5e identities. Execute only on fejer; no sympy required."""
from fractions import Fraction as F
from uniform_identities import P,v,check,checks,C2,C3
al=v['alpha']; tt=v['ly']; uu=v['u0']; ww=tt+uu
Q=C2(al+1); U=C3(al+2)
y=2*al*tt/9; xx=2*al*uu
aa=2*al+1+6*y+xx; ep=Q*y
nu=aa/2+2*al/3+F(5,6)+3*y/2
B0=(aa-2*al-1)*Q+2*U+2*al-aa+1
actual=nu**3-nu**2+2*nu-9*B0-67*ep+10
gg=ww**3+5*ww**2-F(46,9)*ww+F(44,27)
hh=3*ww**2-F(31,9)*ww-F(2,3)
cert=al**2*((al-4)*gg+4*gg+hh)+F(40,9)*(al**3+al**2)*uu+al*(F(16,9)+F(50,3)*tt+F(68,3)*uu)+F(358,27)
check('P47 full B-free identity',actual,cert)
check('P47 cubic positive certificate',gg,ww**3+5*(ww-F(23,45))**2+F(131,405))
check('P47 alpha4 positive certificate',4*gg+hh,4*ww*(ww-F(1,2))**2+27*(ww-F(112,243))**2+F(254,2187))
aq=v['a'];dd=v['n']
check('fixed-alpha endpoint',aq**2/8-aq*(Q/4+F(1,4))-9*Q+1,
      (aq-(2*Q+38))*(aq/8+F(9,2))+172)
j=v['j'];rr=v['r'];base=C2(j+1)
check('general gap block right endpoint',(aq-j)*base+(aq+2)*j-3*C2(j+1),
      (aq-j-1)*C2(j+2)+3*j+1-aq)
jj=aq-1;ss=aq-rr
check('general gap last block',(aq-jj)*C2(jj+1)+(aq+2)*ss-3*C2(ss+1),rr*(4*aq-3*rr-1)/2)
assert F(3135,8192)>F(1,3)
assert F(4913,24576)<F(1,5)
assert F(17,512)<F(1,30)
assert F(13,72*256)<F(1,60)
aa=v['a'];A=v['alpha'];ee=v['R'];cc=v['c0'];uu=v['u0'];kk=v['k0'];D=v['D3']
qq=C2(A+1);CH=A+qq+cc+ee+C3(ee+2)+(qq+A*ee)*(aa-A)
lower=aa+(aa+3)*qq+(aa+1)*uu-3*kk+D
upper=2*CH-aa-(aa+3)*qq-(aa+1)*uu+5*kk-D
check('LOW-H(E) exact difference',lower-3*upper,
  4*aa-6*A+(6*A+6-2*aa)*qq-6*cc+4*(aa+1)*uu-18*kk+4*D-6*ee*(1+A*(aa-A))-6*C3(ee+2))
print({'new_checks':checks[-7:],'all_checks':len(checks),'large_a_constants':'exact fractions verified'})
