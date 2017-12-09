def row_parse(line):
    return list(map(lambda x: int(x), line.split('\t')))


def check_sum(row):
    return max(row) - min(row)


def check_sum_factor(row):
    for i1, v1 in enumerate(row):
        for v2 in row[(i1 + 1):]:
            if v1 % v2 == 0:
                return v1 / v2
            elif v2 % v1 == 0:
                return v2 / v1
    raise Exception('No factors found')


def solve(lines):
    mat = list(map(row_parse, lines))
    cs = map(check_sum, mat)
    cs2 = map(check_sum_factor, mat)
    return sum(cs), int(sum(cs2))


if __name__ == '__main__':
    with open('data/02.txt') as f:
        print(solve([line.strip('\n') for line in f.readlines()]))
