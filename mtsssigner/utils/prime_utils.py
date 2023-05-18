from sympy import sieve, nextprime, isprime
from bisect import bisect_right
import math

# Contains functions pertaining to prime powers
# (generation of, checking if numbers are one or rounding to certain prime powers)

basic_prime_power_sequence = [2, 3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41,
                              43, 47, 49, 53, 59, 61, 64, 67, 71, 73, 79, 81, 83, 89, 97, 101, 103, 107, 109, 113,
                              121, 125, 127, 128, 131, 137, 139, 149, 151, 157, 163, 167, 169, 173, 179, 181, 191,
                              193, 199, 211, 223, 227, 229, 239, 241, 243, 251, 729]

# Checks if a number is a prime power
# https://www.quora.com/How-can-we-check-if-a-number-is-prime-power
def is_prime_power(number:int) -> bool:
    if number < 2:
        return False
    power_range = int(math.log(number, 2))
    for power in range(1,power_range+1):
        if power == 1:
            root = number
        elif power == 2:
            root = int(math.sqrt(number))
        else:
            # https://stackoverflow.com/questions/19255120/is-there-a-short-hand-for-nth-root-of-x-in-python
            root = int(round(math.exp(math.log(number)/power), 0))
            # ou root = int(round(x**(1/n)))
        if (number == (root**power) and isprime(root)):
            return True
    return False

# Generates a prime power sequence, which contain primes (p¹) up until 'number'
def generate_prime_power_sequence(number):
    prime_power_sequence = [prime for prime in sieve.primerange(number*2)]
    for n in range(2,11):
        prime_powers_of_n = [x**n for x in sieve.primerange(number/n)]
        prime_power_sequence.extend(prime_powers_of_n)
    prime_power_sequence.sort()
    return prime_power_sequence

# Returns closest prime power bigger than number
# Prime power sequence contains primes raised up to 10
def round_to_nearest_prime_power(number: int):
    prime_power_sequence = generate_prime_power_sequence(number)
    try:
        return prime_power_sequence.index(number)
    except:
        return prime_power_sequence[bisect_right(prime_power_sequence, number)]

# Returns closest prime power p**n bigger than number
def round_to_nearest_prime_power_raised_by_n(number: int, n: int) -> int:
    if n == 1:
        return nextprime(number)
    prime_power_sequence = generate_prime_power_sequence(number/n)
    print(prime_power_sequence)
    try:
        return prime_power_sequence.index(number)
    except:
        return prime_power_sequence[bisect_right(prime_power_sequence, number)]
