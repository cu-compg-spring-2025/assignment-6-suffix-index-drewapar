import argparse
import utils

SUB = 0
CHILDREN = 1

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Tree')

    parser.add_argument('--reference',
                        help='Reference sequence file',
                        type=str)

    parser.add_argument('--string',
                        help='Reference sequence',
                        type=str)

    parser.add_argument('--query',
                        help='Query sequences',
                        nargs='+',
                        type=str)

    return parser.parse_args()


def add_suffix(nodes, suf):
    n = 0
    i = 0
    while i < len(suf):
        b = suf[i] 
        children = nodes[n][CHILDREN]
        if b not in children:
            n2 = len(nodes)
            nodes.append([suf[i:], {}])
            nodes[n][CHILDREN][b] = n2
            return
        else:
            n2 = children[b]

        sub2 = nodes[n2][SUB]
        j = 0
        while j < len(sub2) and i + j < len(suf) and suf[i + j] == sub2[j]:
            j += 1

        if j < len(sub2):
            n3 = n2 
            n2 = len(nodes)
            nodes.append([sub2[:j], {sub2[j]: n3}])
            nodes[n3][SUB] = sub2[j:]
            nodes[n][CHILDREN][b] = n2

        i += j
        n = n2

def build_suffix_tree(text):
    text += "$"

    nodes = [ ['', {}] ]

    for i in range(len(text)):
        add_suffix(nodes, text[i:])
    
    return nodes

def search_tree(suffix_tree, P):
    nodes = suffix_tree
    n = 0
    overlap = 0
    i = 0
    
    while i < len(P):
        x = P[i]

        # checks if char is child of split node (suffix exists)
        if x not in nodes[n][1]:
            # mismatch found
            break

        n = nodes[n][1][x]  # n is now index of new node with label x and all possible suffixes from that prefix as children
        prefix = nodes[n][0]   # prefix of node
        
        j = 0

        while j < len(prefix) and i < len(P) and P[i] == prefix[j]:
            # checks overlap with prefix and breaks when mismatch or when end of prefix
            i += 1
            j += 1
            overlap += 1
        
    return overlap

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    tree = build_suffix_tree(T)
        
    if args.query:
        for query in args.query:
            match_len = search_tree(tree, query)
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()
