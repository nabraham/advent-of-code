import aoc_utils

def valid_tri(t):
    ts = sorted(t)
    return sum(ts[:2]) > ts[2]


def part_2(tris):
    p2 = []
    for i in range(0,len(tris),3):
        for j in range(3):
            p2.append([tris[i][j], tris[i+1][j], tris[i+2][j]])
    return p2

def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    tris = [[int(n) for n in row.split()] for row in input]
    print(len(list(filter(valid_tri, tris))))
    print(len(list(filter(valid_tri, part_2(tris)))))

if __name__ == '__main__':
    run(aoc_utils.puzzle_main())
