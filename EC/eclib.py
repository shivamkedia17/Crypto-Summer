from petlib.bn import Bn
from dataclasses import dataclass
from typing import *

# TODO 
# use a dataclass to wrap a point and refactor functions accordingly


def legendre(self, x, p):
    if not isinstance(x, Bn):
        x = Bn(x)
    if not isinstance(p, Bn):
        p = Bn(p)

    # assume p is prime
    return x.mod_pow((p-1)//2, p)

class EC():
    # pick a valid, random point from the curve
    def random_point(self):
        p = self.p
        while True:
            # pick a random x
            x = Bn.random(p)
            temp = (x.mod_pow(3, p) + x.mod_mul(self.a, p) + self.b) % p
            
            # check if x satisfies the equation
            if legendre(temp, p) == 1:
                # check if there exists a valid y such that (x,y) is a point on the curve
                for y in range(1, (p+1)//2):
                    y = Bn(y)
                    if y.mod_pow(2, p) == temp:
                        return (x, y)
    
    def find_point(self, x):
        p = self.p
        
        # y^2 = temp
        temp = (x.mod_pow(3, p) + x.mod_mul(self.a, p) + self.b) % p 

        # no such point exists
        if legendre(temp, p) != 1:
            return (None, None)
        # otherwise use Shank's algo
        else:
            # TODO 
            y = self.t_shanks(temp, p)

    
    '''
    Returns the modular square root of n if it exists, given prime modulus p
    '''
    def t_shanks(self, n, p):
        if legendre(n, p) != 1:
            raise ValueError("Given Number is a non-quadratic residue mod p.") 

        # factor out powers of two
        temp = p-1 
        while temp % temp:
            pass
        raise NotImplemented


    # Parameters of the Weierstrauss Equation y^2 = x^3 + ax + b (mod p): [p, a, b]
    def __init__(self, p: int | Bn, a: int | Bn, b: int | Bn) -> None:
        for param in (p, a, b):
            if not isinstance(param, Bn):
                param = Bn(param)

        # if ( 4*(a**3) + 27*(b**2) ) % p == 0:
        if ( a.mod_pow(3, p).mod_mul(4, p) + b.mod_pow(2, p).mod_mul(27, p) ) % p == 0:
            raise ValueError("Singular Elliptic Curve.")

        self.p = p
        self.a = a
        self.b = b
        self.zero = (-1, -1)

    def double_pt(self, x1, y1):
        p = self.p
        s = ((x1.mod_pow(2, p).mod_mul(3, p).mod_add(self.a, p))).mod_mul((y1.mod_mul(2, p)).mod_inverse(p), p)
        x = (s.mod_pow(2, p)).mod_sub(x1.mod_mul(2,p), p)
        y = s.mod_mul(x1.mod_sub(x, p), p).mod_sub(y1, p)
        return (x, y)

    def add_pt(self, x1, y1, x2, y2):
        p = self.p
        s = y2.mod_sub(y1,p).mod_mul(x2.mod_sub(x1, p).mod_inverse(p), p)
        x = (s.mod_pow(2, p)).mod_sub(x1.mod_add(x2, p), p)
        y = s.mod_mul(x1.mod_sub(x, p), p).mod_sub(y1, p)
        return (x, y)
    
    def add(self, x1, y1, x2, y2):
        if (x1, y1) is self.zero:
            return (x2, y2)
        if (x2, y2) is self.zero:
            return (x1, y1)

        if (x1 == x2) and (y1 == -y2):
            return self.zero
        elif (x1 == x2) and (y1 == y2):
            return self.double_pt(x1, y1)
        else:
            return self.add_pt(x1, y1, x2, y2)

    def negate(self, x, y):
        return self.zero if (x, y) is self.zero else (x, -y)

    def subtract(self, x1, y1, x2, y2):
        # (x1, y1) - (x2, y2)
        return self.add(x1, y1, *(self.negate(x2, y2)))

    def mult_pt(self, x1, y1, k):
        P = (x1, y1)

        if P is self.zero:
            return self.zero

        Q = P
        bit_vector = bin(k)[2:]
        for i in bit_vector:
            Q = self.double_pt(*Q)
            if i == '1':
                Q = self.add(*Q, *P)
        return Q

    def check_point(self, x, y):
        if not isinstance(x, Bn):
            x = Bn(x)
        if not isinstance(y, Bn):
            y = Bn(y)

        p = self.p
        temp = (x.mod_pow(3, p) + x.mod_mul(self.a, p) + self.b) % p

        return (y.mod_pow(2, p)) == temp

def main():
    pass

if __name__ == "__main__":
    main()
