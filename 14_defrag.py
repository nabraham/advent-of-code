knots = __import__('10_knots')

def pad(c,n):
    if len(c) < n:
        return '0'*(n-len(c)) + c
    else:
        return c


def hex2bin():
    h2b = {}
    for i in range(16):
        h2b[hex(i)[-1]] = pad(bin(i)[2:],4)
    return h2b


def gen_grid(prefix, N):
    h2b = hex2bin()
    grid = []
    for i in range(N):
        hash_key = '%s-%d' % (prefix, i)
        lengths = [ord(c) for c in hash_key] + [17, 31, 73, 47, 23] 
        knot_list = knots.main(list(range(256)), lengths, 64)
        knot_hash = knots.to_hex(knot_list)
        knot_bin = ''.join([h2b[h] for h in knot_hash])
        grid.append(knot_bin)
    return grid


def row_sum(r):
    return len(list(filter(lambda x: x == '1', r)))


def print_top_left(grid, N=8, pad=4):
    sub_rows = grid[0:N]
    sub_cols = list(map(lambda r: r[0:N], sub_rows))
    import pprint
    pprint.pprint(sub_cols)


def label(grid, i, j):
    if j > 0 and grid[i][j-1] != '0':
        return grid[i][j-1]
    elif i > 0 and grid[i-1][j] != '0':
        return grid[i-1][j]
    else:
        return None

def neighbors(grid, i, j):
    neighbors = []
    if i > 0 and grid[i-1][j] == '1':
        neighbors.append((i-1,j))
    if j > 0 and grid[i][j-1] == '1':
        neighbors.append((i,j-1))
    if i < (len(grid) - 1) and grid[i+1][j] == '1':
        neighbors.append((i+1,j))
    if j < (len(grid[0]) - 1) and grid[i][j+1] == '1':
        neighbors.append((i,j+1))
    return neighbors


def walk_grid(grid, i, j, v):
    queue = set()
    queue.add((i,j))
    while len(queue) > 0:
        next_queue = set()
        for cell in queue:
            grid[cell[0]][cell[1]] = v
            for n in neighbors(grid, cell[0], cell[1]):
                next_queue.add(n)
        queue = next_queue


def count_blobs(str_grid):
    grid = [list(row) for row in str_grid]
    next_region = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '1':
                next_region += 1
                walk_grid(grid, i, j, next_region)
            elif cell == '0':
                grid[i][j] = 0
    return grid, next_region

    

def main(prefix,N=128):
    grid = gen_grid(prefix, N)
    print_top_left(grid)

    #part 1
    row_sums = map(row_sum, grid)

    #part 2
    blobbed, count = count_blobs(grid)
    print_top_left(blobbed)

    return sum(row_sums), count


if __name__ == '__main__':
    import sys
    #example
    #hash_prefix = 'flqrgnkx'
    hash_prefix = 'uugsqrei'
    if len(sys.argv) > 1:
        hash_prefix = sys.argv[1]
    print(main(hash_prefix))
