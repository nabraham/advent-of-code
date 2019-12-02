import aoc_utils
import numpy as np
from pprint import pprint

class Instruction:
    def __init__(self, s):
        self.direction = s[0]
        self.length = int(s[1:])


VELOCITY = {
  'L': np.array([-1,  0]),
  'R': np.array([ 1,  0]),
  'U': np.array([ 0,  1]),
  'D': np.array([ 0, -1])
}


def hash_key(pt):
    return '%d_%d' % (pt[0], pt[1])


def hash_length(h):
    x, y = [int(x) for x in h.split('_')]
    return abs(x) + abs(y)


def part1(lines):
    visited = dict()
    intersections = set([])
    for idx, line in enumerate(lines):
        instructions = [Instruction(x) for x in line.split(',')]
        location = np.array([0, 0])
        for i in instructions:
            velocity = VELOCITY[i.direction]
            for step in range(i.length):
                location += velocity
                key = hash_key(location)
                if key in visited:
                    if idx not in visited[key]:
                        intersections.add(key)
                    visited[key].add(idx)
                else:
                    visited[key] = set([idx])

    closest = min(list(intersections), key=lambda x: hash_length(x))
    return hash_length(closest)



def part2(lines):
    visited = dict()
    intersections = []
    for idx, line in enumerate(lines):
        instructions = [Instruction(x) for x in line.split(',')]
        location = np.array([0, 0])
        total = 0
        for i in instructions:
            velocity = VELOCITY[i.direction]
            for step in range(i.length):
                total += 1
                location += velocity
                key = hash_key(location)
                if key in visited:
                    if idx not in visited[key]:
                        intersections.append(total + visited[key][0])
                        visited[key][idx] = total
                else:
                    visited[key] = {idx: total}

    return min(intersections)


def run(filename):
    print(aoc_utils.file_header(filename))
    lines = aoc_utils.get_input(filename)
    pprint(part1(lines))
    pprint(part2(lines))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
