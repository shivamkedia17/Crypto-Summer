def legendre_symbol(a, p):
    """Calculate the Legendre symbol (a|p)."""
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(a, p):
    """Tonelli-Shanks algorithm to find square roots modulo a prime p."""
    if legendre_symbol(a, p) != 1:
        raise ValueError("The given value 'a' is not a quadratic residue modulo 'p'.")

    # Factor out the largest power of 2 from p-1.
    s = p - 1
    e = 0
    while s % 2 == 0:
        s >>= 1
        e += 1

    # Find a quadratic non-residue b.
    b = 2
    while legendre_symbol(b, p) != -1:
        b += 1

    # Initialize variables.
    m = pow(a, s, p)
    t = pow(a, (s + 1) // 2, p)
    c = pow(b, s, p)
    r = e

    # Main loop.
    while m != 1:
        i = 0
        m_tmp = m
        while m_tmp != 1:
            m_tmp = (m_tmp * m_tmp) % p
            i += 1

        # Update variables.
        b_pow = pow(c, 1 << (r - i - 1), p)
        r = i
        t = (t * b_pow) % p
        c = (b_pow * b_pow) % p
        m = (m * c) % p

    return t

# Example usage:
if __name__ == "__main__":
    p = 67  # Replace with your chosen prime number
    a = 37  # Replace with your chosen value 'a'

    try:
        sqrt_a = tonelli_shanks(a, p)
        print(f"The square root of {a} modulo {p} is: {sqrt_a}")
        # The other square root is (p - sqrt_a) modulo p.
    except ValueError as e:
        print(e)
