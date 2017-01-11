from prime import is_prime, is_deduction
from random import randint, randrange
from math import sqrt
from modulus import div_modulus, gcd_ex

from curve import EllipticCurve, Point
from fractions import Fraction as Frac

from ecc import elliptic as el

attempts = []


def generate_required_prime_number(l, limit=10000000):
    if l < 2:
        raise Exception("Указанная длина слишком мала!")
    prime = False
    i = 0
    bottom = 2 ** (l - 1)
    top = 2 ** l - 1
    while not prime and i < limit:
        for c in reversed(range(int(sqrt(top)))):
            for d in range(int(sqrt(top // 3))):
                p = c ** 2 + 3 * d ** 2
                if bottom <= p <= top and p % 4 == 1 and p not in attempts and is_prime(p):
                    attempts.append(p)
                    return p, c, d

        raise Exception("Не удалось подобрать c и d")
    raise Exception("Не удалось подобрать простое число за указанное число итераций")


def step2(l):
    return generate_required_prime_number(l)


def step3(p, a, b):
    l = [2*a, 2*b]
    l += [-x for x in l]
    for T in l:
        N = p + 1 + T
        for k in [2, 4]:
            if N % k == 0:
                r = N // k
                if is_prime(r):
                    simple_print(3)
                    print('Одно из условий N = 2r, N = 4r - выполнилось.\n'
                          'p = {}. N = {}. r = {}'.format(p, N, r))
                    return N, r, k
    return None


def step4(p, r, m):
    if r == p:
        print('Выполнилось одно из нежелательных условий: r = p, r|(p - 1), r|(p^2 - 1)...r|(p^m - 1)')
        return False
    for i in range(1, m + 1):
        if r % (p ** i - 1) == 0:
            print('Выполнилось одно из нежелательных условий: r = p, r|(p - 1), r|(p^2 - 1)...r|(p^m - 1)')
            return False
    simple_print(4)
    print('Не выполнилось ни одно из нежелательных условий : r = p, r|(p - 1), r|(p^2 - 1)...r|(p^m - 1)')
    return True


def step5(p, r):
    '''
    Вычисленние В и х0, у0.
    :param p: полученный на шаге 3
    :return: (x, y, B) - такой кортеж
    '''
    MAX_INDEX = 10000  # максимальное количество подборов
    B = None
    x = None
    y = None
    _index = 0
    b_variants = []
    flag = True
    while (flag):
        B = 0
        while B in b_variants or B == 0:  # Запомним уже попадавшиеся варианты
            x = randrange(1, p - 1)
            y = randrange(1, p - 1)
            gcd, first, second = gcd_ex(x, p)
            first = first if first > 0 else first + p
            B = ((y ** 2 % p) - (x * x % p * (x % p))) * (first % p)
            B = B + p if B < 0 else B
            # print('x={0}, y = {1}, B = {2}, len = {3}'.format(x, y, B, len(b_variants)))
            if len(b_variants) == p - 1:
                raise 'Не удалось найти подходящие координаты'
        b_variants.append(B)
        # x, y, B = -1, 10, 101
        # print('deduc = {0}'.format(is_deduction(B, 2*r)))
        # print('coub_deduc = {0}'.format(is_coub_deduction(B, 2*r)))
        flag = not is_deduction(-B, 2*r) and is_deduction(-B, 4*r)
        # print(flag)
        gcd, first, second = gcd_ex(x, p)
        first = first if first > 0 else first + p
        flag = flag and ((y ** 2 % p) == (x * x % p * (x % p))) * (first % p)
        # print('{0} ** 2 mod {4} == ({1} ** 3 + {3}) mod {4}   --- {2}'.format(y, x, flag, B, r))
        # Не вышло понять почему тут не работает как в примере

        # flag = flag and is_deduction(B, 6*r) and is_coub_deduction(B, 6*r) # N = 6r
        # print(flag)
        # flag = flag and not is_deduction(B, 2*r) and is_coub_deduction(B, 2*r) # N = 2r
        # print(flag)
        # flag = flag and is_deduction(B, 3*r) and not is_coub_deduction(B, 3*r) # N = 3r
        # print(flag)
        flag = not flag
        # print(flag)
        # flag = False
        _index += 1

        if _index == MAX_INDEX:
            raise 'Произошла ошибка вычисления на шаге 5. Слишком долгий перебор'
    simple_print(5)
    print('Произвольная точка ({},{}). B = {}'.format(x % p, y % p, B))
    return (x % p, y % p, B)


def simple_print(step):
    print('************ ШАГ {} ************'.format(step))


def main():
    l = 16
    m = 5

    res = None
    while res is None:
        p, c, d = step2(l)
        simple_print(1)
        print('Простое число p = {}'.format(p))
        simple_print(2)
        print('Ражложили на простые множители и нашли c = {} и d = {}'.format(c, d))
        res = step3(p, c, d)
        if res and not step4(p, res[1], m):  # res[1] is r, mb better rewrite to namedtuple
            res = None
        if res is None:
            simple_print(3)
            print('Ни одно из условий N = 2r, N = 4r - не выполнилось. Вернемся на шаг 1.')

    N, r, k = res

    res = True
    iterations = 0
    max_iterations = 1000
    while res is not None:
        iterations += 1
        if iterations > max_iterations:
            raise Exception("Слишком много итераций в цикле")
        x0, y0, B = step5(p, r)
        # print('x = {0}, y = {1}, B = {2}'.format(x0, y0, B))
        point = (x0, y0)
        # y^2 = x^3 + B должно выполняться!

        # Step 6
        res = el.mulp(0, -B, p, point, N)  # mulp same as mulf but goes back from projective
        simple_print(6)
        if res is None:
            print('N * (x0, y0) = P∞ - выполняется')
        else:
            print('N * (x0, y0) = P∞ - не выполняется. Вернемся к шагу 5.')

    # Step 7 на другой библиотеке
    # in ecc library curve presented as y**2 == x**3 - p*x - q (mod n), so use -A, -B and p
    # print(el.element(point, 0, -B, p))  # is on the curve
    # Q = el.from_projective(el.mulf(0, -B, p, el.to_projective(point), k), p)
    Q = el.mulp(0, -B, p, point, k)
    simple_print(7)
    print("Q:", Q)
    print('************ РЕЗУЛЬТАТ ************')
    print('p = {} \nB = {} \nQ = {}\nr = {}'.format(p, B, Q, r))


if __name__ == '__main__':
    main()
