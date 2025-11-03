"""
Utility functions for prime number calculations.
"""


def calculate_nigel_number(n):
    """
    Calculate the Nigel Number for a given positive integer N.
    
    The Nigel Number is defined as the sum of all prime numbers 
    that are less than or equal to N.
    
    Args:
        n (int): A positive integer
        
    Returns:
        dict: A dictionary containing:
            - 'sum': The sum of all primes <= N (Nigel Number)
            - 'primes': List of all prime numbers <= N
            
    Raises:
        ValueError: If n is not a positive integer
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Input must be a positive integer")
    
    # Handle edge cases
    if n == 1:
        return {"sum": 0, "primes": []}
    
    if n == 2:
        return {"sum": 2, "primes": [2]}
    
    # Use Sieve of Eratosthenes to find all primes up to n
    primes = sieve_of_eratosthenes(n)
    prime_sum = sum(primes)
    
    return {"sum": prime_sum, "primes": primes}


def sieve_of_eratosthenes(n):
    """
    Find all prime numbers up to and including n using the Sieve of Eratosthenes algorithm.
    
    This is an efficient algorithm for finding all primes up to a given limit.
    Time complexity: O(n log log n)
    Space complexity: O(n)
    
    Args:
        n (int): Upper limit (inclusive) for finding primes
        
    Returns:
        list: List of all prime numbers <= n
    """
    if n < 2:
        return []
    
    # Create a boolean array "prime[0..n]" and initialize all entries as True
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False  # 0 and 1 are not prime numbers
    
    p = 2
    while p * p <= n:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Update all multiples of p starting from p*p
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    
    # Collect all prime numbers
    primes = []
    for i in range(2, n + 1):
        if prime[i]:
            primes.append(i)
    
    return primes