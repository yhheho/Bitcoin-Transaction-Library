from unittest import TestCase


class FieldElement:

    def __init__(self, num, prime):
        self.num = num
        self.prime = prime
        if self.num >= self.prime or self.num < 0:
            error = 'Num {} not in field range 0 to {}'.format(
                self.num, self.prime-1)
            raise RuntimeError(error)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __ne__(self, other):
        if other is None:
            return True
        return self.num != other.num and self.prime != other.prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __add__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')

        num = (self.num + other.num) % self.prime
        prime = self.prime
        return self.__class__(num, prime)

    def __sub__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')

        num = (self.num - other.num) % self.prime
        prime = self.prime
        return self.__class__(num, prime)

    def __mul__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')

        num = (self.num * other.num) % self.prime
        prime = self.prime
        return self.__class__(num, prime)

    def __pow__(self, n):
        # self.num**(p-1) % p == 1
        prime = self.prime
        num = pow(self.num, n % (prime-1), prime)
        return self.__class__(num, prime)

    def __truediv__(self, other):
        if self.prime != other.prime:
            raise RuntimeError('Primes must be the same')

        num = (self.num * pow(other.num, self.prime-2, self.prime)) % self.prime
        prime = self.prime
        return self.__class__(num, prime)


class Point:

    def __init__(self, x, y ,a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b

        if self.x is None and self.y is None:
            return

        if self.y**2 != self.x**3 + a*x + b:
            raise RuntimeError('({}, {}) is not on the curve!'.format(self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y \
            and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y \
            or self.a != other.a or self.b != other.b

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({}, {})'.format(self.x, self.y)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise RuntimeError('Points {}, {} are not on the same curve'.format(self, other))

        if self.x is None:
            return other

        if other.x is None:
            return self

        # case1: (2, 1) + (2, -1)
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        # case2: (2, 1) + (3, 2)
        if self.x != other.x:
            s = (other.y - self.y)/(other.x - self.x)
            x = s**2 - self.x - other.x
            y = s*(self.x-x) - self.y
            return self.__class__(x, y, self.a, self.b)

        # case3: (2, 1) + (2, 1)
        else:
            s = (3*self.x**2 + self.a) / (2*self.y)
            x = s**2 - 2*self.x
            y = s*(self.x-x) - self.y
            return self.__class__(x, y, self.a, self.b)


