def main(step_size, n_steps):
    buff = [0]
    i = 0

    for s in range(n_steps):
        i = (i + step_size) % len(buff) + 1
        buff = buff[:i] + [s+1] + buff[i:]
        print(i-1, buff)
    return buff


def solve(step_size, n_steps):
    buff = main(step_size, n_steps)
    i_find = buff.index(n_steps)
    return buff[(i_find + 1) % len(buff)]


if __name__ == '__main__':
    step_size = 370
    N = 2017

    #PART 1
    print('PART 1:', solve(step_size, N))

    #PART 2
    buff_one = None
    index = 0
    N = 50*10**6
    for iter in range(N):
        index = (index + step_size) % (iter + 1) + 1
        if index == 1:
            buff_one = iter + 1
    print('PART 2:', buff_one)
