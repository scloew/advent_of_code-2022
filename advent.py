"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""
import functools
from math import lcm
import re
from string import ascii_lowercase, ascii_uppercase

from classes import FileSystemObject, ScenicScore, Monkey
from utils import (fetch_input, get_day5_data,
                   rotate_grid, check_tree_visibility,
                   update_scenic_score, get_day_9_sign_and_index,
                   move_rope, process_monkeys, bfs,
                   parse_day_13_input, is_valid_packet, parse_day_14_input,
                   move_sand, move_sand_part_b, parse_day_15_input)


def day_1(part='a'):
    """
    :param part: for polymorphism; 'A' for part A 'B' for B
    :return:
    """
    data = fetch_input(1, '\n\n')

    cals = [sum(int(i) for i in entry.split('\n')) for entry in data]
    cals.sort()
    return sum(cals[-1 if part.lower() == 'a' else -3:])


def day_2(part='a'):
    data = fetch_input(2)
    return day_2a(data) if part.lower() == 'a' else day_2b(data)


def day_2a(data):
    games = [tuple((i[0], i[-1])) for entry in data for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    outcomes = {('A', 'X'): 3, ('A', 'Y'): 6, ('A', 'Z'): 0,
                ('B', 'X'): 0, ('B', 'Y'): 3, ('B', 'Z'): 6,
                ('C', 'X'): 6, ('C', 'Y'): 0, ('C', 'Z'): 3}

    return sum(mps[m2] + outcomes[(m1, m2)] for m1, m2 in games)


def day_2b(data):
    games = [tuple((i[0], i[-1])) for entry in data for i in entry.split('\n')]

    mps = {'X': 1, 'Y': 2, 'Z': 3}
    points = {'X': 0, 'Y': 3, 'Z': 6}
    outcomes = {('A', 'X'): 'Z', ('A', 'Y'): 'X', ('A', 'Z'): 'Y',
                ('B', 'X'): 'X', ('B', 'Y'): 'Y', ('B', 'Z'): 'Z',
                ('C', 'X'): 'Y', ('C', 'Y'): 'Z', ('C', 'Z'): 'X'}

    return sum(points[j] + mps[outcomes[(i, j)]] for i, j in games)


def day_3(part='a'):
    return day_3a() if part.lower() == 'a' else day_3b()


def day_3a():
    priorities = dict(zip(ascii_lowercase + ascii_uppercase, range(1, 53)))
    with open('inputs/Day_3.txt') as infile:
        data = infile.readlines()
    return sum(sum(priorities[i] for i in set(e[:len(e) // 2]).intersection(set(e[(len(e) // 2):]))) for e in data)


def day_3b():
    priorities = dict(zip(ascii_lowercase + ascii_uppercase, range(1, 53)))
    with open('inputs/Day_3.txt') as infile:
        data = infile.read().split('\n')

    sum_ = 0
    for i in range(0, len(data) - 1, 3):
        set_ = set(data[i])
        for j in data[i + 1:i + 3]:
            set_ = set_.intersection(j)
        sum_ += priorities[set_.pop()]
    return sum_


def day_4(part='a'):
    data = fetch_input(4)
    return day_4a(data) if part.lower() == 'a' else day_4b(data)


def day_4a(data):
    count_ = 0
    for entry in data:
        e1, e2 = entry.split(',')
        e1, e2 = e1.split('-'), e2.split('-')
        start1, stop1 = int(e1[0]), int(e1[1])
        start2, stop2 = int(e2[0]), int(e2[1])
        if start1 <= start2 <= stop2 <= stop1 or start2 <= start1 <= stop1 <= stop2:
            count_ += 1
    return count_


def day_4b(data):
    count_ = 0
    for entry in data:
        e1, e2 = entry.split(',')
        e1, e2 = e1.split('-'), e2.split('-')
        start1, stop1 = int(e1[0]), int(e1[1])
        s1 = set(range(start1, stop1 + 1))
        start2, stop2 = int(e2[0]), int(e2[1])
        s2 = set(range(start2, stop2 + 1))

        if s1.intersection(s2):
            count_ += 1
    return count_


def day_5(part='a'):
    stacks, cmds = get_day5_data()

    def move(command):
        num, src, dest = re.findall(r'\d+', command)
        num, src, dest = int(num), int(src) - 1, int(dest) - 1
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
        if len(set(data[i:i + offset])) == offset:
            return i + offset


def day_7(part='a'):
    data = fetch_input(7)[2:]
    fso = FileSystemObject.from_string_list(data)
    return fso.calc_dirs_size_under_lim() if part.lower() == 'a' else fso.smallest_dir_to_make_space()


def day_8(part='a'):
    data = fetch_input(8)
    return day_8a(data) if part.lower() == 'a' else day_8b(data)


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


def day_9(part='a'):
    data = [tuple(i for i in row.split(' ')) for row in fetch_input(9)]
    size = 2 if part.lower() == 'a' else 10
    visited, rope = {(0, 0)}, [[0, 0] for _ in range(size)]
    for cmd, mag in data:
        sign, index = get_day_9_sign_and_index(cmd)
        for _ in range(int(mag)):
            rope[0][index] += sign
            move_rope(rope, visited)
    return len(visited)


def day_10(part='a'):
    data = fetch_input(10)
    return day_10a(data) if part.lower() == 'a' else day_10b(data)


def day_10a(data):
    signal_strength, x = 0, 1
    check_cycle, cycle_increment, cycle = 20, 40, 0
    for line in data:
        cycle += 1
        if cycle == check_cycle:
            signal_strength += x * cycle
            check_cycle += cycle_increment
        if not line == 'noop':
            cycle += 1
            if cycle == check_cycle:
                signal_strength += x * cycle
                check_cycle += cycle_increment
            x += int(line.split()[-1])
    return signal_strength


def day_10b(data):
    cycle, x, screen = 0, 1, []
    for line in data:
        pixel = '#' if x - 1 <= cycle <= x + 1 else ' '
        screen.append(pixel)
        if len(screen) == 40:
            print(''.join(screen))
            screen = []
        cycle += 1
        cycle %= 40
        if not line == 'noop':
            pixel = '#' if x - 1 <= cycle <= x + 1 else ' '
            screen.append(pixel)
            if len(screen) == 40:
                print(''.join(screen))
                screen = []
            cycle += 1
            x += int(line.split(' ')[-1])
        cycle %= 40


def day_11(part='a'):
    with open(r'inputs\Day_11.txt') as infile:
        data = infile.read().split('\n\n')
    monkeys = [Monkey.from_string(row) for row in data]
    if part.lower() == 'a':
        rounds = 20
    else:
        rounds = 10_000
        lcm_ = lcm(*(m.div for m in monkeys))
        for m in monkeys:
            m.adjust_interest = lambda x: x % lcm_
    return process_monkeys(monkeys, num_rounds=rounds)


def day_12(part='a'):
    data = fetch_input(12)
    y, x, _ = bfs(data, 'S', hgt_limit=1000)
    to_search = [(y, x)]
    if not part.lower() == 'a':
        for yi, row in enumerate(data):
            for xi, v in enumerate(row):
                if v == 'a':
                    to_search.append((yi, xi))
    y1, x1, count = bfs(data, 'E', to_search=to_search)
    return count


def day_13(part='a'):
    data = parse_day_13_input()
    return day_13a(data) if part.lower() == 'a' else day_13b(data)


def day_13a(data):
    count = 0
    for i, (x, y) in enumerate(data):
        if is_valid_packet(x, y):
            count += (i + 1)
    return count


def day_13b(data):
    divider1, divider2 = [[2]], [[6]]
    adjusted_data = []
    for x, y in data:
        adjusted_data.append(x)
        adjusted_data.append(y)
    adjusted_data.append(divider1)
    adjusted_data.append(divider2)
    adjusted_data.sort(key=functools.cmp_to_key(lambda p1, p2: -1 if is_valid_packet(p1, p2) else 1))
    return (adjusted_data.index(divider1) + 1) * (adjusted_data.index(divider2) + 1)


def day_14(part='a'):
    barriers = parse_day_14_input()
    y_max = max(i[1] for i in barriers)
    return day_14a(barriers, y_max) if part.lower() == 'a' else day_14b(barriers, y_max)


def day_14a(barriers, y_max):
    x_bounds, count = range(min(barriers)[0], max(barriers)[0] + 1), 0
    while move_sand(barriers, x_bounds, y_max):
        count += 1
    return count


def day_14b(barriers, y_max):
    count, end_point = 0, {(500, 0)}
    y_max += 2
    while not barriers.issuperset(end_point):
        move_sand_part_b(barriers, y_max)
        count += 1
    return count


def day_15(y_index=2_000_000):
    sensor_beacons = parse_day_15_input()
    not_beacons = set()
    for i, v in enumerate(sensor_beacons):
        y_distance = abs(v.y - y_index)
        x_distance = (abs(v.x - v.xb) + abs(v.y - v.yb)) - y_distance
        set_ = {j for j in range(v.x, v.x + x_distance + 1)}
        set_ = set_.union({j for j in range(v.x, v.x - x_distance - 1, -1)})
        not_beacons = not_beacons.union(set_)
    return len(not_beacons) - 1


def day_18():
    droplets = {tuple(int(i) for i in line.split(',')) for line in fetch_input(18)}
    incs = ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
            (0, -1, 0), (0, 0, 1), (0, 0, -1))
    return sum(1 for x, y, z in droplets for xi, yi, zi in incs if (x+xi, y+yi, z+zi) not in droplets)


if __name__ == '__main__':
    DELIMITER = '\n===============\n'

    print(DELIMITER)
    print(f'Day_1A={day_1()}')
    print(f'Day_1B={day_1(part="b")}')
    print(DELIMITER)
    print(f'DAY_2A={day_2()}')
    print(f'DAY_2B={day_2(part="b")}')
    print(DELIMITER)
    print(f'DAY_3A={day_3()}')
    print(f'DAY_3A={day_3(part="b")}')
    print(DELIMITER)
    print(f'DAY_4A={day_4()}')
    print(f'DAY_4B={day_4(part="b")}')
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
    print(f'DAY_9A={day_9()}')
    print(f'DAY_9B={day_9(part="b")}')
    print(DELIMITER)
    print(f'DAY_10A={day_10()}')
    print('DAY_10B=')
    day_10(part="b")
    print(DELIMITER)
    print(f'DAY_11A={day_11()}')
    print(f'DAY_11B={day_11(part="b")}')
    print(DELIMITER)
    print(f'DAY_12A={day_12()}')
    print(f'DAY_12B={day_12(part="b")}')
    print(DELIMITER)
    print(f'DAY_13A={day_13()}')
    print(f'DAY_13B={day_13(part="b")}')
    print(DELIMITER)
    print(f'DAY_14A={day_14()}')
    print(f'DAY_14B={day_14(part="b")}')
    print(DELIMITER)
    print(f'DAY_15A={day_15()}')
    # print(f'DAY_15B={day_15(part="b")}')
    print(DELIMITER)
    print(f'DAY_18A={day_18()}')
    # print(f'DAY_18B={day_18(part="b")}')
    print(DELIMITER)
