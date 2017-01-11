
def gcd_ex(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcd_ex(b, a % b)
        return d, y, x - y * (a // b)


def div_modulus(a, b, m):
    return (a * gcd_ex(b, m)[1]) % m