knots = __import__('10_knots')
import networkx as nx

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


def neighbors(grid, i, j):
    neighbors = []
    if i > 0 and grid[i-1][j] == '1':
        neighbors.append((i-1,j))
    if j > 0 and grid[i][j-1] == '1':
        neighbors.append((i,j-1))
    return neighbors


def count_blobs(grid):
    G = nx.Graph()
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '1':
                G.add_node((i,j))
                for n in neighbors(grid, i, j):
                    G.add_edge((i,j),n)
    return len(list(nx.connected_components(G)))

    
def main(prefix,N=128):
    grid = gen_grid(prefix, N)
    print_top_left(grid)

    #part 1
    row_sums = map(row_sum, grid)

    #part 2
    count = count_blobs(grid)

    return sum(row_sums), count


if __name__ == '__main__':
    import sys
    #example
    hash_prefix = 'flqrgnkx'
    #hash_prefix = 'uugsqrei'
    if len(sys.argv) > 1:
        hash_prefix = sys.argv[1]
    print(main(hash_prefix))
