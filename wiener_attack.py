from wiener_attack_v2 import *
from math import isqrt

input_file = "list1.txt"  
output_file = "cracked_keys_d.txt"

rsa_pairs = []
with open(input_file, "r") as infile:
    lines = infile.readlines()
    for i in range(0, len(lines), 2):
        N_line = lines[i].strip()
        e_line = lines[i + 1].strip()
        
        N = int(N_line.split('=')[1])
        e = int(e_line.split('=')[1])
        
        rsa_pairs.append((e, N))

def find_p_q(n, e, d):
    """Calculate p and q given n, e, and d."""
    # Attempt different values of k to find an integer phi(N)
    for k in range(1, e):
        if (e * d - 1) % k == 0:
            # Calculate phi(N) based on the current k
            phi_n = (e * d - 1) // k
            
            # Calculate sum of p and q
            sum_pq = n - phi_n + 1
            
            # Calculate the discriminant
            discriminant = sum_pq**2 - 4 * n
            
            # Check if the discriminant is a perfect square
            if discriminant >= 0:
                root = isqrt(discriminant)
                
                if root * root == discriminant:
                    # Calculate p and q
                    p = (sum_pq + root) // 2
                    q = (sum_pq - root) // 2
                    
                    if p * q == n:
                        return p, q
    return None, None

# Open output file for writing results
with open(output_file, "w") as outfile:
    for idx, (e, n) in enumerate(rsa_pairs, start=1):
        d = find_private_key(e, n)
        
       # if d is None:
          #  result = f"Pair {idx}: Failed to find d for e={e}, n={n}\n"
       # else:
          #  p, q = find_p_q(n, e, d)
           # if p and q:
        result = f"Pair {idx}: Hacked d={d}, for e={e}, n={n}\n"
           # else:
             #   result = f"Pair {idx}: Hacked d={d} but failed to find p and q for e={e}, n={n}\n"
        
        outfile.write(result)
        print(result)

print(f"Results have been written to {output_file}")
