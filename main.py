from random import randint, getrandbits
from math import gcd
import string

alphabet = string.ascii_lowercase

def simple_test_miller_rabin_test(n, k=10):
    if (n == 2 or n == 3):
        return True, 1

    if (n < 2 or n % 2 == 0):
        return False, None

    t = n - 1
    s = 0

    while (t % 2 == 0):
        t //= 2
        s += 1

    for i in range(k):
        a = randint(2, n - 2)
        x = pow(a, t, n)

        if (x == 1 or x == n - 1):
            continue

        for r in range(1, s):
            x = pow(x, 2, n)

            if (x == 1):
                return False, None

            if (x == n - 1):
                break

        if (x != n - 1):
            return False, None

    return True, 1 - 1 / (4 ** k)


def create_candidate_prime(length):
    prime = getrandbits(length)
    prime |= (1 << length - 1) | 1
    return prime


def create_number_prime(length=512):
    prime = 4
    while not simple_test_miller_rabin_test(prime, 128)[0]:
        prime = create_candidate_prime(length)
    return prime


def create_number_coprime(limit):
    while True:
        number = randint(2, limit - 1)
        if gcd(number, limit) == 1:
            return number


def create_keys():
    p, q = create_number_prime(), create_number_prime()
    n = p * q
    euclid_number = (p - 1) * (q - 1)
    euclid_search = create_number_coprime(euclid_number)
    d = pow(euclid_search, -1, euclid_number)

    key_public = {
        "e": euclid_search,
        "n": n
    }
    key_private = {
        "d": d,
        "n": n
    }
    return key_public, key_private


def encode(message, key_public):
    text_to_digit = [alphabet.index(char) for char in message.lower()]
    encoded = [pow(number, key_public['e'], key_public['n']) for number in text_to_digit]
    return encoded


def decode(encoded, key_private):
    decoded_digits = [pow(number, key_private['d'], key_private['n']) for number in encoded]
    decoded_message = ''.join(alphabet[char] for char in decoded_digits)
    return decoded_message


if __name__ == '__main__':
    text_source = "deniskhomey"
    key_public, key_private = create_keys()
    text_encoded = encode(text_source, key_public)
    print(f"Заданий текст: {text_source}")
    print("====================")
    print(f"Зашифрований текст: {text_encoded}")
    print(f"Розшифрований текст: {decode(text_encoded, key_private)}")
