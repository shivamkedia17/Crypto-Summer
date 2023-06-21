from gcd import extended_gcd
from petlib.bn import Bn

def main():
    '''
    print(extended_gcd(4,5))
    print(extended_gcd(2180, 1240))
    print(extended_gcd(11,13))
    '''

    # a = Bn.random(Bn(2).pow(500))
    # b = Bn.random(Bn(2).pow(500))

    a = Bn.get_prime(24, 1)
    b = Bn.get_prime(24, 1)

    print("First  Number: ", a)
    print("Second Number: ", b)

    d, x, y = extended_gcd(a, b)
    print(f"gcd({a}, {b}) = {d} = {x}.{a} + {y}.{b}")

    # for _ in range(10):
    #     e = Bn.random(n)
    #     d = modular_inverse(e, phi_n)
    #     print(f"e = {e}\nd = {d}\n")


if __name__ == "__main__":
    main()