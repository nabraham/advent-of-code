import aoc_utils
import re
from collections import defaultdict
from pprint import pprint
from string import ascii_letters

N = (0,  1)
S = (0, -1)
E = (1,  0)
W = (-1, 0)
MANHATTAN_NEIGHBORS = [N,S,E,W]
FRONT = '.'

class Cell:
    def __init__(self, x, y, origin, last, dist):
        self.x = x
        self.y = y
        self.origin = origin
        self.last = last
        self.dist = dist

    def neighbors(self, grid):
        neighs = []
        for n in MANHATTAN_NEIGHBORS:
            next = Cell(self.x + n[0], self.y + n[1], self.origin, self, self.dist + 1)
            if next.in_bounds(grid) and not grid.contains(next):
                neighs.append(next)
        return neighs

    def in_bounds(self, grid):
        return (self.x >= grid.min_x and
                self.x <= grid.max_x and
                self.y >= grid.min_y and
                self.y <= grid.max_y)

    def coords(self):
        return '%s,%s' % (self.x, self.y)

    def __repr__(self):
        return '<%s,%s> (%s, %s)' % (self.x, self.y, self.origin, self.dist)

    def __hash__(self):
        return hash(self.coord())

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

    def contains(self, cell):
        return cell.coords() in self.cells

    def debug(self):
        return 'Bounds: %s\nCells: %s' % ([self.min_x, self.max_x, self.min_y, self.max_y], self.cells)

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


def group_by_coords(cells):
    groups = defaultdict(list)
    for c in cells:
        groups[c.coords()].append(c)
    return groups

def has_different_fronts(cells):
    return len(set(map(lambda x: x.origin, cells))) > 1


def part1(lines):
    pattern = re.compile('(\d+), (\d+)')
    queue = []
    for i, line in enumerate(lines):
        m = pattern.match(line)
        c = Cell(int(m.group(1)), int(m.group(2)), key(i), None, 0)
        queue.append(c)
    grid = Grid(queue)

    while len(queue) > 0:
        groups = group_by_coords(queue)
        new_queue = []
        for g in groups:
            cell = groups[g][0]
            if grid.contains(cell):
                pass
            elif len(groups[g]) > 1 and has_different_fronts(groups[g]):
                front = Cell(cell.x, cell.y, FRONT, None, cell.dist)
                grid.add(front)
            else:
                grid.add(cell)
                new_queue += cell.neighbors(grid)
        queue = new_queue

    print(grid)
    return grid.biggest()


def part2(lines):
    return None


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    #pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
