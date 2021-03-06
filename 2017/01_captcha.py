import aoc_utils

def solve(s,n=1):
    z = zip(s,s[n:] + s[:n]) 
    m = map(lambda x: [0, int(x[0])][x[0] == x[1]], z)
    return sum(list(m))


if __name__ == '__main__':
    line = aoc_utils.get_input(aoc_utils.puzzle_main(__file__))[0]
    print(solve(line))
    print(solve(line, int(len(line) / 2)))
