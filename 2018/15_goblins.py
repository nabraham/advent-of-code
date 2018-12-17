import aoc_utils
from collections import defaultdict
from pprint import pprint
from functools import reduce


def plan_path_to_target(player, grid, targets):
    starts = grid.find_open_neighbors(player.position, set())
    possibles = defaultdict(set)
    q = {}
    for s in starts:
        q[s] = set([s])
        if s in targets:
            possibles[s].add(s)
    explored = set(starts)

    while len(q) > 0 and len(possibles) == 0:
        new_q = defaultdict(set)
        for head in q:
            roots = q[head]
            neighbors = grid.find_open_neighbors(head, explored)
            for n in neighbors:
                if n in targets:
                    possibles[n] = possibles[n].union(roots)
                else:
                    new_q[n] = new_q[n].union(roots)
        q = new_q
        explored = explored.union(set(list(q.keys())))

    if len(possibles) > 0:
        target = sorted(list(possibles.keys()), key=lambda x: x.priority())[0]
        return sorted(possibles[target], key=lambda x: x.priority())[0]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def priority(self):
        return 1000 * self.y + self.x

    def __repr__(self):
        return '(%d,%d)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.priority()


class Player:
    def __init__(self, pid, display, x, y, race, hp, ap):
        self.pid = pid
        self.display = display
        self.position = Point(x, y)
        self.race = race
        self.hit_points = hp
        self.attack_power = ap
        self.alive = True

    def rid(self):
        return '%s%d' % (self.race, self.pid)

    def __repr__(self):
        return '%s <%s>(%d)' % (self.rid(), self.position, self.hit_points)

    def __hash__(self):
        return hash(self.pid)

    def __eq__(self, other):
        return self.pid == other.pid

    def find_move(self, grid):
        if not grid.is_next_to_enemy(self):
            targets = grid.adjacent_to_enemies(self)
            # print('targets = ', targets)
            return plan_path_to_target(self, grid, targets)

    def find_enemy(self, grid):
        return grid.find_attack_enemy(self)

    def move(self, grid, target):
        # print('moving %s to %s' % (self, target))
        grid.move_player(self, target)

    def position_order(self):
        return self.position.priority()

    def hp_order(self):
        return 10000 * self.hit_points + self.position_order()

    def attack(self, enemy, grid):
        enemy.hit_points -= self.attack_power
        if enemy.hit_points <= 0:
            grid.remove(enemy)


NEIGHBOR_VECS = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]


class Grid:

    def __init__(self, lines, elf_attack=3):
        count = 0
        self.cells = []
        self.registry = {}
        self.height = len(lines)
        self.width = len(lines[0])
        for i, line in enumerate(lines):
            row = []
            for j, c in enumerate(line):
                v = c
                if c in 'EG':
                    attack_power = {'E': elf_attack, 'G': 3}[c]
                    p = Player(count, count % 10, j, i, c, 200, attack_power)
                    self.registry[p.pid] = p
                    v = p.pid
                    count += 1
                row.append(v)
            self.cells.append(row)

    def at_point(self, p):
        return self.at_coords(p.x, p.y)

    def at_coords(self, x, y):
        k = self.cells[y][x]
        if k in self.registry:
            return self.registry[k]
        return k

    def play_round(self):
        ordered_players = sorted(self.registry.values(), key=lambda x: x.position_order())
        for p in ordered_players:
            if p.alive:
                move = p.find_move(self)
                if move is not None:
                    p.move(self, move)
                enemy = p.find_enemy(self)
                if enemy is not None:
                    p.attack(enemy, self)

    def is_next_to_enemy(self, player):
        for v in NEIGHBOR_VECS:
            o = player.position + v
            if self.in_bounds(o) and isinstance(self.at_point(o), Player) and self.at_point(o).alive and self.at_point(o).race is not player.race:
                return True
        return False

    def adjacent_to_enemies(self, player):
        enemies = list(filter(lambda x: x.race != player.race, self.registry.values()))
        adjacent = map(lambda x: self.find_open_neighbors(x.position, set()), enemies)
        return set(reduce(lambda x, y: x + y, adjacent, []))

    def find_open_neighbors(self, position, explored):
        unexplored = []
        for v in NEIGHBOR_VECS:
            other = position + v
            if other not in explored and self.in_bounds(other) and str(self.at_point(other)) == '.':
                unexplored.append(other)
        return unexplored

    def in_bounds(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def find_attack_enemy(self, player):
        enemies = []
        for v in NEIGHBOR_VECS:
            o = player.position + v
            if self.in_bounds(o):
                cell = self.at_point(o)
                if isinstance(cell, Player) and cell.race is not player.race:
                    enemies.append(cell)
        if len(enemies) > 0:
            return sorted(enemies, key=lambda x: x.hp_order())[0]

    def move_player(self, player, location):
        self.cells[player.position.y][player.position.x] = '.'
        self.cells[location.y][location.x] = player.pid
        player.position = location

    def remove(self, player):
        player.alive = False
        self.cells[player.position.y][player.position.x] = '.'
        del self.registry[player.pid]

    def finished(self):
        return len(set(map(lambda x: x.race, self.registry.values()))) < 2

    def score(self, round):
        return round * sum(map(lambda x: x.hit_points, filter(lambda x: x.alive, self.registry.values())))

    def count(self, race):
        return len(list(filter(lambda x: x.race == race, self.registry.values())))

    def __repr__(self):
        pretty = [' ' + ''.join(map(lambda x: str(x % 10), range(self.width)))]
        for i in range(self.height):
            row = str(i % 10)
            players = []
            for j in range(self.width):
                at = self.at_coords(j, i)
                if isinstance(at, Player):
                    players.append(at)
                    row += str(at.race)
                else:
                    row += at
            row += '   %s' % ', '.join(map(lambda x: str(x), players))
            pretty.append(row)
        return '\n'.join(pretty)


def print_turn(turn, grid):
    print('\nAfter %d rounds:' % turn)
    print(grid)


def run_game(grid):
    turn = 0
    while not grid.finished():
        turn += 1
        grid.play_round()
    return grid.score(turn - 1)


def part1(lines):
    g = Grid(lines)
    return run_game(g)


def part2(lines, elf_power=10):
    all_lived = False
    elf_count = ''.join(lines).count('E')
    while not all_lived:
        elf_power += 1
        g = Grid(lines, elf_power)
        score = run_game(g)
        all_lived = g.count('E') == elf_count
    return score


def run(filename, elf_power=10):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines, elf_power))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main(), 20)
