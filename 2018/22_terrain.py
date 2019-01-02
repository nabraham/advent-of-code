from collections import namedtuple
import networkx as nx
import aoc_utils
from pprint import pprint

Cell = namedtuple('Cell', ['geo', 'erosion', 'terrain'])
Point = namedtuple('Point', ['x', 'y'])
ROCK, WET, NARROW = 0, 1, 2
TORCH, CLIMB, NEITHER = 0, 1, 2
TERRAIN = {ROCK: '.', WET: '=', NARROW: '|'}
EQUIP = {ROCK: (TORCH, CLIMB), WET: (CLIMB, NEITHER), NARROW: (TORCH, NEITHER)}

# thank you, u/korylprince for the refactor; my bug was not passing in both target and bounds
# part 2 grid was messed up outside (>x & >y) the target


def terrain(erosion):
    return erosion % 3


def as_char(cell):
    return TERRAIN[terrain(cell.erosion)]


class Grid:
    def __init__(self, depth, modulo, target, bounds=None):
        self.cells = {}
        self.target = target
        self.bounds = [bounds, target][bounds is None]
        self.depth = depth
        self.modulo = modulo

    def erosion(self, geo):
        return (geo + self.depth) % self.modulo

    def set(self, x, y):
        if (x, y) in [(0, 0), (self.target[0], self.target[1])]:
            g = 0
        elif x == 0:
            g = y * 48271
        elif y == 0:
            g = x * 16807
        else:
            ex = self.cells[(x - 1, y)].erosion
            ey = self.cells[(x, y - 1)].erosion
            g = ex * ey
        e = self.erosion(g)
        t = terrain(e)
        self.cells[(x, y)] = Cell(g, e, t)

    def calc(self):
        for y in range(self.bounds.y + 1):
            for x in range(self.bounds.x + 1):
                self.set(x, y)

    def val(self):
        return sum([self.cells[(x, y)].terrain for x in range(self.bounds.x + 1) for y in range(self.bounds.y + 1)])

    def __repr__(self):
        rows = []
        for y in range(self.bounds.y + 1):
            row = ''
            for x in range(self.bounds.x + 1):
                row += as_char(self.cells[(x, y)])
            rows.append(row)
        return '\n'.join(rows)

    def path_to(self, target):
        graph = nx.Graph()
        for y in range(0, self.bounds.y + 1):
            for x in range(0, self.bounds.x + 1):
                items = EQUIP[self.cells[(x, y)].terrain]
                graph.add_edge((x, y, items[0]), (x, y, items[1]), weight=7)
                for dx, dy in ((0, 1), (1,0)):
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x <= self.bounds.x and 0 <= new_y <= self.bounds.y:
                        new_items = EQUIP[self.cells[(new_x, new_y)].terrain]
                        for item in set(items).intersection(set(new_items)):
                            graph.add_edge((x, y, item), (new_x, new_y, item), weight=1)
        return nx.dijkstra_path_length(graph, (0, 0, TORCH), (target[0], target[1], TORCH))


def parse(lines):
    depth = int(lines[0].split(': ')[1].strip())
    target = [int(x) for x in lines[1].split(': ')[1].split(',')]
    return depth, Point(target[0], target[1])


def part1(lines, modulo=20183):
    depth, target = parse(lines)
    g = Grid(depth, modulo, target)
    g.calc()
    return g.val()


def part2(lines, pad=500, modulo=20183):
    depth, target = parse(lines)
    bounds = Point(target.x + pad, target.y + pad)
    g = Grid(depth, modulo, target, bounds)
    g.calc()
    return g.path_to(target)


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines, 100))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
