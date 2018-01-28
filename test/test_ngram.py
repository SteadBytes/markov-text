import unittest
from markov_text.ngram import NGramDistribution


class NGramDistributionTest(unittest.TestCase):
    def setUp(self):
        self.dist = NGramDistribution()
        self.test_window = ('test', 'window')

    def test_update_new_token(self):
        sub_dist = dict()
        token = 'token'
        self.dist.update(sub_dist, token)
        self.assertIn(token, sub_dist)
        self.assertEqual(sub_dist[token], 1)

    def test_update_existing_token(self):
        token = 'token'
        sub_dist = {token: 1}
        self.dist.update(sub_dist, token)
        self.assertEqual(sub_dist[token], 2)

    def test_insert_new_window(self):
        self.assertDictEqual(self.dist.dict, {})
        token = 'token'
        self.dist.insert(self.test_window, token)
        self.assertIn(self.test_window, self.dist.dict)
        self.assertIn(token, self.dist.dict[self.test_window])

    def test_insert_existing_window(self):
        self.dist.dict = {self.test_window: {}}
        self.assertIn(self.test_window, self.dist.dict)
        token = 'token'
        self.dist.insert(self.test_window, token)
        self.assertIn(token, self.dist.dict[self.test_window])

    def test_insert_existing_token(self):
        token = 'token'
        self.dist.dict = {self.test_window: {token: 1}}
        self.dist.insert(self.test_window, token)
        self.assertEqual(self.dist.dict[self.test_window][token], 2)


if __name__ == '__main__':
    unittest.main()
