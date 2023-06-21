from petlib.bn import Bn
from eclib import EC
'''
Creating the ElGamal Encryption based on delayed Diffie-Hellman Key Exchange using Elliptic Curves

Standrd Diffie Hellman using integers:
    - Everything is in the (mod p) world
    - A and B first pick a common random number G (which is public)
    - Then they seperately pick private a and b.
    - Alice's A = G^a (mod p ofc)
    - Bob's   B = G^b (mod p ofc)
    - They then exchange A and B so that Alice's B^a = K = Bob's A^b which is G^(ab) 
    
Standard ElGamal:
    - Instead of 'exchanging' A and B, Alice accidently perishes afer making (G, p, A) public
    - Bob manifests a while later, and is presented with whatever Alice made public
    - He then picks a random b in the mod p world and goes about similar business
'''

def main():
    # First we pick our standard p
    # p = Bn.get_prime(bits=100, safe=0)
    p = Bn.from_decimal("6277101735386680763835789423207666416083908700390324961279")
    n = Bn.from_decimal("6277101735386680763835789423176059013767194773182842284081")
    a = Bn.from_hex("64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1")
    b = Bn.from_hex("3099d2bbbfcb2538542dcd5fb078b6ef5f3d6fe2c745de65")
    Gx = Bn.from_hex("188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012")
    Gy = Bn.from_hex("07192b95ffc8da78631011ed6b24cdd573f977a11e794811")
    ec = EC(p, a, b)
    # ax, ay = ec.find_point()
    # bx, by = ec.find_point()
    ka = n.random()
    kb = n.random()

    A  = ec.mult_pt(Gx, Gy, ka)
    B  = ec.mult_pt(Gx, Gy, kb)
    K_Alice = ec.mult_pt(*B, ka)
    K_Bob   = ec.mult_pt(*A, kb)

    print("Alice's private Key = ", ka)
    print("Alice's public Key = ", A)
    print("Bob's private Key = ", kb)
    print("Bob's public Key = ", B)

    print("Alice's Key = ", K_Alice)
    print("Bob's Key = ", K_Bob)


if __name__ == "__main__":
    main()