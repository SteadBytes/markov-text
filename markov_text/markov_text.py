import os
import sys
from .parse import Parser
from .text_gen import TextGenerator
from .ngram import NGramDistribution
# TODO: Bulk parse from CLI
# TODO: Better args parsing

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.realpath(__file__))
    args = sys.argv
    usage = f'Usage: {args[0]} (parse <name> <depth> <path to txt file>|gen <name> <count>)'

    if len(args) < 3:
        raise ValueError(usage)

    mode = args[1]
    ngram_name = args[2]

    if mode == 'parse':

        if len(args) != 5:
            raise ValueError(usage)

        order = int(args[3])
        fp = args[4]
        dist = NGramDistribution(order=order)
        p = Parser(dist)
        p.parse_file(fp)
        dist.save_to_file(os.path.join(base_dir, ngram_name + '.pkl'))
    elif mode == 'gen':
        num_sentences = int(args[3])
        dist = NGramDistribution()
        dist.from_file(os.path.join(base_dir, ngram_name + '.pkl'))
        print()
        m = TextGenerator(dist)
        for _ in range(num_sentences):
            print(m.generate_sentence())
