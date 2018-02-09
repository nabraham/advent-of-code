import aoc_utils
import string


def exchange(programs, indices):
    tmp = programs[indices[0]]
    programs[indices[0]] = programs[indices[1]]
    programs[indices[1]] = tmp
    return programs


def process_instruction(i, programs):
    if i[0] == 's':
        tail = int(i[1:])
        return programs[-tail:] + programs[:-tail]
    elif i[0] == 'x':
        indices = [int(x) for x in i[1:].split('/')]
        return exchange(programs, indices)
    elif i[0] == 'p':
        names = i[1:].split('/')
        indices = [programs.index(n) for n in names]
        return exchange(programs, indices)
    else:
        raise Exception('Unexpected dance move')


def main(dance, programs):
    for instruction in dance:
        programs = process_instruction(instruction, programs)
    return programs


if __name__ == '__main__':
    #print(main(['s1','x3/4','pe/b'], list('abcde')))
    #print(main(['s1','x3/4','pe/b'], list('baedc')))

    programs = list(string.ascii_lowercase[:16])
    dance = aoc_utils.get_input()[0].split(',')
    #PART 1
    print('Part 1:', ''.join(main(dance, list(programs))))

    #PART 2
    seen = set([''.join(programs)])
    stack = [''.join(programs)]
    repeat = -1
    while repeat < 0:
        programs = main(dance, programs)
        key = ''.join(programs)
        if key in seen:
            repeat = stack.index(key)
        else:
            seen.add(key)
            stack.append(key)
    print('Cycled after %d, Repeats to %d' %  (len(stack), repeat))
