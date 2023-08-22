import random
from gcd import *
from petlib.bn import Bn 

def shanks_dlp(a, b, p):
    # find x s.t a^x = b (mod p) if it exists

    if not isinstance(a, Bn):
        a = Bn(a)
    if not isinstance(b, Bn):
        b = Bn(b)
    if not isinstance(p, Bn):
        p = Bn(p)

    # k = random.randrange(5, 1000)
    k = 1000
    # k = p.random()
    base_powers = [ a.mod_pow(i, p) for i in range(1, k) ]
    
    for i in range(1, k):
        num = b.mod_mul( ( a.mod_pow(k*i, p).mod_inverse(p) ), p)  
        if num in base_powers:
            base_power = base_powers.index(num) + 1
            inv_power  = i*k
            return base_power + inv_power
    
    return None


def main():

    # a = (Bn(2)**Bn(48)).random()
    # x = (Bn(2)**Bn(8)).random()
    # p = Bn.get_prime(bits=48, safe=0)

    a = Bn(45)
    x = Bn(5)
    p = Bn(43)
    res = a.mod_pow(x, p)
    print(a)
    print(f"X: {x}")
    print(p)
    print(res)
    print(shanks_dlp(a, res, p))

if __name__ == "__main__":
    main()