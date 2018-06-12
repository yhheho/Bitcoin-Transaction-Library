from session3.ecc import G, N, S256Point, Signature, PrivateKey
from session3.helper import double_sha256
from random import randint


class Exercise3:

    @staticmethod
    def print_divider():
        print("========================================")

    @staticmethod
    def exercise1_1():
        Exercise3.print_divider()
        secret = 1800555555518005555555
        z = int.from_bytes(double_sha256(b'ECDSA is awesome!'), 'big')
        k = randint(0, 2**256)
        r = (k*G).x.num
        s = (z+r*secret) * pow(k, N-2, N) % N   # rules, mod N, not mod prime
        print(hex(z), hex(r), hex(s))
        print(secret * G)

    @staticmethod
    def exercise1_2():
        Exercise3.print_divider()
        point = S256Point(0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574,
                          0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4)
        z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

        u = z * pow(s, N-2, N) % N
        v = r * pow(s, N-2, N) % N
        print((u*G + v*point).x.num == r)

    @staticmethod
    def exercise1_3():
        Exercise3.print_divider()
        px = 0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c
        py = 0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34

        signatures = (
            # (z, r, s)
            (0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60,
             0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395,
             0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4),
            (0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d,
             0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c,
             0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6),
        )

        point = S256Point(px, py)

        for z, r, s in signatures:
            u = z * pow(s, N-2, N) % N
            v = r * pow(s, N-2, N) % N
            print((u*G + v*point).x.num == r)

    @staticmethod
    def exercise2_1():
        Exercise3.print_divider()
        der = bytes.fromhex('304402201f62993ee03fca342fcb45929993fa6ee885e00ddad8de154f268d98f083991402201e1ca12ad140c04e0e022c38f7ce31da426b8009d02832f0b44f39a6b178b7a1')
        sec = bytes.fromhex('0204519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574')

        z = int.from_bytes(double_sha256(b'ECDSA is awesome!'), 'big')

        sig = Signature.parse(der)
        point = S256Point.parse(sec)
        print(point.verify(z, sig))

    @staticmethod
    def exercise3_1():
        Exercise3.print_divider()
        print(PrivateKey(2 ** 256 - 2 ** 199).wif(True, False))
        print(PrivateKey(2 ** 256 - 2 ** 201).wif(False, True))
        print(PrivateKey(0x0dba685b4511dbd3d368e5c4358a1277de9486447af7b3604a69b8d9d8b7889d).wif(False, False))
        print(PrivateKey(0x1cca23de92fd1862fb5b76e5f4f50eb082165e5191e116c18ed1a6b24be6a53f).wif(True, True))
