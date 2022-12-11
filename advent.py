"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""
import re
from string import ascii_lowercase, ascii_uppercase

from classes import FileSystemObject, ScenicScore
from utils import (fetch_input, get_day5_data,
                   rotate_grid, check_tree_visibility,
                   update_scenic_score)


def day_1(part='a'):
    """
    :param part: for polymorphism; 'A' for part A 'B' for B
    :return:
    """
    data = fetch_input(1, '\n\n')

    cals = [sum(int(i) for i in entry.split('\n')) for entry in data]
    cals.sort()
    return sum(cals[-1 if part.lower() == 'a' else -3:])


def day_2a():
    data = fetch_input(2)
    games = [tuple((i[0], i[-1])) for entry in data for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    outcomes = {('A', 'X'): 3, ('A', 'Y'): 6, ('A', 'Z'): 0,
                ('B', 'X'): 0, ('B', 'Y'): 3, ('B', 'Z'): 6,
                ('C', 'X'): 6, ('C', 'Y'): 0, ('C', 'Z'): 3}

    return sum(mps[m2]+outcomes[(m1, m2)] for m1, m2 in games)


def day_2b():
    data = fetch_input(2)
    games = [tuple((i[0], i[-1])) for entry in data for i in entry.split('\n')]

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
    data = fetch_input(4)

    count_ = 0
    for entry in data:
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

    def move(command):
        num, src, dest = re.findall(r'\d+', command)
        num, src, dest = int(num), int(src)-1, int(dest)-1
        reverse = -1 if part.lower() == 'a' else 1
        stacks[dest].extend(stacks[src][-num:][::reverse])
        del stacks[src][-num:]

    for cmd in cmds:
        move(cmd)

    return ''.join(stack[-1] for stack in stacks)


def day_6(part='a'):
    with open(r'inputs\Day_6.txt') as infile:
        data = infile.read()[:-1]

    offset = 4 if part.lower() == 'a' else 14

    for i, v in enumerate(data):
        if len(set(data[i:i+offset])) == offset:
            return i+offset


def day_7(part='a'):
    data = fetch_input(7)[2:]
    fso = FileSystemObject.from_string_list(data)
    if part.lower() == 'a':
        return fso.calc_dirs_size_under_lim()
    else:
        return fso.smallest_dir_to_make_space()


def day_8(part='a'):
    data = fetch_input(8)
    if part.lower() == 'a':
        return day_8a(data)
    else:
        return day_8b(data)


def day_8a(data):
    visible_trees = [[False for _ in row] for row in data]

    for _ in range(4):
        check_tree_visibility(data, visible_trees)
        data = rotate_grid(data)
        visible_trees = rotate_grid(visible_trees)

    return sum(sum(i for i in row if i) for row in visible_trees)


def day_8b(data):
    trees_visibility = [[ScenicScore() for _ in _] for _ in data]

    for direction in ['left', 'down', 'right', 'up']:
        update_scenic_score(data, trees_visibility, direction)
        data = rotate_grid(data)
        trees_visibility = rotate_grid(trees_visibility)

    return max(max(score.calc_score() for score in row) for row in trees_visibility)


if __name__ == '__main__':
    DELIMITER = '\n===============\n'

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
    print(f'DAY_6A={day_6()}')
    print(f'DAY_6B={day_6(part="b")}')
    print(DELIMITER)
    print(f'DAY_7A={day_7()}')
    print(f'DAY_7B={day_7(part="b")}')
    print(DELIMITER)
    print(f'DAY_8A={day_8()}')
    print(f'DAY_8B={day_8(part="b")}')
    print(DELIMITER)
