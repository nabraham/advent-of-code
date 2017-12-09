#(0) 3  0  1  -3  - before we have taken any steps.
#(1) 3  0  1  -3  - jump with offset 0 (that is, don't jump at all). Fortunately, the instruction is then incremented to 1.
# 2 (3) 0  1  -3  - step forward because of the instruction we just modified. The first instruction is incremented again, now to 2.
# 2  4  0  1 (-3) - jump all the way to the end; leave a 4 behind.
# 2 (4) 0  1  -2  - go back to where we just were; increment -3 to -2.
# 2  5  0  1  -2  - jump 4 steps forward, escaping the maze

def inc1(x):
    return x + 1

def inc2(x):
    return [x + 1, x - 1][x > 2]

def main(tape, inc):
    index = 0
    step = 0
    while index >= 0 and index < len(tape):
        next_index = index + tape[index]
        tape[index] = inc(tape[index])
        index = next_index
        step += 1

    return tape, step

if __name__ == '__main__':

    print(main([0, 3, 0, 1, -3], inc1))
    print(main([0, 3, 0, 1, -3], inc2))
    with open('data/05.txt') as f:
        tape = [int(l.strip('\n')) for l in f.readlines()]
        print(main(list(tape), inc1))
        print(main(list(tape), inc2))
