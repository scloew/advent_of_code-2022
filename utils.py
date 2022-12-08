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
