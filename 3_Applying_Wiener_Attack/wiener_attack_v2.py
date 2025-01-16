from typing import Tuple, List, Generator, Optional
from decimal import Decimal, getcontext

def int_sqrt(n: int) -> int:
    if n == 0:
        return 0
    estimate = 2 ** ((n.bit_length() + 1) // 2)
    while True:
        next_estimate = (estimate + n // estimate) // 2
        if next_estimate >= estimate:
            return estimate
        estimate = next_estimate


def check_perfect_square(n: int) -> bool:
    h = n & 0xF 
    if h > 9:
        return False
    x = int_sqrt(n)
    return x * x == n

def fraction_to_continued_fraction(num: int, denom: int) -> Generator[int, None, None]:
    while denom != 0:
        quotient = num // denom
        yield quotient
        num, denom = denom, num - quotient * denom



def continued_fraction_of_real(x: Decimal, max_iterations=1000):

    cf = []
    r = x
    for _ in range(max_iterations):

        a = r.to_integral_value(rounding="ROUND_FLOOR")  #  floor(r)
        a_int = int(a)  
        cf.append(a_int)
        
      
        frac = r - a
        if frac == 0:
            break
    
        r = 1 / frac
    
    return cf

def generate_convergents(cf: List[int]):

    p0, q0 = 0, 1
    p1, q1 = 1, 0
    for a in cf:
        p = a * p1 + p0
        q = a * q1 + q0
        yield (p, q)
        p0, q0 = p1, q1
        p1, q1 = p, q



def find_private_key(e: int, n: int, max_convergents: int = 10000) -> Optional[int]:
    continued_frac = list(fraction_to_continued_fraction(e, n))
    
    for idx, (k, candidate_d) in enumerate(generate_convergents(continued_frac)):
        if idx >= max_convergents:
            break  

        if k == 0:
            continue

      
        if (e * candidate_d - 1) % k != 0:
            continue
        phi_candidate = (e * candidate_d - 1) // k
        
       
        potential_square_term = n - phi_candidate + 1
        if potential_square_term % 2 != 0:
            continue
        
        half_term = potential_square_term // 2
        discriminant = half_term ** 2 - n

   
        if discriminant >= 0 and check_perfect_square(discriminant):
            return candidate_d
    
    return None



def find_private_key_de_weger(e: int, n: int, max_convergents: int = 10000) -> Optional[int]:
   
    getcontext().prec = 2 * n.bit_length() 

    # alpha = e / (n + 1 - 2*sqrt(n)) en Decimal
    N_dec = Decimal(n)
    e_dec = Decimal(e)
    alpha = e_dec / (N_dec + Decimal(1) - 2 * N_dec.sqrt())

    cf = continued_fraction_of_real(alpha, max_iterations=max_convergents)

    # Parcourir les convergents
    for idx, (k, candidate_d) in enumerate(generate_convergents(cf)):
        if idx >= max_convergents:
            break
        
        if k == 0:
            continue
        
        # check div par k
        if (e * candidate_d - 1) % k != 0:
            continue

        phi_candidate = (e * candidate_d - 1) // k

        # Vérifier discriminant, etc.
        potential_square_term = n - phi_candidate + 1
        if potential_square_term % 2 != 0:
            continue
        
        half_term = potential_square_term // 2
        discriminant = half_term**2 - n

        if discriminant >= 0 and check_perfect_square(discriminant):
            return candidate_d

    return None