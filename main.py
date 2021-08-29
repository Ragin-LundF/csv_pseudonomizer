import getopt
import mmap
import random
import re
import string
import sys
import timeit
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence, Dict

from tqdm import tqdm

abv = re.compile(r'^(([A-Z]\.){1,})(_|[^\w])')  # A.B.C.
word = re.compile(r'^(([a-zA-Z]){1,})(_|[^\w])')  # ABC | Abc | abc

base = "googlebooks-eng-all-1gram-20120701-"
files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', \
         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', \
         't', 'u', 'v', 'w', 'x', 'y', 'z']


def process_file(file):
    global base
    vocab = {}
    fsize = Path(base + file).stat().st_size
    tot = 0
    print(f"processing {base + file}")
    with open(base + file, "r+b") as fp:
        # use a progress bar
        with tqdm(total=fsize, desc=file) as pbar:
            # map the entire file into memory, normally much faster than buffered i/o
            mm = mmap.mmap(fp.fileno(), 0)
            # iterate over the block, until next newline
            for line in iter(mm.readline, b""):
                t = ''
                # convert the bytes to a utf-8 string and split the fields
                term = line.decode("utf-8").split("\t")
                # catch patterns such as A.B.C. (old-style abbreviations)
                m_abv = abv.findall(term[0])
                if m_abv:
                    # remove punctuation
                    t = re.sub(r'[^\w]', '', m_abv.group(1))
                else:
                    m_word = word.findall(term[0])
                    if m_word:
                        t = m_word.group(1)
                # add it to dictionary if not yet included and add its match_count   
                if t in vocab:
                    vocab[t] += int(term[2])
                else:
                    vocab[t] = int(term[2])
                # update the progress bar
                tot += len(line)
                pbar.update(tot - pbar.n)
            mm.close()
    fp.close()
    # output vocabulary and counts to csv file
    outf = "gbooks-en-" + file + ".csv"
    with open(outf, "a+") as fp:
        for term in vocab:
            fp.write(f"{term}\t{vocab[term]}\n")
    fp.close()


# ------
@dataclass
class Node:
    is_term: bool = False
    children: Dict[str, "Node"] = field(default_factory=dict)


@dataclass
class Trie:
    root: Node = Node()
    min_depth: int = 0

    def __init__(self, patterns: Sequence[str] = None):
        """
        Initially build a trie from search-strings.
        """
        super().__init__()
        if patterns is not None:
            for pattern in patterns:
                self.insert(pattern)

    def insert(self, pattern: str):
        l = len(pattern)
        self.min_depth = (min(l, self.min_depth) if self.min_depth > 0 else l)
        node = self.root
        for char in pattern:
            node = node.children.setdefault(char, Node())
        node.is_term = True

    def search(self, s: str) -> bool:
        """
        Check if a string contains any substring contained in the trie.
        """
        for i in range(len(s) - self.min_depth + 1):
            node = self.root
            for char in s[i:]:
                if char in node.children:
                    node = node.children[char]
                    if node.is_term:
                        return True
                else:
                    break
        return False

    # The rest is for quick and dirty testing.
#    def rand_string(min_length, max_length):
#        return "".join(
#            random.SystemRandom().choice(string.ascii_uppercase)
#            for _ in range(random.SystemRandom().choice(range(min_length, max_length)))
#        )

    # print("generate patterns")
    # start = timeit.default_timer()
    # patterns = [rand_string(3, 25) for _ in range(1_000)]
    # print(f"\tcount: {len(patterns)}")
    # print(f"\tseconds: {round(timeit.default_timer() - start, 2)}s")

    # print("build trie")
    # start = timeit.default_timer()
    # trie = Trie(patterns)
    # print(f"\tseconds: {round(timeit.default_timer() - start, 2)}s")
    #
    # random_pattern = random.SystemRandom().choice(patterns)
    # assert trie.search(f"HELLO {random_pattern} WORLD")
    # assert not trie.search(f"lowercase {random_pattern.lower()} is not in trie")
    #
    # acc = 0
    # measurements = 1_000
    # for _ in range(measurements):
    #     test = rand_string(20, 200)
    #     start = timeit.default_timer()
    #     trie.search(test)
    #     acc += timeit.default_timer() - start
    #
    # print(f"Time for {measurements} tests: {acc}")


# ------


# use as many threads as possible, default: min(32, os.cpu_count()+4)
with ThreadPoolExecutor() as executor:
    result = executor.map(process_file, files)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "di:o:", ["dummy", "input=", "output="])
    except getopt.GetoptError:
        print("main.py -i <inputfile> -o <outputfile> -d <true|false>")
        sys.exit(2)

    should_process = True
    input_file = ""
    output_file = ""

    for opt, arg in opts:
        if opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-d", "--dummy"):
            from generator.dummydata import generate_dummy_data
            should_process = False
            generate_dummy_data()

    if should_process:
        process_file(input_file)


if __name__ == "__main__":
    main()
