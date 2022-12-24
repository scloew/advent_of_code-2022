import re

from classes import SensorBeacon


def fetch_input(day, delim='\n'):
    with open(f'inputs\\Day_{day}.txt') as infile:
        return infile.read().split(delim)[:-1]


def get_day5_data():
    with open(r'inputs/Day_5.txt') as infile:
        init_state, cmds = infile.read().split('\n\n')

    stacks = [[] for _ in range(9)]
    for line in init_state.split('\n')[:-1]:
        index = 0
        for i in range(1, len(line), 4):
            stacks[index].append(line[i])
            index += 1

    stacks = [[i for i in stack[::-1] if not i == ' '] for stack in stacks]
    return stacks, cmds.split('\n')[:-1]


def rotate_grid(grid):
    return [list(reversed(x)) for x in zip(*grid)]


def check_tree_visibility(grid, visible_trees):
    for i, row in enumerate(grid):
        max_hgt = chr(ord('0') - 1)
        for j, hgt in enumerate(row):
            if max_hgt < hgt:
                visible_trees[i][j] = True
                max_hgt = hgt


def update_scenic_score(grid, trees_visibility, direction):
    for i, row in enumerate(grid):
        stack = [(row[0], 0)]
        for j, val in enumerate(row[1:]):
            inc_val = 1
            while stack and stack[-1][0] < val:
                inc_val += stack[-1][1]
                stack.pop()
            trees_visibility[i][j + 1].increment(direction, inc_val)
            stack.append((val, inc_val))


def get_day_9_sign_and_index(cmd):
    if cmd in {'U', 'D'}:
        sign, index = 1 if cmd == 'U' else -1, 0
    else:
        sign, index = 1 if cmd == 'R' else -1, 1
    return sign, index


def is_adjacent(head, tail):
    incs = tuple((i, j) for j in range(-1, 2) for i in range(-1, 2))
    y, x = head
    yt, xt = tail
    for yi, xi in incs:
        if (yt + yi, xt + xi) == (y, x):
            return True
    return False


def move_tail(head, tail):
    _move_diagonal(head, tail) if not (head[0] == tail[0] or head[1] == tail[1]) else _move_linear(head, tail)


def _move_diagonal(head, tail):
    incs = ((i, j) for j in range(-1, 2) for i in range(-1, 2) if abs(i) == abs(j))
    _move(head, tail, incs)


def _move_linear(head, tail):
    incs = ((i, j) for j in range(-1, 2) for i in range(-1, 2) if not abs(i) == abs(j))
    _move(head, tail, incs)


def _move(head, tail, incs):
    for yi, xi in incs:
        tail[0] += yi
        tail[1] += xi
        if is_adjacent(head, tail):
            return
        tail[0] -= yi
        tail[1] -= xi


def move_rope(rope, visited):
    if is_adjacent(rope[0], rope[1]):
        return
    for i, point in enumerate(rope[1:]):
        if not is_adjacent(rope[i], point):
            move_tail(rope[i], point)
    visited.add(tuple(rope[-1]))


def process_monkeys(monkeys, num_rounds=20):
    for i in range(num_rounds):
        for j, m in enumerate(monkeys):
            for new_m, worry in m.handle_items():
                monkeys[new_m].items.append(worry)
    monkeys.sort(key=lambda x: x.handled_cnt)
    return monkeys[-1].handled_cnt * monkeys[-2].handled_cnt


def bfs(grid, target, to_search=None, hgt_limit=1):
    to_search = [(0, 0)] if to_search is None else to_search
    incs = tuple(tuple([i, j]) for i in range(-1, 2) for j in range(-1, 2) if not abs(i) == abs(j))
    seen, count = set(to_search), -1

    while to_search:
        count += 1
        next_search = []
        for y, x in to_search:
            if grid[y][x] == target:
                return y, x, count
            for yi, xi in incs:
                yp, xp = y + yi, x + xi
                continue_ = 0 <= yp < len(grid) and 0 <= xp < len(grid[0])
                if not continue_:
                    continue
                hgt0, hgt1 = 'a' if grid[y][x] == 'S' else grid[y][x], 'z' if grid[yp][xp] == 'E' else grid[yp][xp]
                if ord(hgt1) - ord(hgt0) <= hgt_limit and (yp, xp) not in seen:
                    seen.add((yp, xp))
                    next_search.append((yp, xp))
        to_search = next_search
    return None, None, None


def parse_day_13_input():
    with open(r'inputs/Day_13.txt') as infile:
        data = infile.read().split('\n\n')
    for pair in data:
        p0, p1, *_ = pair.split('\n')
        yield _parse_day_13_line(p0), _parse_day_13_line(p1)


def _parse_day_13_line(line):
    stack, index, temp = [[]], 0, ''
    while index < len(line):
        c = line[index]
        if c == ',' and temp:
            stack[-1].append(int(temp))
            temp = ''
        elif c == '[':
            stack.append([])
        elif c == ']':
            if temp:
                stack[-1].append(int(temp))
                temp = ''
            stack[-2].append(stack[-1])
            stack.pop()
        elif not c == ',':
            temp += c
        index += 1
    return stack.pop().pop()


def is_valid_packet(packet1, packet2):
    for i, v in enumerate(packet1):
        if len(packet2) == i:
            return False
        if v == packet2[i]:
            continue
        if isinstance(v, int) and isinstance(packet2[i], int):
            return v < packet2[i]
        elif isinstance(v, list) and isinstance(packet2[i], list):
            return is_valid_packet(v, packet2[i])
        elif isinstance(v, list):
            return is_valid_packet(v, [packet2[i]])
        else:
            return is_valid_packet([v], packet2[i])
    return True


def parse_day_14_input():
    data, rocks = fetch_input(14), set()
    for line in data:
        for set_ in _parse_day_14_line(line):
            rocks = rocks.union(set_)
    return rocks


def _parse_day_14_line(line):
    rocks = line.split(' -> ')
    for i, entry in enumerate(rocks[:-1]):
        x, y = _day_14_get_start_stop(entry)
        x1, y1 = _day_14_get_start_stop(rocks[i + 1])
        if x == x1:
            first, last = (y, y1) if y < y1 else (y1, y)
            yield {(x, yi) for yi in range(first, last + 1)}
        else:
            first, last = (x, x1) if x < x1 else (x1, x)
            yield {(xi, y) for xi in range(first, last + 1)}


def _day_14_get_start_stop(entry):
    x, y = entry.split(',')
    return int(x), int(y)


def move_sand(barriers, x_bounds, y_max):
    incs, x, y, moved = ((0, 1), (-1, 1), (1, 1)), 500, 0, True
    while x in x_bounds and y <= y_max and moved:
        moved = False
        for xi, yi in incs:
            if (x + xi, y + yi) in barriers:
                continue
            elif x + xi not in x_bounds or y + yi >= y_max:
                return False
            else:
                x += xi
                y += yi
                moved = True
                break
    barriers.add((x, y))
    return True


def move_sand_part_b(barriers, y_max):
    incs, x, y, moved = ((0, 1), (-1, 1), (1, 1)), 500, 0, True
    while moved:
        moved = False
        for xi, yi in incs:
            if (x + xi, y + yi) in barriers:
                continue
            elif y + yi == y_max - 1:
                barriers.add((x+xi, y+yi))
                return
            else:
                x += xi
                y += yi
                moved = True
                break
    barriers.add((x, y))


def parse_day_15_input():
    data = fetch_input(15)
    return [_parse_day_15_line(line) for line in data]


def _parse_day_15_line(line):
    regex = r'-?\d+'
    return SensorBeacon(*[int(i) for i in re.findall(regex, line)])

