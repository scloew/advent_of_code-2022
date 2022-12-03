"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""
from string import ascii_lowercase, ascii_uppercase


DELIMITER = '\n===============\n'


def day_1(part='A'):
    """
    :param part: for polymorphism; 'A' for part A 'B' for B
    :return:
    """
    with open(r'inputs/DAY_1.txt') as infile:
        data = infile.read().split('\n\n')

    cals = [sum(int(i) for i in entry.split('\n')) for entry in data[:-1]]
    cals.sort()
    return sum(cals[-1 if part.lower() == "a" else -3:])


def day_2a():
    with open(r'inputs/DAY_2.txt') as infile:
        data = infile.read().split('\n')
    games = [tuple((i[0], i[-1])) for entry in data[:-1] for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    outcomes = {('A', 'X'): 3, ('A', 'Y'): 6, ('A', 'Z'): 0,
                ('B', 'X'): 0, ('B', 'Y'): 3, ('B', 'Z'): 6,
                ('C', 'X'): 6, ('C', 'Y'): 0, ('C', 'Z'): 3}

    return sum(mps[m2]+outcomes[(m1, m2)] for m1, m2 in games)


def day_2b():
    with open(r'inputs/DAY_2.txt') as infile:
        data = infile.read().split('\n')
    games = [tuple((i[0], i[-1])) for entry in data[:-1] for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    points = {'X': 0, 'Y': 3, 'Z': 6}
    outcomes = {('A', 'X'): 'Z', ('A', 'Y'): 'X', ('A', 'Z'): 'Y',
                ('B', 'X'): 'X', ('B', 'Y'): 'Y', ('B', 'Z'): 'Z',
                ('C', 'X'): 'Y', ('C', 'Y'): 'Z', ('C', 'Z'): 'X'}

    return sum(points[j]+mps[outcomes[(i, j)]] for i, j in games)


def day_3a():
    priorities = dict(zip(ascii_lowercase+ascii_uppercase, range(1, 53)))
    with open('inputs/DAY_3.txt') as infile:
        data = infile.readlines()
    return sum(sum(priorities[i] for i in set(e[:len(e)//2]).intersection(set(e[(len(e)//2):]))) for e in data)


def day_3b():
    priorities = dict(zip(ascii_lowercase + ascii_uppercase, range(1, 53)))
    with open('inputs/DAY_3.txt') as infile:
        data = infile.read().split('\n')

    sum_ = 0
    for i in range(0, len(data)-1, 3):
        set_ = set(data[i])
        for j in data[i:i+3]:
            set_ = set_.intersection(j)
        sum_ += priorities[set_.pop()]
    return sum_


if __name__ == '__main__':
    print(DELIMITER)
    print(f'Day_1A={day_1()}')
    print(f'Day_1B={day_1(part="B")}')
    print(DELIMITER)
    print(f'DAY_2A={day_2a()}')
    print(f'DAY_2B={day_2b()}')
    print(DELIMITER)
    print(f'DAY_3A={day_3a()}')
    print(f'DAY_3A={day_3b()}')
    print(DELIMITER)
