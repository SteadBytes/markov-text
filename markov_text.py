import random
import os
import re
base_dir = os.path.dirname(os.path.realpath(__file__))


class FrequencyDistribution(dict):
    def __init__(self, iterable=None):
        super().__init__()
        self.types = 0  # num distinct items
        self.tokens = 0  # total items
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        """ Update distribution with items in `iterable`
        """
        for item in iterable:
            if item in self:
                self[item] += 1
                self.tokens += 1
            else:
                self[item] = 1
                self.types += 1
                self.tokens += 1

    def count(self, item):
        """ Return total count of given item
        Args:
            item (hashable:) Key of item
        Returns:
            int: Count of item in distribution or 0 if not present
        """
        if item in self:
            return self[item]
        return 0

    def max_l_item(self):
        """ Returns maximuim likelihood (frequency) item from the distribution
        """
        return max(self, key=lambda k: self[k])

    def rand_weighted_item(self):
        """ Returns a random item from the distribution weighted by likelihood
        """
        random_int = random.randint(0, self.tokens - 1)
        index = 0
        list_of_keys = list(self.keys())
        for i in range(0, self.types):
            index += self[list_of_keys[i]]
            if(index > random_int):
                return list_of_keys[i]

    def random_item(self):
        """ Return a random item from the distribution
        """
        random_key = random.sample(self, 1)
        return random_key


class MarkovChain:
    def __init__(self, order=1):
        self.order = order
        self.freqs = dict()

    def train(self, corpus):
        """ Populates self.freqs using data in corpus.

        If self.order=1: self.freqs keys are words

        For self.order = n > 1: self.freqs keys are n-tuples

        Each item in self.freqs is a FrequencyDistribution of words following
        the key.
        """
        words = [w.lower() for w in corpus.split()]
        n = self.order
        for i in range(0, len(words) - n):
            if n == 1:
                window = words[i]
            else:
                window = tuple(words[i:i + n])
            if window in self.freqs:
                self.freqs[window].update([words[i + n]])
            else:
                self.freqs[window] = FrequencyDistribution([words[i + n]])

    def generate_raw(self, start=None, max_len=0):
        """ Generator for text based on trained data.

        Args:
            start (str): Word/n-tuple to start with. Default = None
            max_len (int): Maximum number of words generated. Default = 0
        Yields:
            str: Next generated word
        """
        if len(self.freqs) == 0:
            return

        n_tuples = self.order > 1

        if start:
            key = start
        else:
            key = random.choice(list(self.freqs.keys()))

        if n_tuples:
            yield ' '.join(key)
        else:
            yield key

        n = self.order
        i = n
        while max_len == 0 or i < max_len:
            i += n
            if key not in self.freqs:
                return
            next_freqs = self.freqs[key]
            next_word = next_freqs.rand_weighted_item()
            if n_tuples:
                key = key[1:] + tuple([next_word])
            else:
                key = next_word
            yield next_word

    def generate_text(self, word_wrap=80, start=None, max_len=0):
        """ Wrapper around generate_raw() to include formatting with capital
        letters, text wrapping and new lines.

        Args:
            word_wrap (int): Max line length to wrap text at. Default = 80
            start (str): Word/n-tuple to start with. Default = None
            max_len (int): Maximum number of words generated. Default = 0
        Yields:
            str: Formatted next word
        """
        # can be changed depending on text?
        capitalize_chars = '.?!"'
        newline_chars = '.?!'

        char_count = 0
        # If capitalization is required, make the first word capitalized,
        # by making last_char a capitalize_char
        last_char = capitalize_chars[0] if len(capitalize_chars) > 0 else ''

        for w in self.generate_raw(start=start, max_len=max_len):
            # Capitalize if last character was a capitalization character,
            # or if the first one of new word is.
            if last_char in capitalize_chars:
                w_str = w.capitalize()
            elif w[0] in capitalize_chars:
                w_str = w[0] + w[1:].capitalize()
            else:
                w_str = w

            # add appropriate whitespace between words.
            w_str += ' ' if w[-1] not in newline_chars else '\n'

            if word_wrap > 0:
                char_count += len(w_str)
                if w_str[-1] == '\n':
                    char_count = 0
                if char_count >= word_wrap:
                    w_str += '\n'
                    char_count = 0
            yield w_str
            # actual last char will be space or '\n' now so -2 to get letter
            last_char = w_str[-2]


# TODO: Move into model/Split up classes
with open(os.path.join(base_dir, 'TRAINING_TEXT.txt'), encoding='utf8') as f:
    corpus = f.read()

model = MarkovChain(order=3)
# TODO: Add more text cleaning

# remove 'Chapter II' etc
pattern = ('(Chapter (?=[MDCLXVI])M*(C[MD]|D?C{0,3})' +
           '(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}))')
cleaned = re.sub(pattern, '', corpus)
model.train(cleaned)
print(''.join([w for w in model.generate_text(max_len=200)]))
