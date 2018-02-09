import string
import logging
import numpy

logger = logging.getLogger('tubes')

def print_maze(m, n=40):
    for row in m[:n]:
        logger.warn(''.join(row[:n]))


def off_maze(p,m):
    return p[0] < 0 or p[0] >= len(m) or p[1] < 0 or p[1] >= len(m[p[0]]) 


def turn(pos, direction, maze):
    if direction[0] == 0:
        if pos[0] > 0 and maze[pos[0] - 1][pos[1]] != ' ':
            logger.warn('Turning North')
            return (-1,0)
        else:
            logger.warn('Turning South')
            return (1,0)
    else:
        if pos[1] > 0 and maze[pos[0]][pos[1] - 1] != ' ':
            logger.warn('Turning West')
            return (0,-1)
        else:
            logger.warn('Turning East')
            return (0,1)


def main(maze):
    print_maze(maze, 320)
    pos = (0, maze[0].index('|'))
    direction = (1,0)
    accum = []
    steps = 0
    logger.warn('Position: %s, Direction: %s' % (pos, direction))
    while True:
        steps += 1
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        if off_maze(pos, maze):
            logger.warn('off the maze')
            break
        else:
            logger.warn('Position: %s, Direction: %s' % (pos, direction))
            curr = maze[pos[0]][pos[1]]
            if curr in '-|':
                pass
            elif curr == '+':
                direction = turn(pos, direction, maze)
            elif curr in string.ascii_uppercase:
                logger.warn('accumulating "%s"'% curr)
                accum += curr
            else:
                logger.warn('off the path')
                break
    return ''.join(accum), steps


def optimize(maze):
    logger.error('Pre optimization: %d x %d' % (len(maze), len(maze[0])))
    #filter identical rows -- probably should check for only [ |], but this is good enough
    maze = [row for i, row in enumerate(maze[1:]) if i == 0 or row != maze[i-1]]
    #filter identical cols -- probably should check for only [ -], but this is good enough
    matrix = numpy.array(maze).transpose()
    matrix = numpy.array([row for i, row in enumerate(matrix[1:]) if i == 0 or list(row) != list(matrix[i-1])])
    matrix = matrix.transpose()
    logger.error('Post optimization: %d x %d' % matrix.shape)
    maze = [list(row) for row in matrix]
    return maze


def run(filename, should_optimize=False):
    with open(filename) as f:
        maze = [list(line.strip('\n')) for line in f.readlines()]
        if should_optimize:
            maze = optimize(maze)
        return main(maze)


if __name__ == '__main__':
    logger.error(run('data/19_test.txt'))
    logger.setLevel(logging.ERROR)
    logger.error(run('data/19.txt', True))
    logger.error(run('data/19.txt', False))
