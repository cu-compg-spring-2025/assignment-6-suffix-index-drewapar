import argparse
import utils
import suffix_tree

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

def get_suffixes(s):
    suffixes = []
    for i in range(len(s)):
        suffixes.append(s[i:])
    return suffixes

def build_suffix_array(T):
    suffixes = get_suffixes(T)
    suffixes.sort()

    SA = []

    for suffix in suffixes:
        SA.append(len(T) - len(suffix))

    return SA

def get_overlap(T, q):
    overlap = 0

    while overlap < len(T) and overlap < len(q) and T[overlap] == q[overlap]:
        overlap += 1

    return overlap

def left_BS(T, suffix_array, q, i):
    lo = 0
    hi = len(suffix_array)
    while (hi - lo >= 1):  
        mid = int((lo + hi) / 2)
        if (suffix_array[mid]+i >= len(T)) or T[suffix_array[mid]+i] < q[i]:
            lo = mid + 1
        else:
            hi = mid 

    return lo 

def right_BS(T, suffix_array, q, i):
    lo = 0
    hi = len(suffix_array)
    while (hi - lo >= 1):
        
        mid = int((lo + hi) / 2)
        if T[suffix_array[mid]+i] <= q[i]:
            lo = mid + 1
        else:
            hi = mid

    return lo 

def search_array(T, suffix_array, q):
    i = 0
    left = 0
    right = len(suffix_array)

    while i < len(q) and (right - left > 1):
        _left = left + left_BS(T, suffix_array[left:right], q, i) 
        _right = left + right_BS(T, suffix_array[left:right], q, i) 
        
        if _left == _right:
            break
        
        i += 1
        left = _left
        right = _right
    
    return get_overlap(T[suffix_array[left]:], q)

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]

    array = build_suffix_array(T)

    if args.query:
        for query in args.query:
            match_len = search_array(T, array, query)
            print(f'{query} : {match_len}')

if __name__ == '__main__':
    main()
