import aoc_utils
from collections import defaultdict
from pprint import pprint


class Cell:
    def __init__(self, x, y, serial):
        rack_id = x + 10
        power = rack_id * y
        power += serial
        power *= rack_id
        power = int(str(power)[-3])
        self.power = power - 5
        self.x = x
        self.y = y


    def __repr__(self):
        return str(self.power)


class Grid:
    def __init__(self, serial, N=300):
        self.serial = serial
        self.cells = []
        self.size = N
        for y in range(N):
            row = []
            for x in range(N):
                row.append(Cell(x, y, serial))
            self.cells.append(row)


    def at(self, x, y):
        return self.cells[y][x].power


    def max_window(self, W=3):
        windows = defaultdict(int)
        for y in range(0, self.size-W):
            for x in range(0, self.size-W):
                for j in range(W):
                    for i in range(W):
                        windows['%d,%d' % (x,y)] += self.at(x+i, y+j)
        return max(windows.items(), key=lambda x: x[1])


def part1(lines):
    serial = int(lines[0])
    return Grid(serial).max_window()


def part2(lines):
    serial = int(lines[0])
    maxx = []
    g = Grid(serial)
    for w in range(3, 20):
        maxx.append((w, g.max_window(w)))
    return max(maxx, key=lambda x: x[1][1])


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
