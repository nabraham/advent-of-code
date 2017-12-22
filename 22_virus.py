import math
from pprint import pprint

N, E, S, W = [0, 1, 2, 3]
DIR_HR = 'NESW'
DIRECTIONS = [(-1,0), (0,1), (1,0), (0,-1)]
RIGHT = 1
LEFT = 3

def move(grid, p, v):
    infected = 1 - grid[p[0]][p[1]]
    grid[p[0]][p[1]] = infected
    p = [p[0] + v[0], p[1] + v[1]]

    if p[0] == -1:
        print('NEW NORTH')
    elif p[0] == len(grid):
        print('NEW SOUTH')
    elif p[1] == -1:
        print('NEW WEST')
    elif p[1] == len(grid):
        print('NEW EAST')
        
    return grid, p, infected


def main(grid, iters):
    start = math.floor(len(grid)/2)
    pos = (start, start)
    pointing = N
    infected_count = 0
    for step in range(iters):
        if grid[pos[0]][pos[1]] == '#':
            pointing = (pointing + RIGHT) % 4
        else:
            pointing = (pointing + LEFT) % 4
        grid, pos, infected = move(grid, pos, DIRECTIONS[pointing]) 
        infected_count += infected
        print()
        pprint(grid)
        print(pos,'-',DIR_HR[pointing])
        
    

def run(filename, iters=10000):
    with open(filename) as f:
        grid = [list(map(int, list(line.strip('\n').replace('.','0').replace('#','1')))) for line in f.readlines()]
        pprint(grid)
        main(grid, iters)


if __name__ == '__main__':
    run('data/22_test.txt',15)
