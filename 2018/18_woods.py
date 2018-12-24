import aoc_utils
from pprint import pprint

NEIGHBORS = list(filter(lambda x: x != (0, 0), [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]]))
OPEN, TREES, LUMBER = '.', '|', '#'


def transition(type, neighbors):
    if type == OPEN:
        return [OPEN, TREES][neighbors.count(TREES) >= 3]
    elif type == TREES:
        return [TREES, LUMBER][neighbors.count(LUMBER) >= 3]
    else:
        return [OPEN, LUMBER][neighbors.count(LUMBER) >= 1 and neighbors.count(TREES) >= 1]


class Grid:
    def __init__(self, lines):
        self.height = len(lines)
        self.width = len(lines[0])
        self.cells = [list(line) for line in lines]

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self.cells])

    def adjacent(self, i, j):
        deltas = list(map(lambda x: (x[0] + i, x[1] + j), NEIGHBORS))
        in_bounds = list(filter(lambda x: (0 <= x[0] < self.height) and (0 <= x[1] < self.width), deltas))
        return ''.join(map(lambda x: self.cells[x[0]][x[1]], in_bounds))

    def update(self):
        out = [list(''.join(row)) for row in self.cells]
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                neighbors = self.adjacent(i, j)
                out[i][j] = transition(col, neighbors)
        self.cells = out

    def value(self):
        return str(self).count(TREES) * str(self).count(LUMBER)


def part1(lines, n=10):
    g = Grid(lines)
    for turn in range(n):
        g.update()
    return g.value()


def part2(lines):
    g = Grid(lines)
    found_cycle = False
    turn = 0
    seen = {str(g): turn}
    lookup = {turn: str(g)}
    while not found_cycle:
        turn += 1
        g.update()
        if str(g) in seen:
            found_cycle = True
        else:
            seen[str(g)] = turn
            lookup[turn] = str(g)
    start = seen[str(g)]
    target = start + ((1000000000 - start) % (turn - start))
    billion = Grid(lookup[target].split('\n'))
    return billion.value()
    # 1 2 3 4 5 6 7 8 9 0 1 2 3 4
    # x x x A B C D A B C D A B C


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
