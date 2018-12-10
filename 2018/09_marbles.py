import aoc_utils
import re
from collections import deque, defaultdict
from pprint import pprint

game_pattern = re.compile(r'(\d+) players; last marble is worth (\d+) points')

def print_state(player, circle):
    c_index = circle.index(0)
    circle.rotate(-c_index)
    print('[%d]:' % player, circle)
    circle.rotate(c_index)

def part1(lines, multiplier=1):
    game_match = game_pattern.match(lines[0])
    n_players = int(game_match.group(1))
    end_points = int(game_match.group(2))*multiplier
    players = defaultdict(int)
    circle = deque([0])

    #refactored to deque; thanks, reddit u/marcusandrews -- genius!
    for marble in range(1, end_points + 1):
        if marble % 23:
            circle.rotate(-1)
            circle.append(marble)
        else:
            circle.rotate(7)
            players[marble % n_players] += marble + circle.pop()
            circle.rotate(-1)
        #print_state(marble, circle)

    return max(players.values())


def part2(lines):
    return part1(lines, 100) 


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
