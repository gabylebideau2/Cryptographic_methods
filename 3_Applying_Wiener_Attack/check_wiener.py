import re
from sympy import gcd, isprime
import random

def parse_file(file_path: str):
    """Parse the file to extract (e, n, d) tuples."""
    pairs = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'Hacked d=(\d+), for e=(\d+), n=(\d+)', line)
            if match:
                d = int(match.group(1))
                e = int(match.group(2))
                n = int(match.group(3))
                pairs.append((e, n, d))
    return pairs

def find_pq(n: int, d: int, e: int):
    """Try to find p and q from n, d, and e using Wiener's attack assumptions."""
    k = e * d - 1
    if k % 2 == 1:
        return None, None  # k should be even
    
    r, t = k, 0
    while r % 2 == 0:
        r //= 2
        t += 1
    
    for _ in range(100):
        g = random.randint(2, n - 1)
        y = pow(g, r, n)
        if y == 1 or y == n - 1:
            continue
        for _ in range(t - 1):
            x = pow(y, 2, n)
            if x == 1:
                p = gcd(y - 1, n)
                q = n // p
                if p * q == n and isprime(p) and isprime(q):
                    return p, q
            y = x
            if y == n - 1:
                break
    return None, None

def verify_d(e: int, d: int, n: int) -> bool:
    """Verify if d is correct by encrypting and decrypting a message."""
    p, q = find_pq(n, d, e)
    if not p or not q:
        print(f"Failed to find p and q for e={e}, n={n}")
        return False
    
    phi_n = (p - 1) * (q - 1)
    if (e * d) % phi_n != 1:
        return False

    message = random.randint(2, n - 1)
    encrypted = pow(message, e, n)
    decrypted = pow(encrypted, d, n)
    return message == decrypted

def main(input_file):
    pairs = parse_file(input_file)
    for idx, (e, n, d) in enumerate(pairs, start=1):
        if verify_d(e, d, n):
            print(f"Pair {idx}: Verified d={d} for e={e}, n={n}")
        else:
            print(f"Pair {idx}: Failed to verify d={d} for e={e}, n={n}")

if __name__ == "__main__":
    main("results_second_batch.txt")
