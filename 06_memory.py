def redistribute(banks):
    mx = max(banks)
    i = banks.index(mx)
    count = banks[i]
    banks[i] = 0
    while count > 0:
        i = (i + 1) % len(banks)
        count -= 1
        banks[i] += 1
    return banks

def loop_size(stack, banks):
    start = stack.index(str(banks))
    return len(stack) - start
        

def main(banks):
    seen = set()
    stack = []
    step = 0
    print(banks)
    while str(banks) not in seen:
        seen.add(str(banks))
        stack.append(str(banks))
        step += 1
        banks = redistribute(banks)
        print(banks)
    return step, loop_size(stack, banks)

if __name__=='__main__':
    import sys
    banks = list(map(lambda x: int(x), sys.argv[1:]))
    print(main(banks))
