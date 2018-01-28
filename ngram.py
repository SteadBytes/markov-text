import pickle


class NGramDistribution:
    def __init__(self, order=2):
        self.dict = {}
        self.order = order

    def update(self, dist, token):
        if token in dist:
            dist[token] += 1
        else:
            dist[token] = 1

    def insert(self, window, token):
        if window in self.dict:
            self.update(self.dict[window], token)
        else:
            self.dict[window] = {token: 1}

    def save_to_file(self, fp, verbose=True):
        with open(fp, 'wb') as f:
            pickle.dump({'dict': self.dict, 'order': self.order}, f)
        if verbose:
            print(f'{self} saved to {fp}')

    def from_file(self, fp, verbose=True):
        with open(fp, 'rb') as f:
            data = pickle.load(f)
        self.dict = data['dict']
        self.order = data['order']
        if verbose:
            print(f'Loaded data from {fp} into {self}')
