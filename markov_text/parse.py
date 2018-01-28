import re
import glob
from .ngram import NGramDistribution


class ParsingException(Exception):
    pass


class Parser:
    START_SENTENCE_TOKEN = '^'
    END_SENTENCE_TOKEN = '$'
    CHAPTER_REGEX = ('(Chapter (?=[MDCLXVI])M*(C[MD]|D?C{0,3})' +
                     '(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}))')

    def __init__(self, distribution: NGramDistribution, sentence_split='.', word_split=' '):
        self.distribution = distribution
        self.sentence_split = sentence_split
        self.word_split = word_split

    def _parse_sentence(self, sentence):
        sentence = re.sub(r'\s+', " ", sentence).strip().lower()

        words = sentence.split(self.word_split)
        start_tokens = [self.START_SENTENCE_TOKEN] * (self.distribution.order)
        end_tokens = [self.END_SENTENCE_TOKEN] * (self.distribution.order)

        return start_tokens + words + end_tokens

    def parse(self, corpus, save_to=None):
        corpus = re.sub(self.CHAPTER_REGEX, '', corpus)
        sentences = corpus.split(self.sentence_split)

        for sentence in sentences:
            tokens = self._parse_sentence(sentence)
            for i in range(len(tokens) - self.distribution.order):
                window = tuple(tokens[i:i + self.distribution.order])
                self.distribution.insert(
                    window, tokens[i + self.distribution.order])

    def parse_file(self, fp, encodings=None, verbose=True):
        # If not specified, use 2 most common encodings
        # https://w3techs.com/technologies/overview/character_encoding/all
        encodings = encodings if encodings else ['utf8', 'ISO-8859-1']
        success = False
        for i, encoding in enumerate(encodings):
            try:
                with open(fp, encoding=encoding) as f:
                    self.parse(f.read())
                    if verbose:
                        print(f'Successfully parsed {fp}')
                    success = True
                    break
            except UnicodeDecodeError:
                if verbose:
                    print(f'Unable to decode {fp} using {encoding}')
        if not success:
            raise ParsingException(
                f'Unable to decode {fp} using any of {encodings}')
        return success

    def bulk_parse(self, pathname, encodings=None, verbose=2):
        fail = []
        success = []
        for fp in glob.glob(pathname):
            try:
                self.parse_file(fp, encodings=encodings, verbose=verbose)
                success.append(fp)
            except ParsingException:
                fail.append(fp)
        if verbose:
            print(f'Parse complete: {len(success)} successful, {len(fail)} failed')
        if verbose == 2:
            if success:
                print('Success:\n  {}'.format('\n  '.join(success)))
            if fail:
                print('Fail:\n  {}'.format('\n  '.join(fail)))
