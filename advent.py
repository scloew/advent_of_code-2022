"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""


def day_1():
    with open(r'inputs/DAY_1A.txt') as infile:
        data = infile.read().split('\n\n')

    for entry in data[:-1]:
        max_ = max(max_, sum(int(i) for i in entry.split('\n')))
    max_ = max(sum(int(i) for i in entry.split('\n')) for entry in data[:-1])
    print(f'DAY_1A={max_}')
    return max_


if __name__ == '__main__':
    day_1()
