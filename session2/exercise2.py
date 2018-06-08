from session2.ecc import FieldElement, Point, G
from session2.helper import hash160, double_sha256, encode_base58


class Exercise2:

    def __init__(self):
        pass

    @staticmethod
    def print_divider():
        print("========================================")

    @staticmethod
    def exercise1_1():
        Exercise2.print_divider()
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        points = ((192, 105), (17, 56), (200, 119), (1, 193), (42, 99))
        for x_raw, y_raw in points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)

            try:
                p = Point(x, y, a, b)
                print('({}, {}) is on the curve'.format(x_raw, y_raw))
            except RuntimeError:
                print('({}, {}) is not on the curve'.format(x_raw, y_raw))

    @staticmethod
    def exercise2_1():
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        additions = ((192, 105, 17, 56), (47, 71, 117, 141), (143, 98, 76, 66))

        for x1_raw, y1_raw, x2_raw, y2_raw in additions:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)

            x2 = FieldElement(x2_raw, prime)
            y2 = FieldElement(y2_raw, prime)

            p1 = Point(x1, y1, a, b)
            p2 = Point(x2, y2, a, b)
            print('{} + {} = {}'.format(p1, p2, p1+p2))

    @staticmethod
    def exercise3_1():
        Exercise2.print_divider()
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)

        multiplications = ((2, 192, 105), (2, 143, 98), (2, 47, 71), (4, 47, 71), (8, 47, 71), (21, 47, 71))

        for n, x_raw, y_raw in multiplications:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            p = Point(x, y, a, b)
            product = Point(None, None, a, b)

            for _ in range(n):
                product = product + p

            print(product)

    @staticmethod
    def exercise4_1():
        Exercise2.print_divider()
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(47, prime)
        y = FieldElement(71, prime)
        p = Point(x, y, a, b)
        product = Point(x, y, a, b)
        inf = Point(None, None, a, b)

        count = 1
        while product != inf:
            product += p
            count = count + 1

        print(count)

    @staticmethod
    def exercise4_3():
        Exercise2.print_divider()
        p = 2**256 - 2**32 - 977
        x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        print(y ** 2 % p == (x ** 3 + 7) % p)

    @staticmethod
    def exercise4_4():
        # this exercise is confirming n*G = 0
        Exercise2.print_divider()
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        # n = 0x0A
        print(n * G)

    @staticmethod
    def exercise4_5():
        Exercise2.print_divider()
        secret = 999
        point = secret*G
        print(point)

    @staticmethod
    def exercise5_1():
        Exercise2.print_divider()
        secrets = (7, 1485, 2 ** 128, 2 ** 240 + 2 ** 31)

        # iterate over secrets
        for secret in secrets:
            # get the public point
            print(secret * G)

    @staticmethod
    def exercise6_1():
        Exercise2.print_divider()
        secrets = (999 ** 3, 123, 42424242)

        for secret in secrets:
            point = secret * G
            print(point.sec(True))
            # uncompressed = b'\x04' + point.x.num.to_bytes(32, 'big') + point.y.num.to_bytes(32, 'big')
            #
            # if point.y.num % 2 == 0:
            #     compressed = b'\x02' + point.x.num.to_bytes(32, 'big')
            # else:
            #     compressed = b'\x03' + point.x.num.to_bytes(32, 'big')
            #
            # print(uncompressed.hex())
            # print(compressed.hex())

    @staticmethod
    def exercise7_1():
        Exercise2.print_divider()
        secrets = ((True, 888**3), (False, 321), (False, 4242424242))

        for compressed, secret in secrets:

            p = secret * G
            sec = p.sec(compressed)
            h160 = hash160(sec)

            for prefix in (b'\x00', b'\x6f'):
                raw = prefix + h160
                checksum = double_sha256(raw)[:4]
                total = raw + checksum
                address = encode_base58(total).decode('ascii')
                if prefix == b'\x00':
                    print("mainnet: " + address)
                else:
                    print("testnet: " + address)




