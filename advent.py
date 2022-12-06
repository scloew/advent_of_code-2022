"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""
from string import ascii_lowercase, ascii_uppercase
import re

from utils import get_day5_data


DELIMITER = '\n===============\n'


def day_1(part='a'):
    """
    :param part: for polymorphism; 'A' for part A 'B' for B
    :return:
    """
    with open(r'inputs/Day_1.txt') as infile:
        data = infile.read().split('\n\n')

    cals = [sum(int(i) for i in entry.split('\n')) for entry in data[:-1]]
    cals.sort()
    return sum(cals[-1 if part.lower() == "a" else -3:])


def day_2a():
    with open(r'inputs/Day_2.txt') as infile:
        data = infile.read().split('\n')
    games = [tuple((i[0], i[-1])) for entry in data[:-1] for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    outcomes = {('A', 'X'): 3, ('A', 'Y'): 6, ('A', 'Z'): 0,
                ('B', 'X'): 0, ('B', 'Y'): 3, ('B', 'Z'): 6,
                ('C', 'X'): 6, ('C', 'Y'): 0, ('C', 'Z'): 3}

    return sum(mps[m2]+outcomes[(m1, m2)] for m1, m2 in games)


def day_2b():
    with open(r'inputs/Day_2.txt') as infile:
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
    with open('inputs/Day_3.txt') as infile:
        data = infile.readlines()
    return sum(sum(priorities[i] for i in set(e[:len(e)//2]).intersection(set(e[(len(e)//2):]))) for e in data)


def day_3b():
    priorities = dict(zip(ascii_lowercase + ascii_uppercase, range(1, 53)))
    with open('inputs/Day_3.txt') as infile:
        data = infile.read().split('\n')

    sum_ = 0
    for i in range(0, len(data)-1, 3):
        set_ = set(data[i])
        for j in data[i+1:i+3]:
            set_ = set_.intersection(j)
        sum_ += priorities[set_.pop()]
    return sum_


def day_4a():
    with open('inputs/DAY_4.txt') as infile:
        data = infile.read().split('\n')

    count_ = 0
    for entry in data[:-1]:
        e1, e2 = entry.split(',')
        e1, e2 = e1.split('-'), e2.split('-')
        start1, stop1 = int(e1[0]), int(e1[1])
        start2, stop2 = int(e2[0]), int(e2[1])
        if start1 <= start2 <= stop2 <= stop1 or start2 <= start1 <= stop1 <= stop2:
            count_ += 1
    return count_


def day_4b():
    with open('inputs/DAY_4.txt') as infile:
        data = infile.read().split('\n')

    count_ = 0
    for entry in data[:-1]:
        e1, e2 = entry.split(',')
        e1, e2 = e1.split('-'), e2.split('-')
        start1, stop1 = int(e1[0]), int(e1[1])
        s1 = set(range(start1, stop1+1))
        start2, stop2 = int(e2[0]), int(e2[1])
        s2 = set(range(start2, stop2+1))

        if s1.intersection(s2):
            count_ += 1
    return count_


def day_5(part='a'):
    stacks, cmds = get_day5_data()

    def move(cmd):
        num, src, dest = re.findall(r'\d+', cmd)
        num, src, dest = int(num), int(src)-1, int(dest)-1
        if part.lower() == 'a':
            stacks[dest].extend(stacks[src][-num:][::-1])
        else:
            stacks[dest].extend(stacks[src][-num:])
        del stacks[src][-num:]

    for cmd in cmds:
        move(cmd)

    return ''.join(stack[-1] for stack in stacks)


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
    print(f'DAY_4A={day_4a()}')
    print(f'DAY_4B={day_4b()}')
    print(DELIMITER)
    print(f'DAY_5A={day_5()}')
    print(f'DAY_5B={day_5(part="b")}')
    print(DELIMITER)
