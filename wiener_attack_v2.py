from typing import Tuple, List, Generator, Optional

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

def generate_convergents(continued_fraction: List[int]) -> Generator[Tuple[int, int], None, None]:
    num0, denom0 = 0, 1
    num1, denom1 = 1, 0
    for term in continued_fraction:
        numerator = term * num1 + num0
        denominator = term * denom1 + denom0
        yield numerator, denominator
        num0, denom0 = num1, denom1
        num1, denom1 = numerator, denominator

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
