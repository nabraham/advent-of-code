import aoc_utils

NESW = [(0,1),(1,0),(0,-1),(-1,0)]
TURN = {'R': 1, 'L': -1}

def dist(pos):
    return abs(pos[0]) + abs(pos[1])


def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    visited = set(['0,0'])
    moves = [m.strip(' ') for m in input[0].split(',')]
    pos = [0,0]
    orient = 0
    first = True
    for m in moves:
        orient = (orient + TURN[m[0]] + 4) % 4
        steps = int(m[1:])
        for s in range(1,steps+1):
            new_x = pos[0] + s * NESW[orient][0]
            new_y = pos[1] + s * NESW[orient][1]
            key = '%s,%s' % (new_x, new_y)
            if first and key in visited:
                print('First: %d,%d - %d' % (new_x, new_y, dist([new_x, new_y])))
                first = False
            visited.add(key)

        pos[0] += steps * NESW[orient][0]
        pos[1] += steps * NESW[orient][1]
    print(dist(pos))


if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
