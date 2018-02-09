import math
import aoc_utils
from collections import deque

N, E, S, W = [0, 1, 2, 3]
DIR_HR = 'NESW'
DIRECTIONS = [(-1,0), (0,1), (1,0), (0,-1)]
RIGHT = 1
REVERSE = 2
LEFT = 3
CLEAN, WEAK, INFECTED, FLAGGED = 0,1,2,3

def print_grid(grid):
    print('\n'.join([str(list(row)) for row in grid]))

def move(grid, p, v, transition):
    grid[p[0]][p[1]] = transition(grid[p[0]][p[1]])
    n_infected = [0, 1][grid[p[0]][p[1]] == INFECTED]
    p = [p[0] + v[0], p[1] + v[1]]
    if p[0] == -1:
        zeros = deque([0] * len(grid[0]))
        grid.appendleft(zeros)
        p[0] = 0
    elif p[0] == len(grid):
        zeros = deque([0] * len(grid[0]))
        grid.append(zeros)
    elif p[1] == -1:
        for row in grid:
            row.appendleft(0)
        p[1] = 0
    elif p[1] == len(grid[0]):
        for row in grid:
            row.append(0)
        
    return grid, p, n_infected


def main(grid, transition, turn_logic, iters):
    start = math.floor(len(grid)/2)
    pos = (start, start)
    pointing = N
    infected_count = 0
    for step in range(iters):
        #print(pos,'-',DIR_HR[pointing])
        #print_grid(grid)
        #print('Heading ', DIR_HR[pointing], '\n')
        pointing = turn_logic(grid[pos[0]][pos[1]], pointing)
        grid, pos, infected = move(grid, pos, DIRECTIONS[pointing], transition) 
        infected_count += infected
    return infected_count
        

def run(filename, transition, turn_logic, iters=10000):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    grid = deque([deque(map(int, list(line.strip('\n')
        .replace('.',str(CLEAN))
        .replace('#',str(INFECTED))))) for line in input])
    print(main(grid, transition, turn_logic, iters))


def transition_p1(state):
    return [CLEAN, INFECTED][state == CLEAN]


def transition_p2(state):
    return (state + 1) % 4


def turn_p1(state, pointing):
    if state == INFECTED:
        pointing = (pointing + RIGHT) % 4
    else:
        pointing = (pointing + LEFT) % 4
    return pointing


def turn_p2(state, pointing):
    if state == CLEAN:
        pointing = (pointing + LEFT) % 4
    if state == INFECTED:
        pointing = (pointing + RIGHT) % 4
    elif state == FLAGGED:
        pointing = (pointing + REVERSE) % 4
    return pointing

    

if __name__ == '__main__':
    run(aoc_utils.puzzle_test(__file__), transition_p1, turn_p1, 70)
    run(aoc_utils.puzzle_main(__file__), transition_p1, turn_p1)
    run(aoc_utils.puzzle_test(__file__), transition_p2, turn_p2, 100)
    run(aoc_utils.puzzle_main(__file__), transition_p2, turn_p2, 10000000)
