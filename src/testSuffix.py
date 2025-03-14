import argparse
import utils
import suffix_trie
import suffix_tree
import suffix_array
import matplotlib.pyplot as plt
import tracemalloc
import time
import numpy as np
import random

def get_args():
    parser = argparse.ArgumentParser(description='Suffix Tree')

    parser.add_argument('--reference',
                        help='Reference sequence file',
                        type=str)

    parser.add_argument('--string',
                        help='Reference sequence',
                        type=str)

    parser.add_argument('--query_range',
                        help='Query range (start stop step)',
                        nargs=3,
                        required=True,
                        type=int)

    parser.add_argument('--out_file',
                        help='File to output results to',
                        type=str,
                        required=True)

    return parser.parse_args()

def get_random_query(string, length):
    if length > len(string):
        raise ValueError("Length of substring is longer than the string.")

    query = ""
    alphabet = ['A', 'C', 'T', 'G']

    for i in range(length):
        query = query + random.choice(alphabet)

    return query

def run_test(test_build, test_function, T, query_len, i):
    query = get_random_query(T, query_len)

    start = time.monotonic_ns()
    s = test_build(T) 
    if i == 2:
        r = test_function(T, s, query)
    else:
        r = test_function(s, query)
    stop = time.monotonic_ns()

    tracemalloc.start()
    s = test_build(T)
    if i == 2:
        r = test_function(T, s, query)
    else:
        r = test_function(s, query)
    mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return r, stop - start, mem[1] - mem[0]


def test_harness(test_builds, test_functions, T, query_range):
    run_times = [ [] for _ in range(len(test_functions))]
    mem_usages = [ [] for _ in range(len(test_functions))]
    match_lens = [ [] for _ in range(len(test_functions))]

    for i, test_function in enumerate(test_functions):
        for query_len in query_range:
            match_len, run_time, mem_usage = run_test(test_builds[i], test_function, T, query_len, i)
            run_times[i].append(run_time)
            mem_usages[i].append(mem_usage)
            match_lens[i].append(match_len)

    return match_lens, run_times, mem_usages

def main():
    args = get_args()

    T = None

    if args.string:
        T = args.string
    elif args.reference:
        reference = utils.read_fasta(args.reference)
        T = reference[0][1]
        T = T[0:1000] # needed for large space of suffix_trie

    query_range = range(args.query_range[0], args.query_range[1], args.query_range[2])


    test_builds = [ suffix_trie.build_suffix_trie, suffix_tree.build_suffix_tree, suffix_array.build_suffix_array ]
    test_functions = [ suffix_trie.search_trie, suffix_tree.search_tree, suffix_array.search_array ]
    search_structures = [ "Suffix Trie", "Suffix Tree", "Suffix Array", ]

    match_lens, run_times, mem_usages = test_harness(test_builds, test_functions, T, query_range)

    height = 8
    width = 10
    fig, axs = plt.subplots(3, 1, figsize=(width, height))

    for i, search_structure in enumerate(search_structures):
        ax = axs[0]
        ax.plot(query_range, run_times[i], label=search_structure)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax = axs[1]
        ax.plot(query_range, mem_usages[i], label=search_structure)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        ax = axs[2]
        ax.plot(query_range, match_lens[i], label=search_structure)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    axs[0].set(ylabel='Run Time (ns)', title='Run Times vs. Query Size')
    axs[0].legend(loc='best', frameon=False)
    axs[1].legend(loc='best', frameon=False)
    axs[2].legend(loc='best', frameon=False)
    axs[1].set(ylabel='Memory Usage', title='Memory Usage vs. Query Size')
    axs[2].set(ylabel='Match Length (chars)', title='Match Length vs. Query Size', xlabel='Query Size (chars)')

    plt.tight_layout()
    plt.savefig(args.out_file)


if __name__ == '__main__':
    main()