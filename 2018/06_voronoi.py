import aoc_utils
import re
from collections import defaultdict
from pprint import pprint
from string import ascii_letters

FRONT = '.'

class Cell:
    def __init__(self, x, y, origin, last, dist):
        self.x = x
        self.y = y
        self.origin = origin
        self.last = last
        self.dist = dist

    def distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def coords(self):
        return '%s,%s' % (self.x, self.y)

    def __repr__(self):
        return '<%s,%s> (%s, %s)' % (self.x, self.y, self.origin, self.dist)


class Grid:
    def __init__(self, starting_cells):
        self.count = defaultdict(int)
        self.cells = {}
        self.calc_bounds(starting_cells)

    def calc_bounds(self, cells):
        self.min_x = min(cells, key=lambda x: x.x).x
        self.max_x = max(cells, key=lambda x: x.x).x
        self.min_y = min(cells, key=lambda x: x.y).y
        self.max_y = max(cells, key=lambda x: x.y).y

    def add(self, cell):
        if cell.origin != FRONT:
            self.count[cell.origin] += 1
        self.cells[cell.coords()] = cell

    def biggest(self):
        counts = self.count.items()
        edges = set([])

        for x in range(self.min_x, self.max_x + 1):
            for y in [self.min_y, self.max_y]:
                edges.add(self.cells['%s,%s' % (x, y)].origin)

        for y in range(self.min_y, self.max_y + 1):
            for x in [self.min_x, self.max_x]:
                edges.add(self.cells['%s,%s' % (x, y)].origin)

        finite = list(filter(lambda x: x[0] not in edges, counts))
        return max(finite, key=lambda x: x[1])

    def __repr__(self):
        g = []
        for i in range(self.min_y, self.max_y + 1):
            row = ''
            for j in range(self.min_x, self.max_x + 1):
                k = '%s,%s' % (j,i)
                if k in self.cells:
                    row += self.cells[k].origin
                else:
                    row += '?'
            g.append(row)
        return '\n'.join(g)


def key(i):
    return ascii_letters[i]


def find_closest(i, j, cells):
    dists = list(map(lambda x: (x.distance(i,j), x), cells))
    closest = min(dists, key=lambda x: x[0])[0]
    multiples = list(filter(lambda x: x[0] == closest, dists))
    if len(multiples) == 1:
        return Cell(i, j, multiples[0][1].origin, None, 0)
    else:
        return Cell(i, j, FRONT, None, 0)


def get_queue(lines):
    pattern = re.compile('(\d+), (\d+)')
    queue = []
    for i, line in enumerate(lines):
        m = pattern.match(line)
        c = Cell(int(m.group(1)), int(m.group(2)), key(i), None, 0)
        queue.append(c)
    return queue


def total_dist(i, j, cells):
    return sum(map(lambda x: x.distance(i, j), cells))


def part1(lines):
    queue = get_queue(lines)
    grid = Grid(queue)
    for i in range(grid.min_x, grid.max_x + 1):
        for j in range(grid.min_y, grid.max_y + 1):
            c = find_closest(i,j, queue)
            grid.add(c)
    big = grid.biggest()
    return big[1], big[0]


def part2(lines):
    queue = get_queue(lines)
    grid = Grid(queue)
    total = [32, 10000][grid.max_x > 32]
    count = 0
    for i in range(grid.min_x, grid.max_x + 1):
        for j in range(grid.min_y, grid.max_y + 1):
            if total_dist(i, j, queue) < total:
                count +=1
    return count


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
