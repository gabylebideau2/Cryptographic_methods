from sage.all import *
import re

def wiener_attack(N, e):
    """
    Implements Wiener's attack for RSA.
    Attempts to find the private key d for given N and e.
    """
    # Compute continued fraction expansion of e/N
    cf = continued_fraction(Integer(e) / Integer(N))
    
    # Generate convergents
    convergents = cf.convergents()
    
    for frac in convergents:
        k = frac.numerator()
        d = frac.denominator()
        if k == 0:
            continue
        # Check if d is a potential private key
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        if phi < 0:
            continue
        # Solve for p and q
        s = N - phi + 1
        discriminant = s * s - 4 * N
        if discriminant.is_square():
            sqrt_disc = sqrt(discriminant)
            p = (s + sqrt_disc) // 2
            q = (s - sqrt_disc) // 2
            if p * q == N:
                return d
    return None

def deweger(n, e):
    """
    De Weger's attack for RSA.
    Attempts to find the private key d and factors p, q of n.
    """
    n = Integer(n)
    e = Integer(e)

    # Compute the continued fraction expansion of e/n
    cf = (e / n).continued_fraction()
    print("Partial Quotients:", list(cf))  # Log partial quotients for debugging

    # Iterate through convergents
    for f in cf.convergents()[1:]:
        k = f.numerator()
        d = f.denominator()

        if k == 0 or (e * d - 1) % k != 0:
            continue

        # Compute φ(n) using (e * d - 1) / k
        phi = (e * d - 1) // k

        # Solve for roots of x^2 - (n - φ(n) + 1)x + n = 0
        a = 1
        b = -(n - phi + 1)
        c = n
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            continue

        sqrt_discriminant = sqrt(discriminant)

        if sqrt_discriminant.is_integer():
            p = (-b + sqrt_discriminant) // (2 * a)
            q = (-b - sqrt_discriminant) // (2 * a)

            if p * q == n:
                return (p, q, d)
    return None

def read_file(filename):
    """
    Reads the input file and returns its content as a string.
    """
    with open(filename, "r") as f:
        content = f.read()
    return content

def parse_input(data):
    """
    Parses the input data and extracts (N, e) pairs.
    """
    pairs = re.findall(r"N(\d+)=(\d+)\se(\d+)=(\d+)", data)
    return [(int(n), int(e)) for _, n, _, e in pairs]


def wiener_with_debug(n, e):
    """Wiener's attack with debug information"""
    n = Integer(n)
    e = Integer(e)
    cf = (e / n).continued_fraction()
    ##print("Partial Quotients:", list(cf))
    
    for f in cf.convergents()[1:]:
        k, d = f.numerator(), f.denominator()
        phi = ((e * d) - 1) / k
        b = -(n - phi + 1)
        dis_sqrt = sqrt(b * b - 4 * n)
        if dis_sqrt.is_integer():
            p = (-b + dis_sqrt) / 2
            q = (-b - dis_sqrt) / 2
            if p < q:
                p, q = q, p
            return (p, q, d)
    return None

# Example for debugging N1, e1
N1 = 152424830152074416761980383938911671839299622508277457481343520025918322805703
e1 = 82761263969112182716232973843567649071227230970361962466874478674427787680753

# Example for debugging
"""
result = wiener_with_debug(N1, e1)
if result:
    p, q, d = result
    print(f"Found factors p = {p}, q = {q}, and private key d = {d}")
else:
    print("Wiener's attack failed to find factors.")
"""
def main():
    input_file = "wiener_input.txt"
    data = read_file(input_file)
    parsed_data = parse_input(data)
    
    results = []
    for i, (N, e) in enumerate(parsed_data, 1):
        d = deweger(N, e)
        if d:
            print(f"Case {i}: Secret exponent d = {d}")
        else:
            print(f"Case {i}: Wiener attack failed.")

if __name__ == "__main__":
    main() 
