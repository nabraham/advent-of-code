def solve(s,n=1):
    z = zip(s,s[n:] + s[:n]) 
    m = map(lambda x: [0, int(x[0])][x[0] == x[1]], z)
    return sum(list(m))


if __name__ == '__main__':
    with open('data/01.txt') as f:
        line = f.readlines()[0]
        print(solve(line))
        print(solve(line, int(len(line) / 2)))
