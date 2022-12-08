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

    def smallest_dir_over_limit(self, capacity=70_000_000, needed=30_000_000):
        needed = needed - (capacity-44795677)
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

        sizes = []
        calc_dir_size(self, sizes)
        return sizes

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
