import random
from ngram import NGramDistribution
from parse import Parser


class TextGenerator:
    def __init__(self, distribution: NGramDistribution):
        self.distribution = distribution
        self.order = distribution.order

    def weighted_random_choice(self, choices):
        total = sum(c[1] for c in choices)
        rnd = random.uniform(0, total)
        cum_total = 0
        for key, freq in choices:
            cum_total += freq
            if cum_total > rnd:
                return key

    def get_next_token(self, prev):
        if prev in self.distribution.dict:
            choices = [(k, f) for k, f in self.distribution.dict[prev].items()]
        else:
            return None
        if not choices:
            return None
        k = self.weighted_random_choice(choices)
        return k

    def generate_sentence(self):
        sentence = [Parser.START_SENTENCE_TOKEN] * (self.order)
        end_sequence = [Parser.END_SENTENCE_TOKEN] * (self.order)

        while True:
            sentence_tail = sentence[(-self.order):]
            if sentence_tail == end_sequence:
                break
            next_token = self.get_next_token(tuple(sentence_tail))
            if next_token:
                sentence.append(next_token)
            else:
                break
        return (' '.join(sentence[self.order:-self.order]) + '.').capitalize()
