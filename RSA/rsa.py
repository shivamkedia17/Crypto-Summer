from petlib.bn import Bn
from gcd import modular_inverse, gcd

def main():
    bits = [4, 16, 64, 128, 256, 400, 511]

    rounds = 15
    for r in range(rounds):
        print(f"Round {r}:")
        print()
        for size in bits:
            tests, fails = test(size)
            print(f"n: {size*2 + 1} bits. {tests - fails} out of {tests} tests passed.")
        print()

def test(bits):
    # p = Bn.get_prime(41, 1)
    # q = Bn.get_prime(40, 1)
    # p = Bn.get_prime(511, 1)
    # q = Bn.get_prime(512, 1)
    # p = Bn(11)
    # q = Bn(23)

    try:
        p = Bn.get_prime(bits, 1)
    except Exception:
        p = Bn.get_prime(bits, 0)
    
    try:
        q = Bn.get_prime(bits+1, 1)
    except Exception:
        q = Bn.get_prime(bits+1, 0)
    
    

    n = p * q
    phi_n = (p-1) * (q-1)
    # print(f"p = {p}\nq = {q}\nn = {n}\nphi_n = {phi_n}")

    # print()

    e, d = None, None
        
    while d is None:
        e = Bn.random(n)
        d = modular_inverse(e, phi_n)

    # d = d.mod(n)

    # print(f"e = {e}\nd = {d}\n")
    assert(e.mod_mul(d, phi_n) == 1)

    # check if RSA works

    # '''
    tests = 20
    fails = 0
    for i in range(tests):
        M = Bn.random(n)
        # assert(M < n)

        ciphertext = encrypt(M, e, n)
        deciphered = decrypt(ciphertext, d, n)
        # print(f"Message: {M}\nEncrypted: {ciphertext}\nDecrypted: {deciphered}")

        try:
            assert(M == deciphered)
        except AssertionError:
            fails += 1
    
    return (tests, fails)
    # '''

    '''
    M = input("Enter your message: ")
    M = Bn(int.from_bytes(M.encode()))
    C = encrypt(M, e, n)
    print(f"Ciphertext: {C}")
    D = decrypt(C, d, n)
    assert(M == D)
    D = bytes.fromhex(hex(D)).decode()
    print(f"Decrypted: {D}")
    '''

def encrypt(M, e, n) -> Bn:
    """
    Encrypts a message M (encodes it if string is given), returns M^e (mod n)
    """

    if isinstance(M, int):
        M = Bn(M)
    elif not isinstance(M, Bn):
        raise TypeError
        
    try:
        assert(M < n)
    except AssertionError:
        print("Error: Given message is too large.")

    C = M.mod_pow(e, n) 
    return C

def decrypt(C: Bn, d: int | Bn, n: int | Bn) -> Bn:
    try:
        assert(type(C) is Bn)
    except AssertionError:
        print("Error: Encryption Error, Ciphertext wasn't encrypted properly.")

    M = C.mod_pow(d, n)
    return M

if __name__ == "__main__":
    main()