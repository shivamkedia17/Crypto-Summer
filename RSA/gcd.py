from petlib.bn import Bn

def main():
    a = 23
    b = 53
    # print(f"The GCD of {a} and {b} is {gcd(a,b)}")

    d, x, y = extended_gcd(a, b)
    print(f"gcd({a}, {b}) = {d} = {x}.{a} + {y}.{b}")
    print(f"Inverse of {a} mod {b} is ", modular_inverse(a, b))

def extended_gcd(a, b):
    """
    Iterative Extended Euclidean GCD
    Return d,x,y such that d = x.a + y.b
    """
    
    # r_i = x_i.a + y_i.b
    
    r_0 = a
    r_1 = b

    x_0, y_0 = 1, 0 
    x_1, y_1 = 0, 1 

    while r_1 != 0:
        quotient, remainder = divmod(r_0, r_1)
        r_0, r_1 = r_1, remainder       # gcd(a, b) = (b, a mod b)
        x_0, x_1 = x_1, x_0 - quotient*x_1
        y_0, y_1 = y_1, y_0 - quotient*y_1

    return (r_0, x_0, y_0)

def gcd(a,b):
    '''
    Iterative GCD using Euclidean algorithm
    '''
    _b = a
    _r = b
    while _r != 0:
        _b, _r = _r, _b % _r
    
    return _b


def modular_inverse(a: int | Bn, n: int | Bn) -> int | Bn | None:
    """
    Given a, n where 'a' belongs to set Z_n, returns the modular inverse of 'a' in set Z_n
    """
    d,x,y = extended_gcd(a, n)
    return x if d == 1 else None

if __name__ == "__main__":
    main()
