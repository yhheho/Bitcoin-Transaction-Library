from session1.ecc import FieldElement, Point
from random import randint


class Exercise1:

    def __init__(self):
        pass

    @staticmethod
    def print_divider():
        print("==================================================")

    @staticmethod
    def exercise1_1():
        Exercise1.print_divider()
        print(FieldElement(2, 31) + FieldElement(15, 31))
        print(FieldElement(17, 31) + FieldElement(21, 31))
        print(FieldElement(29, 31) - FieldElement(4, 31))
        print(FieldElement(15, 31) - FieldElement(30, 31))

    @staticmethod
    def exercise2_1():
        Exercise1.print_divider()
        print(FieldElement(24, 31) * FieldElement(19, 31))
        print(FieldElement(17, 31) ** 3)
        print(FieldElement(5, 31) ** 5 * FieldElement(18, 31))

    @staticmethod
    def exercise2_2():
        Exercise1.print_divider()
        prime = 31
        k = randint(1, prime)

        print(sorted([i*k % prime for i in range(prime)]))

    @staticmethod
    def exercise3_1():
        Exercise1.print_divider()
        print(FieldElement(3, 31) / FieldElement(24, 31))
        print(FieldElement(17, 31)**(-3))
        print(FieldElement(4, 31)**(-4) * FieldElement(11, 31))

    @staticmethod
    def exercise6_1():
        print(Point(2, 5, 5, 7) + Point(-1, -1, 5, 7))

    @staticmethod
    def exercise7_1():
        print(Point(-1, 1, 5, 7) + Point(-1, 1, 5, 7))



