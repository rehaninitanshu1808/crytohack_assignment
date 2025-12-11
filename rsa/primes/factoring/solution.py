import math
import sys

# Set a higher recursion limit for the isqrt function if needed
# sys.setrecursionlimit(2000)

n = 510143758735509025530880200653196460532653147

# --- Custom Integer Square Root Function for Large Integers ---
# Standard math.isqrt() fails for numbers this large.
def integer_sqrt(n):
    """
    Computes the integer square root of n using Newton's method.
    """
    if n < 0:
        raise ValueError("Cannot compute square root of negative number")
    if n == 0:
        return 0
    
    # Start with a decent initial guess (using float math for a quick start)
    x = int(n**0.5) 
    
    while True:
        # Newton's method for finding square roots: x_new = (x + n/x) / 2
        x_new = (x + n // x) // 2
        
        if x_new >= x: # If we've converged or overshot, the previous x is the floor
            return x
        x = x_new

def fermat_factor(n):
    # a = math.isqrt(n) + 1  <-- Original line
    a = integer_sqrt(n) + 1  # <-- Fixed line
    b2 = a * a - n
    
    print(f"Starting value for a: {a}")
    
    # We will limit the search space to avoid an infinite loop if N is prime
    # or the factors are too far apart for Fermat's method to be efficient.
    # We check 1,000,000 iterations to find the factor pair.
    max_iterations = 1000000 
    
    for i in range(max_iterations):
        # b = math.isqrt(b2) <-- Original line
        b = integer_sqrt(b2) # <-- Fixed line
        
        if b * b == b2:
            return a - b, a + b
        
        a += 1
        b2 = a * a - n
        
        if i % 10000 == 0:
             print(f"Iteration {i}: a = {a}")
             
    # If it fails to factor after max_iterations, it returns None, None
    return None, None 

p, q = fermat_factor(n)

if p is not None and q is not None:
    print("\n--- Result ---")
    print(f"Factor p: {p}")
    print(f"Factor q: {q}")
    print(f"Smallest Factor: {min(p, q)}")
    # Double-check the factors multiply to N
    print(f"Check p * q == n: {p * q == n}")
else:
    print("\n--- Failed ---")
    print("Fermat's factorization failed to find factors after 1,000,000 iterations.")