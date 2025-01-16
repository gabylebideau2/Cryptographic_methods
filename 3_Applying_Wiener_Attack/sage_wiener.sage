###############################################################################
# Fichier : sage_wiener.sage
###############################################################################

from sage.all import (
    Integer,       
    sqrt,          
    RealField,      
)
import re

def wiener_attack(N, e):
    """
    Version "classique" de l'attaque de Wiener, développant e/N (fraction continue)
    Borne d < N^0.25.
    """
    N = Integer(N)
    e = Integer(e)

    
    cf = (e / N).continued_fraction()
    
    convergents = cf.convergents()

    for frac in convergents:
        k = frac.numerator()
        d = frac.denominator()
        if k == 0:
            continue
       
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        if phi < 0:
            continue
        
        s = N - phi + 1
        discriminant = s * s - 4 * N
        if discriminant >= 0:
            sqrt_disc = Integer(discriminant).isqrt()
            if sqrt_disc * sqrt_disc == discriminant:
                p = (s + sqrt_disc) // 2
                q = (s - sqrt_disc) // 2
                if p * q == N:
                    return (p, q, d)
    return None


def deweger_attack(N, e, precision_bits=2048):
    """
    Implémentation de l’attaque de de Weger.
    N, e : entiers RSA
    precision_bits : nb de bits de précision pour le calcul de sqrt(N).
    """

   
    N = Integer(N)
    e = Integer(e)


    R = RealField(precision_bits)

    # Construire alpha  en version "réelle"
    alpha = R(e) / (R(N) + R(1) - 2 * R(N).sqrt())

    r_approx = alpha.exact_rational()
 
    cf = r_approx.continued_fraction()


    # copy paste of wiener
    for frac in cf.convergents():
        # vu que k et d peuvent être "rationnels" -> on cast en Integer
        k = Integer(frac.numerator())
        d = Integer(frac.denominator())

        if k == 0:
            continue

        
        if (e * d - 1) % k != 0:
            continue

        
        phi_candidate = (e * d - 1) // k
        if phi_candidate < 0:
            continue

        
        # check
        s = N - phi_candidate + 1
        disc = s * s - 4 * N

        if disc < 0:
            continue

        sqrt_disc = Integer(disc).isqrt()
        if sqrt_disc * sqrt_disc == disc:
            p = (s + sqrt_disc) // 2
            q = (s - sqrt_disc) // 2
            if p * q == N:
                return (p, q, d)

    return None


def read_file(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def parse_input(data):
    pairs = re.findall(r"N(\d+)=(\d+)\s+e(\d+)=(\d+)", data)
    return [(int(n), int(e)) for _, n, _, e in pairs]


def main():
    input_file = "integers_to_factorize2.txt"
    data = read_file(input_file)
    parsed_data = parse_input(data)
    
    for i, (N, e) in enumerate(parsed_data, start=1):
        
        result = deweger_attack(N, e, precision_bits=2*N.bit_length())
       

        if result is not None:
            p, q, d = result
            print(f"[Case {i}] Found factors p = {p}, q = {q}, and private key d = {d}")
        else:
            print(f"[Case {i}]  failed to find factors.")


if __name__ == "__main__":
    main()
