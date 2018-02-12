import aoc_utils
import re
from collections import Counter
from functools import cmp_to_key
from string import ascii_lowercase

def count_compare(c1, c2):
    if c1[1] == c2[1]:
        return ord(c1[0]) - ord(c2[0])
    else:
        return c2[1] - c1[1]

def tr(amnt):
    def f(c):
        if c == '-':
            return ' '
        elif c in ascii_lowercase:
            i = ord(c) - ord('a')
            i = (i + amnt) % 26 + ord('a')
            return chr(i)
        else:
            return c
    return f


class Room:
    raw = None
    counts = None
    sector = None
    cs = None

    def __init__(self, s):
        parts = re.split('[\-\[\]]', s)
        self.raw = s
        self.counts = Counter(list(''.join(parts[:-3])))
        self.sector = int(parts[-3])
        self.cs = parts[-2]

    def valid(self):
        sort_items = sorted(self.counts.items(), key=cmp_to_key(count_compare))
        calc_sum = ''.join(list(map(lambda x: x[0], sort_items)))[:5]
        return calc_sum == self.cs

    def shift(self):
        return ''.join(list(map(tr(self.sector), list(self.raw))))

    def __repr__(self):
        return self.raw
        

def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    rooms = map(lambda x: Room(x), input)
    valid = list(filter(lambda x: x.valid(), rooms))
    print(sum(map(lambda x: x.sector, valid)))
    for v in valid:
        s = v.shift()
        if 'north' in s and 'pole' in s:
            print(s)

if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
