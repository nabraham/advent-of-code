import aoc_utils
import re
from pprint import pprint

COMPASS = '<^>v'
TURNS = [-1, 0, 1]
VECTORS = { '>' : ( 1,  0),
            '<' : (-1,  0),
            '^' : ( 0, -1),
            'v' : ( 0,  1) }
SLASH = { '>' : '^',
          '^' : '>',
          'v' : '<',
          '<' : 'v' }
BACK_SLASH = { '>' : 'v',
               'v' : '>',
               '^' : '<',
               '<' : '^' }
TURN_MAP = { '/' : SLASH, '\\' : BACK_SLASH }


def print_grid(g):
    print('\n'.join(g))


def print_state(count, grid, vehicles, debug):
    if not debug:
        return
    new_grid = list(map(lambda x: list(x), grid))
    for v in vehicles:
        new_grid[v.y][v.x] = v.direction
    print('\n', count)
    print_grid(list(map(lambda x: ''.join(x), new_grid)))


class Vehicle:
    def __init__(self, id, x, y, direction):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_index = 0

    def move(self, grid):
        self.x += VECTORS[self.direction][0]
        self.y += VECTORS[self.direction][1]
        cell = grid[self.y][self.x]
        if cell in TURN_MAP:
            self.direction = TURN_MAP[cell][self.direction]
        elif cell == '+':
            ci = COMPASS.index(self.direction)
            ci = (ci + TURNS[self.turn_index] + 4) % 4
            self.direction = COMPASS[ci]
            self.turn_index = (self.turn_index + 1) % 3

    def __repr__(self):
        return '%d: (%d,%d) - %s' % (self.id, self.x, self.y, self.direction)

    def coords(self):
        return '%d,%d' % (self.x, self.y)


def parse_grid(lines):
    g = []
    vs = []
    id = 0
    for j, line in enumerate(lines):
        for direction in COMPASS:
            i = line.find(direction)
            if i >= 0:
                vs.append(Vehicle(id, i, j, direction))
                id += 1
        line = re.sub('[\<\>]', '-', line)
        line = re.sub('[\^v]', '|', line)
        g.append(line)
    return g, vs


def move_vehicles(grid, vehicles):
    collisions = []
    v_sort = sorted(vehicles, key=lambda v: v.y * 10000 + v.x)
    for v in v_sort:
        alive = {}
        for other in vehicles:
            if other.id is not v.id and other.id not in collisions:
                alive[other.coords()] = other.id

        v.move(grid)

        if v.coords() in alive:
            collisions.append( (v.id, v.coords()) )
            collisions.append( (alive[v.coords()], v.coords()) )

    return collisions


def part1(lines):
    g, vehicles = parse_grid(lines)
    collisions = set()
    while len(collisions) == 0:
        collisions = move_vehicles(g, vehicles)
    return collisions[0]


def part2(lines, debug=False):
    g, vehicles = parse_grid(lines)
    collisions = set()
    while len(vehicles) > 1:
        collisions = move_vehicles(g, vehicles)
        c_set = set(map(lambda x: x[0], collisions))
        vehicles = list(filter(lambda x: x.id not in c_set, vehicles))
    return vehicles[0].coords()


def run(filename, debug=False):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename, False)
    pprint(part1(lines))
    pprint(part2(lines, debug))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test(), True)
    run(aoc_utils.puzzle_main())
