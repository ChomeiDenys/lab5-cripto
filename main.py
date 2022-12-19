from random import randint, getrandbits
from math import gcd
import string

alp = string.ascii_lowercase


def miller_rabin_test(n, k=10):
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


def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=512):
    p = 4
    while not miller_rabin_test(p, 128)[0]:
        p = generate_prime_candidate(length)
    return p


def generate_coprime_number(limit):
    while True:
        num = randint(2, limit - 1)
        if gcd(num, limit) == 1:
            return num


def generate_keys():
    p, q = generate_prime_number(), generate_prime_number()
    n = p * q
    eul = (p - 1) * (q - 1)
    e = generate_coprime_number(eul)
    d = pow(e, -1, eul)

    public_key = {
        "e": e,
        "n": n
    }
    private_key = {
        "d": d,
        "n": n
    }
    return public_key, private_key


def encode(message, public_key):
    text_to_digits = [alp.index(ch) for ch in message.lower()]
    encoded = [pow(num, public_key['e'], public_key['n']) for num in text_to_digits]
    return encoded


def decode(encoded, private_key):
    decoded_digits = [pow(num, private_key['d'], private_key['n']) for num in encoded]
    decoded_message = ''.join(alp[ch] for ch in decoded_digits)
    return decoded_message


if __name__ == '__main__':
    text = "MikhailDubrovskyi"
    public_key, private_key = generate_keys()
    encoded_text = encode(text, public_key)
    print(text)
    print(f"Encoded text: {encoded_text}")
    print(f"Decoded text: {decode(encoded_text, private_key)}")