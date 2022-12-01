"""
Solutions to 2022 advent of code
https://adventofcode.com/
"""
DELIMITER = '\n===============\n'


def day_1(part='A'):
    """
    :param part: for polymorphism; 'A' for part A 'B' for B
    :return:
    """
    with open(r'inputs/DAY_1A.txt') as infile:
        data = infile.read().split('\n\n')

    cals = [sum(int(i) for i in entry.split('\n')) for entry in data[:-1]]
    cals.sort()
    return sum(cals[-1 if part.lower() == "a" else -3:])


if __name__ == '__main__':
    print(f'Day_1A={day_1()}')
    print(f'Day_2A={day_1(part="B")}')
    print(DELIMITER)