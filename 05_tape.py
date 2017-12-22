import aoc_utils

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
    tape = [int(line) for line in aoc_utils.get_input()]
    print(main(list(tape), inc1))
    print(main(list(tape), inc2))
