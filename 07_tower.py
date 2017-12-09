import re
from collections import Counter

patt = re.compile('([a-z]+)\s+\(([0-9]+)\)(\s+-> (.*))?')

class Node:
    name = ''
    weight = 0
    children = None
    cweights = None
    cnames = None
    parent = None

    def __init__(self, name, weight, children=[]):
        self.name = name
        self.weight = weight
        self.children = children
        self.cweights = []
        self.cnames = []

    def create(line):
        matches = patt.match(line)
        name = matches.group(1)
        weight = int(matches.group(2))
        children = matches.group(4)
        if children != None:
            children = re.split(', ', children)
            return Node(name, weight, children)
        else:
            return Node(name, weight)

    def __repr__(self):
        return '%s <%s> (%d) - %s // %s // %s' % (self.name, self.parent, self.weight, self.children, self.cweights, self.cnames)

def find_root(tree, node):
    while tree[node].parent != None:
        node = tree[node].parent
    return node

def find_wrong(tree):
    step = 0
    while True:
        step += 1
        nodes = [tree[k] for k in tree]
        bottom = list(filter(lambda x: len(x.children) == 0, nodes))
        for b in bottom:
            if len(set(b.cweights)) > 1:
                print(b)
                count = Counter(b.cweights)
                different = 0
                same = 0
                for c in count:
                    if count[c] == 1:
                        different = c
                    else:
                        same = c
                delta = same-different
                i = b.cweights.index(different)
                return (b.cnames[i], delta)
            else:
                tree[b.parent].cweights += [(b.weight + sum(b.cweights))]
                tree[b.parent].cnames += [b.name]
                tree[b.parent].children.remove(b.name)
            tree.pop(b.name)


def main(nodes):
    tree = dict()
    for n in nodes:
        tree[n.name] = n
    for n in nodes:
        for c in n.children:
            tree[c].parent = n.name

    root = find_root(tree, nodes[0].name)
    wrong = find_wrong(dict(tree))
    print(tree[wrong[0]])
    return root, (tree[wrong[0]].weight + wrong[1])

if __name__ == '__main__':
    with open('data/07.txt') as f:
        nodes = [Node.create(l.strip('\n')) for l in f.readlines()]
        print(main(nodes))
