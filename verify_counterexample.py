"""Exact certificate for the length-14 counterexample to two-state word separation.
Run: python verify_counterexample.py
Dependencies: numpy, sympy. No numerical optimization or floating-point comparisons.
The counterexample's analytic proof does not depend on this program.
"""
import itertools
import math
import random
import numpy as np
import sympy as sp

U = 'abbabaabbababa'
V = 'bababaabbabaab'

# Verification 1. Symbolic trace via the basis I,A,B,AB and Cayley-Hamilton.
x,y,z = sp.symbols('x y z')

def right(vec, c):
    p,q,r,t = vec
    if c.lower() == 'a':
        w = [-q+(z-x*y)*r-y*t,p+x*q+y*r+z*t,x*r+t,-r]
    else:
        w = [-r,-t,p+y*r,q+y*t]
    if c.isupper():
        w = [(x if c=='A' else y)*a-b for a,b in zip(vec,w)]
    return [sp.expand(a) for a in w]

def trace_word(w):
    vec = [1,0,0,0]
    for c in w:
        vec = right(vec,c)
    return sp.expand(2*vec[0]+x*vec[1]+y*vec[2]+z*vec[3])

h = x*x-x*y*z+y*y
t = z*z
expected = 2-t*(t-1)**2*h*(h-1)**2*(4-h-t)
assert U != V and len(U)==len(V)==14 and U.count('a')==V.count('a')==7
assert sp.expand(trace_word(U[::-1].upper()+V)-expected)==0
assert expected.subs({x:sp.sqrt(3),y:0,z:sp.Rational(1,2)})==sp.Rational(47,64)
print('PASS: exact symbolic trace factorization and attaining trace 47/64.')

# Verification 2. Enumerate equal-composition, prefix/suffix-trimmed pairs.
# For each pair, either an exact dihedral criterion or an exact integer
# quaternion inner product <= 0 certifies a trace zero by continuity.
# An integer quaternion q represents q/||q||; normalization is positive.
# With all sample squared norms <= 13 and n <= 14, all signed int64
# operations are exact: product coordinate dot sums <= 13**14 < 2**63.
assert 13**14 < 2**63

def mul(q,p):
    a,b,c,d=np.moveaxis(q,-1,0); e,f,g,h=np.moveaxis(p,-1,0)
    return np.stack((a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
                     a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e),axis=-1)

def vals(n,A,B):
    v=np.array([[1,0,0,0]],dtype=np.int64)
    for _ in range(n):
        v=np.concatenate((mul(v,A),mul(v,B)),axis=0)
    return v

def word(i,n):
    return ''.join('b' if i>>j&1 else 'a' for j in range(n))

def dihedral_signature(i,n):
    e=[0,0];counts=[0,0];stack=[]
    for j in range(n):
        b=i>>j&1
        e[b]+=(-1)**counts[1-b]
        counts[b]+=1
        if stack and stack[-1]==b:stack.pop()
        else:stack.append(b)
    return (e[0],e[1],tuple(stack))

# A,B axes in a common plane (sufficient, up to simultaneous conjugacy).
As=[(a,b,0,0) for a in range(4) for b in range(1,4)
    if math.gcd(a,b)==1 and a*a+b*b<=13]
Bs=[(a,b,c,0) for a in range(4) for b in range(-3,4) for c in range(1,4)
    if a*a+b*b+c*c<=13 and math.gcd(math.gcd(a,b),c)==1]
points=list(itertools.product(As,Bs))
random.Random(42).shuffle(points)

def run(n):
    N=1<<n
    words=np.arange(N,dtype=np.int32)
    counts=np.array([i.bit_count() for i in range(N)])
    blocks=[];total=0
    # Index LSB is first letter. By exchanging u and v, we can set
    # u first=a, v first=b. Their last letters also differ after trimming.
    for k in range(1,n):
        for end in (0,1):
            us=words[(words&1==0)&(words>>(n-1)==end)&(counts==k)]
            vs=words[(words&1==1)&(words>>(n-1)==1-end)&(counts==k)]
            if len(us) and len(vs):
                total+=len(us)*len(vs)
                blocks.append((np.repeat(us,len(vs)),np.tile(vs,len(us))))
    I=np.concatenate([p for p,q in blocks]); J=np.concatenate([q for p,q in blocks])
    assert len(I)==total
    sigs=[dihedral_signature(i,n) for i in range(N)]
    sig_ids={s:i for i,s in enumerate(set(sigs))}
    sig=np.array([sig_ids[s] for s in sigs]);keep=sig[I]==sig[J]
    I=I[keep];J=J[keep];after=len(I)
    for A,B in points:
        if not len(I):break
        Q=vals(n,np.array(A),np.array(B))
        dots=np.sum(Q[I]*Q[J],axis=1)
        keep=dots>0
        I=I[keep];J=J[keep]
    print(f'n={n:2d} trimmed pairs={total:8d}, after dihedral={after:6d}, remaining={len(I)}')
    return total,[(word(i,n),word(j,n)) for i,j in zip(I,J)]

count=0
for n in range(2,14):
    total,remaining=run(n)
    count+=total
    assert not remaining
assert count==1622259
print('PASS: every distinct binary pair of maximum length <=13 is exactly separable.')

# Optional classification at length 14, up to exchange of words and trimming.
_,remaining=run(14)
# Four survivors have the same exact positive trace polynomial. The fifth
# is resolved by a larger integer-quaternion point (Python arbitrary ints).
def qmul(q,p):
    a,b,c,d=q;e,f,g,h=p
    return (a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)
def eval_q(w,A,B):
    q=(1,0,0,0)
    for c in w:q=qmul(q,A if c=='a' else B)
    return q

unseparable=[]
for u,v in remaining:
    if u=='aaaaaaaaaaaabb' and v=='bbaaaaaaaaaaaa':
        A=(5,7,0,0);B=(15,11,23,0)
        assert sum(a*b for a,b in zip(eval_q(u,A,B),eval_q(v,A,B)))<0
    else:
        assert sp.expand(trace_word(u[::-1].upper()+v)-expected)==0
        unseparable.append((u,v))
assert len(unseparable)==4
print('PASS: precisely four unordered inseparable binary pairs at length 14:')
for u,v in unseparable:print(u,v)
