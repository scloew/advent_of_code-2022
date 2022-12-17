from collections import defaultdict
import re
from operator import add, sub, mul


from numpy import prod


class FileSystemObject:

    def __init__(self, parent, name):
        self.name, self.parent, self.dirs, self.files_size = name, parent, {}, 0

    def __str__(self):
        return f'\tname={self.name} ' \
               f'\n\tparent={self.parent.name if self.parent is not None else None} ' \
               f'\n\tdirs={[k for k in self.dirs]} size={self.files_size}'

    def calc_dirs_size_under_lim(self, limit_=100_000):
        return sum(i for i in self._calc_dirs_sizes() if i <= limit_)

    def calc_total_size(self):
        return max(self._calc_dirs_sizes())

    def smallest_dir_to_make_space(self, capacity=70_000_000, needed=30_000_000):
        needed = needed - (capacity - self.calc_total_size())
        min_ = capacity
        for i in self._calc_dirs_sizes():
            if needed < i:
                min_ = min(min_, i)
        return min_

    def _calc_dirs_sizes(self):

        def calc_dir_size(fso, sizes=None):
            if sizes is None:
                sizes = []
            dir_size = fso.files_size + sum((calc_dir_size(file_sys_obj, sizes) for
                                             file_sys_obj in fso.dirs.values()))
            sizes.append(dir_size)
            return dir_size

        dir_sizes = []
        calc_dir_size(self, dir_sizes)
        return dir_sizes

    @classmethod
    def from_string_list(cls, data):
        cd = cls(None, '/')
        tld = cd
        for line in data:
            if '$ ls' in line:
                continue
            if line == '$ cd ..':
                cd = cd.parent
            elif '$ cd' in line:
                dir_ = line.split(' ')[-1]
                cd = cd.dirs[dir_]
            elif 'dir' == line.split(' ')[0]:
                name = line.split(' ')[-1]
                cd.dirs[name] = cls(parent=cd, name=name)
            else:
                cd.files_size += int(line.split(' ')[0])

        return tld


class ScenicScore:

    def __init__(self):
        self.tree_visibility = defaultdict(int)

    def increment(self, direction, val=1):
        self.tree_visibility[direction] += val

    def calc_score(self):
        return prod([val for val in self.tree_visibility.values()])


class Monkey:

    def __init__(self, items, op, divisor, true_monkey, false_monkey):
        self.items, self.op, self.div = items, op, divisor
        self.true_monkey, self.false_monkey = true_monkey, false_monkey
        self.handled_cnt = 0

    # TODO: double check this function and add logic for monkeys taking a round
    def handle_items(self):
        self.handled_cnt += len(self.items)
        for worry in self.items:
            new_worry = self.op(worry) // 3
            yield self.true_monkey if not new_worry % self.div else self.false_monkey, new_worry
        self.items = []

    @classmethod
    def from_string(cls, string_):
        data = string_.rstrip().split('\n')[1:]
        ops = {'+': add, '-': sub, '*': mul}
        items = [int(i) for i in re.findall(r'\d+', data[0])]
        op, val = data[1].split(' ')[-2:]
        lam = lambda x: ops[op](x, x) if val == 'old' else ops[op](x, int(val))
        div = int(re.findall(r'\d+', data[2])[0])
        true_m, false_m = int(data[-2].split(' ')[-1]), int(data[-1].split(' ')[-1])
        return cls(items, lam, div, true_m, false_m)

