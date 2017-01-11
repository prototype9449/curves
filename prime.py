from random import randint
from math import sqrt


def simple_is_prime(a):
    return all(a % i for i in range(2, int(sqrt(a))))


def to_binary(n):
    r = []
    while n > 0:
        r.append(n % 2)
        n /= 2
    return r


def Miller_Rabin_test(n, s=50):
    for j in range(1, s + 1):
        a = randint(1, n - 1)
        b = to_binary(n - 1)
        d = 1
        for i in range(len(b) - 1, -1, -1):
            x = d
            d = (d * d) % n
            if d == 1 and x != 1 and x != n - 1:
                return True  # Составное
            if b[i] == 1:
                d = (d * a) % n
                if d != 1:
                    return True  # Составное
                return False  # Простое


def is_prime(p):
    return Miller_Rabin_test(p) and simple_is_prime(p)


def generate_required_prime_number(l, limit=10000000):
    if l < 2:
        raise Exception("Указанная длина слишком мала!")
    prime = False
    i = 0
    while not prime and i < limit:
        p = randint(2 ** (l - 1), 2 ** l - 1)
        if p % 6 == 1 and is_prime(p):
            return p
    raise Exception("Не удалось подобрать простое число за указанное число итераций")


def is_deduction(a, p):
    '''
    Вычисляет является ли а - квадратичным (при q = 3 кубическим)  вычетом по модулю р
    Перебором, существует ли решение для x^2 = a mod p,
    если да, то а - квадратичный вычет, иначет невычет
    '''
    for ind in range(1, p - 1):
        x = (ind ** 2) % p
        if x == a:
            return True
    return False
