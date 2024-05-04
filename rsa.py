import random
import math

def gcd_using_euclidean_algorithm(a, b):
    if(b>a):
        a, b = b, a

    while(b!=0):
        r = a%b

        a=b
        b=r

    return a

def modular_exponentiation(a, b, n):
    previous = a%n
    product = 1

    if(b%2 == 1):
        product *= previous

    b = b//2

    while(b>0):
        current = (previous * previous)%n
        
        if(b%2 == 1):
            product *= current

        b = b//2
        previous = current

    return product%n

def is_prime(n):
    for i in range(2, int(math.sqrt(n))+1):
        if(n%i == 0):
            return False
    
    return True

def choose_prime_number(start, end):
    while(True):
        n = random.randint(start, end)

        if(n%2 != 0):
            if(is_prime(n)):
                return n

def phi(p, q):
    return (p-1)*(q-1)

def choose_e(phi_n):
    for i in range(2, phi_n):
        if(gcd_using_euclidean_algorithm(phi_n, i) == 1):
            return i

def modular_multiplicative_inverse(x, n):
    if(x>n):
        a=x
        b=n
    else:
        a=n
        b=x

    t1=0
    t2=1

    while(b!=0):
        q = a//b
        r = a%b

        t = t1 - t2*q

        a=b
        b=r

        t1=t2
        t2=t

    if(t1>0):
        return t1
    else:
        return t1 + n

def encrypt(string, e, n):
    encrypted_ascii_values = ''

    for character in string:
        ascii_value = ord(character)
        encrypted_ascii_value = (modular_exponentiation(ascii_value, e, n))

        encrypted_ascii_values = encrypted_ascii_values + str(encrypted_ascii_value) + ' '

    encrypted_ascii_values = encrypted_ascii_values.rstrip(' ')

    return encrypted_ascii_values

def decrypt(encrypted_ascii_values, d, n):
    list_of_encrypted_ascii_values = encrypted_ascii_values.split()
    original_string = ''

    for encrypted_ascii_value in list_of_encrypted_ascii_values:
        original_acsii_value = modular_exponentiation(int(encrypted_ascii_value), d, n)
        original_string = original_string + chr(original_acsii_value)

    return original_string

    