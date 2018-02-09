import numpy as np
from pprint import pprint


def mat_hash(mat):
    return ''.join(list(map(str,list(mat.flatten()))))


def divide_matrix(m,d):
    dims = m.shape
    steps = int(dims[0] / d)
    rows = []
    for i in range(steps):
        row = []
        for j in range(steps):
            row.append(m[i*d:(i+1)*d, j*d:(j+1)*d])
        rows.append(row)
    return rows


def iterate(matrix, rules, i):
    dims = matrix.shape
    divisor = -1
    if dims[0] != dims[1]:
        raise Exception('Matrix must be square')
    divisor = [3, 2][dims[0] % 2 == 0]
    sub_list = divide_matrix(matrix, divisor)
    new_list = [[rules[mat_hash(m)] for m in row] for row in sub_list]

    flat_cols = []
    for row in new_list:
        c0 = row[0]
        for m in row[1:]:
            c0 = np.concatenate((c0,m), axis=1)
        flat_cols.append(c0)
    r0 = flat_cols[0]
    for row in flat_cols[1:]:
        r0 = np.concatenate((r0,row), axis=0)
    print('%d - divisor: %d, sum - %d' % (i, divisor, r0.sum()))
    return r0


def create_matrix(s):
    chars = s.replace('.','0').replace('#','1').split('/')
    nums = [list(map(int,r)) for r in chars]
    return np.array(nums)


def generate_all(m):
    r_90 = np.rot90(m)
    r_180 = np.rot90(r_90)
    r_270 = np.rot90(r_180)
    f_ud = np.flipud(m)
    f_lr = np.fliplr(m)
    f_90 = np.rot90(f_ud)
    f_270 = np.rot90(f_lr)
    return [m, r_90, r_180, r_270, f_ud, f_lr, f_90, f_270]

def run(filename, N=5):
    m0 = create_matrix('.#./..#/###')
    
    with open(filename) as f:
        rules = {}
        for line in f.readlines():
            parts = line.strip('\n').split(' ')
            key = create_matrix(parts[0])
            value = create_matrix(parts[2])
            for k in generate_all(key):
                rules[mat_hash(k)] = value

    for i in range(N):
        m0 = iterate(m0, rules, i)
    print(m0)

if __name__ == '__main__':
    run('data/21.txt')
    run('data/21.txt', 18)
