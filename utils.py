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
        max_hgt = chr(ord('0')-1)
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
            trees_visibility[i][j+1].increment(direction, inc_val)
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
        if (yt + yi, xt+xi) == (y, x):
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
    if to_search is None:
        to_search = [(0, 0)]
    incs = tuple(tuple([i, j]) for i in range(-1, 2) for j in range(-1, 2) if not abs(i) == abs(j))
    seen = set(to_search)

    count = -1
    while to_search:
        count += 1
        next_search = []
        for y, x in to_search:
            if grid[y][x] == target:
                return y, x, count
            for yi, xi in incs:
                yp, xp = y+yi, x+xi
                continue_ = 0 <= yp < len(grid) and 0 <= xp < len(grid[0])
                if not continue_:
                    continue
                hgt0, hgt1 = 'a' if grid[y][x] == 'S' else grid[y][x], 'z' if grid[yp][xp] == 'E' else grid[yp][xp]
                continue_ &= ord(hgt1)-ord(hgt0) <= hgt_limit
                if continue_ and (yp, xp) not in seen:
                    seen.add((yp, xp))
                    next_search.append((yp, xp))
        to_search = next_search

    return None, None, None
