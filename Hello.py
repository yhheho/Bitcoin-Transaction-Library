from session1.exercise1 import Exercise1
from session2.exercise2 import Exercise2


def session1():
    Exercise1.exercise1_1()
    Exercise1.exercise2_1()
    Exercise1.exercise2_2()
    Exercise1.exercise3_1()
    Exercise1.exercise6_1()
    Exercise1.exercise7_1()


def session2():
    Exercise2.exercise1_1()
    Exercise2.exercise2_1()
    Exercise2.exercise3_1()
    Exercise2.exercise4_1()
    Exercise2.exercise4_3()


def main():
    # session1()
    session2()
    print('Hello Python')


if __name__ == "__main__":
    main()