from unittest import TestCase
from io import BytesIO
from session3.helper import double_sha256, encode_base58, \
                            hash160, encode_base58_checksum, decode_base58
from random import randint


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
        return self.num != other.num or self.prime != other.prime

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

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num, self.prime)

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

    def __init__(self, x, y, a, b):
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

    def __rmul__(self, coefficient):
        product = self.__class__(None, None, self.a, self.b)
        for _ in range(coefficient):
            product += self

        return product


A = 0
B = 7
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def hex(self):
        return '{:x}'.format(self.num).zfill(64)

    def __repr__(self):
        return self.hex()

    def sqrt(self):
        return self**((P+1)//4)


class S256Point(Point):
    bits = 256

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)

        if x is None:
            super().__init__(x=None, y=None, a=a, b=b)
        elif type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        else:
            return 'Point({}, {})'.format(self.x, self.y)

    def __rmul__(self, coefficient):
        # 因為最大是 2^256
        # 所以把 N 取 mod 後剩下的數一定可以用 256 bits 表示
        # 那麼只要將 mod 後的數對每個位元看是否是1來判斷要不要累加即可得到結果

        coef = coefficient % N
        current = self

        # result is what we return, starts at 0
        result = S256Point(None, None)

        # we double 256 times and add where there is a 1 in the binary
        # representation of coefficient
        for i in range(self.bits):
            if coef & 1:
                result += current

            current += current
            # we shift the coefficient to the right
            coef >>= 1
        return result

    def sec(self, compressed=True):
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    def address(self, compressed=True, testnet=False):
        sec = self.sec(compressed)
        h160 = hash160(sec)

        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'

        raw = prefix + h160
        checksum = double_sha256(raw)[:4]
        address = encode_base58(raw + checksum)
        return address.decode('ascii')

    def verify(self, z, sig):
        s_inv = pow(sig.s, N-2, N)

        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u*G + v*self
        return total.x.num == sig.r

    @classmethod
    def parse(cls, sec_bin):

        # if the first byte is 4, the SEC has x and y
        if sec_bin[0] == 4:
            x = int(sec_bin[1:33].hex(), 16)
            y = int(sec_bin[33:65].hex(), 16)
            return S256Point(x, y)

        # if the first byte is not 4, we have to compute y
        # note that -y mod p = p - y in finite field
        is_even = sec_bin[0] == 2
        x = S256Field(int(sec_bin[1:].hex(), 16))
        alpha = x**3 + S256Field(B)
        beta = alpha.sqrt()

        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        else:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta

        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)


class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

    def der(self):
        rbin = self.r.to_bytes(32, byteorder='big')

        # because if highest bit is set, it means it's negative
        # (which means the leading bit of the byte is 1 -> >= 128)
        # so we need to put a '00' to prevent it becoming negative
        if rbin[0] >= 128:
            rbin = b'\x00' + rbin

        # add length
        result = bytes([2, len(rbin)]) + rbin

        sbin = self.s.to_bytes(32, byteorder='big')
        if sbin[0] >= 128:
            sbin = b'\x00' + sbin

        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result

    @classmethod
    def parse(cls, sig_bin):
        s = BytesIO(sig_bin)
        compound = s.read(1)[0]

        if compound != 0x30:
            raise RuntimeError('Bad Signature')

        length = s.read(1)[0]
        if length + 2 != len(sig_bin):
            raise RuntimeError('Bad Signature Length')

        marker = s.read(1)[0]
        if marker != 0x02:
            raise RuntimeError('Bad Signature')

        rlength = s.read(1)[0]
        r = int(s.read(rlength).hex(), 16)

        marker = s.read(1)[0]
        if marker != 0x02:
            raise RuntimeError('Bad Signature')

        slength = s.read(1)[0]
        s = int(s.read(slength).hex(), 16)

        if len(sig_bin) != 6 + rlength + slength:
            raise RuntimeError('Signature too long')

        return cls(r, s)


class PrivateKey:

    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')

        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'

        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''

        return encode_base58_checksum(prefix + secret_bytes + suffix)

    def sign(self, z):
        k = randint(0, 2**256)
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        s = (z + r*self.secret) * k_inv

        if s > N/2:
            s = N - s

        return Signature(r, s)
