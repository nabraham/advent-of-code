import aoc_utils
from functools import reduce
from collections import namedtuple
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import re

Vein = namedtuple('Vein', ['min_x', 'max_x', 'min_y', 'max_y'])


class Tap:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def move_down(self, grid):
        while len(grid) > self.y + 1 and grid[self.y + 1][self.x] == '.':
            grid[self.y][self.x] = '|'
            self.y += 1
            grid[self.y][self.x] = '|'

    def fill_left(self, grid):
        if self.y + 1 == len(grid):
            return 'X'
        while self.x > 0 and grid[self.y][self.x - 1] in '|.' and grid[self.y + 1][self.x] in '#~':
            self.x -= 1
            grid[self.y][self.x] = '|'

        if self.x == 0:
            return '#', (self.x, self.y)
        return grid[self.y][self.x - 1], (self.x, self.y)

    def fill_right(self, grid, start_at_x=None):
        if self.y + 1 == len(grid):
            return 'X'
        if start_at_x is not None:
            self.x = start_at_x
        while self.x + 1 < len(grid[self.y]) and grid[self.y][self.x + 1] in '|.' and grid[self.y + 1][self.x] in '#~':
            self.x += 1
            grid[self.y][self.x] = '|'

        if self.x + 1 == len(grid[self.y]):
            return '#', (self.x, self.y)
        else:
            return grid[self.y][self.x + 1], (self.x, self.y)

    def __repr__(self):
        return '(%d,%d)' % (self.x, self.y)


def min_max(part):
    range_parts = part.split('=')[1].split('..')
    return int(range_parts[0]), int(range_parts[-1])


def parse_vein(line):
    parts = line.split(', ')
    x, y = sorted(parts, key=lambda z: z[0])
    min_x, max_x = min_max(x)
    min_y, max_y = min_max(y)
    return Vein(min_x, max_x, min_y, max_y)


def create_grid(veins, min_x, max_x, min_y, max_y):
    g = []
    for i in range(max_y + 1):
        row = []
        for j in range(min_x, max_x + 1):
            row.append('.')
        g.append(row)

    g[0][500 - min_x] = '+'
    for v in veins:
        for x in range(v.min_x, v.max_x + 1):
            for y in range(v.min_y, v.max_y + 1):
                g[y][x - min_x] = '#'

    return g


def print_grid(g, taps=[]):
    rez = ''
    tap_set = set(map(lambda x: '%d,%d' % (x.x, x.y), taps))
    for i, row in enumerate(g):
        for j, col in enumerate(row):
            key = '%d,%d' % (j, i)
            if key in tap_set:
                rez += '+'
            else:
                rez += col
        rez += '\n'
    print(rez)


def score_grid(g):
    flat = reduce(lambda x, y: x + y, g, [])
    return {'~': flat.count('~'), '|': flat.count('|')}


def fill_between(g, p1, p2, symbol):
    for x in range(p1[0], p2[0] + 1):
        g[p1[1]][x] = symbol


def print_bounds(grid, pad=100):
    contains_water = map(lambda x: [0, x[0]]['~' in x[1] or '|' in x[1]], enumerate(grid))
    max_y = max(contains_water) + pad
    min_y = max_y - 2 * pad
    return max(0, min_y), min(len(grid), max_y)


def run_sim(lines):
    veins = [parse_vein(line) for line in lines]
    min_x = min(map(lambda x: x.min_x, veins)) - 2
    max_x = max(map(lambda x: x.max_x, veins)) + 2
    min_y = min(map(lambda x: x.min_y, veins))
    max_y = max(map(lambda x: x.max_y, veins))
    grid = create_grid(veins, min_x, max_x, 0, max_y)
    taps = {Tap(500 - min_x, 0)}
    while len(taps) > 0:
        new_taps = set([])
        for t in taps:
            t.move_down(grid)
            # print_grid(grid, taps)
            float_up = (t.y + 1) < len(grid) and grid[t.y + 1][t.x] in '~#'
            stopped_at = t.x
            while float_up:
                stop_left = t.fill_left(grid)
                stop_right = t.fill_right(grid, stopped_at)
                # print(t, 'filling between', stop_left, stop_right)
                if stop_left[0] == '#' and stop_right[0] == '#':
                    fill_between(grid, stop_left[1], stop_right[1], '~')
                    t.y -= 1
                    t.x = stopped_at
                elif stop_left[0] == 'X':
                    float_up = False
                    grid[t.y][t.x] = '|'
                else:
                    float_up = False
                    fill_between(grid, stop_left[1], stop_right[1], '|')
                    if stop_left[0] not in '#|':
                        new_taps.add(Tap(stop_left[1][0], stop_left[1][1]))
                    if stop_right[0] not in '#|':
                        new_taps.add(Tap(stop_right[1][0], stop_right[1][1]))
        filtered = filter(lambda x: x not in taps, new_taps)
        taps = set(filtered)
        # print_image(grid, print_bounds(grid, 200))
    # print_grid(grid)
    return score_grid(grid), min_y, grid


def print_image(grid, bounds=None):
    if bounds is None:
        bounds = (0, len(grid))
    syms = {'.': 0, '|': 0.5, '~': 0.4, '#': 1}
    mat = np.zeros((bounds[1] - bounds[0] + 1, len(grid[0])), dtype=float)
    for i, row in enumerate(grid[bounds[0]:bounds[1]]):
        for j, col in enumerate(row):
            mat[i][j] = syms.get(grid[i + bounds[0]][j], 0.25)
    plt.subplot('111')
    plt.imshow(mat, cmap='Greys')
    plt.title('day 17: water')
    plt.show()


def part1(lines):
    counts, min_y, grid = run_sim(lines)
    return sum(counts.values()) - min_y


def part2(lines):
    counts, min_y, grid = run_sim(lines)
    # why fix your code when you can print the grid to string and regex fix it
    s = ''.join([''.join(map(str, x)) for x in grid])
    sr = re.sub('~\\|~', '~~~', s)
    return sr.count('~')


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
