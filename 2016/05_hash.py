import aoc_utils
from hashlib import md5

def gen_hash(seed, i):
    return md5((seed + str(i)).encode('ascii')).hexdigest()

def interesting(h):
    return h[:5] == '00000'

def first_interesting(h):
    return h[5]

def part1(seed):
    i = 0
    count = 0
    rez = ''
    while count < 8:
        h = gen_hash(seed, i)
        if interesting(h):
            rez += first_interesting(h)
            print(rez)
            count += 1
        i += 1

def part2(seed):
    rez = ['.'] * 8
    i = 0
    while '.' in rez:
        h = gen_hash(seed, i)
        if interesting(h):
            index = h[5]
            val = h[6]
            if index in '01234567' and rez[int(index)] == '.':
                rez[int(index)] = val
                print(rez)
            else:
                print('doh!')
        i += 1
    print(''.join(rez))



def run(filename):
    print('\n' + aoc_utils.file_header(filename))
    input = aoc_utils.get_input(filename)
    seed = input[0]
    part1(seed)
    part2(seed)

if __name__ == '__main__':
    run(aoc_utils.puzzle_test())
    run(aoc_utils.puzzle_main())
