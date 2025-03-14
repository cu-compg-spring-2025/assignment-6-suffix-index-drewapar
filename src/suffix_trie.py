import argparse
import utils

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Trie')

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

def build_suffix_trie(s):
    root = {'children': {}}

    for i in range(len(s)):
        curr = root
        suffix = s[i:]

        for char in suffix:
            if char not in curr['children']:
                curr['children'][char] = {'children': {}}
            curr = curr['children'][char]

    return root

def search_trie(trie, pattern):
    curr = trie
    overlap = 0

    for char in pattern:
        if char in curr['children']:
            overlap += 1
            curr = curr['children'][char]
        else:
            break
    
    return overlap

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    trie = build_suffix_trie(T)

    if args.query:
        for query in args.query:
            match_len = search_trie(trie, query)
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()
