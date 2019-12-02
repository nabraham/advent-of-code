import os.path
import __main__


def file_base(_file_):
    if _file_ == None:
        _file_ = __main__.__file__
    base = os.path.splitext(os.path.basename(_file_))[0].split('_')[0]
    return os.path.join('data',base)


def puzzle_main(_file_=None):
    return file_base(_file_) + '.txt'


def puzzle_test(_file_=None):
    return file_base(_file_) + '_test.txt'


def file_header(filename):
    return '\n%s\n%s' % (filename, '-'*len(filename))


def get_input(filename=None, strip=True):
    if filename == None:
        filename = puzzle_main()
    with open(filename) as f:
        if strip:
            input = f.read().strip()
        else:
            input = f.read().strip('\n')
    return input.split('\n')
