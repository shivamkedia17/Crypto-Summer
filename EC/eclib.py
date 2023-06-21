from petlib.bn import Bn

class EC():
    def legendre(self, x):
        p = self.p
        return x.mod_pow((p-1)//2, p)
        # return (x.mod_pow(p-1, p).mod_mul(x.mod_pow(2, p).mod_inverse(p)))


    def find_point(self):
        p = self.p
        while True:
            x = Bn.random(p)
            temp = (x.mod_pow(3, p) + x.mod_mul(self.a, p) + self.b) % p
            if self.legendre(temp) == 1:
                for y in range(1, (p+1)//2):
                    y = Bn(y)
                    if y.mod_pow(2, p) == temp:
                        return (x, y)


    # Parameters of the Weierstrauss Equation y^2 = x^3 + ax + b (mod p)
    def __init__(self, p, a, b) -> None:
        self.p = p
        self.a = a
        self.b = b
        self.zero = (float('inf'), float('inf'))
        # self.points = self.find_points(self)

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


    def mult_pt(self, x1, y1, k):
        P = (x1, y1)
        Q = P
        bit_vector = bin(k)[2:]
        for i in bit_vector:
            Q = self.double_pt(*Q)
            if i == '1':
                Q = self.add(*Q, *P)
        return Q

# find points on an elliptic curve
if __name__ == "__main__":
    main()