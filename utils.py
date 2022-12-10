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
        visible_trees[i][0], max_hgt = True, row[0]
        for j, hgt in enumerate(row):
            if max_hgt < hgt:
                visible_trees[i][j] = True
                max_hgt = hgt


def update_scenic_score(grid, trees_visiblity, directions):
    return NotImplemented