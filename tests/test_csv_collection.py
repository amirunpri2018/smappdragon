import os
import unittest
from tests.config import config
from smappdragon import CsvCollection

class TestCsvCollection(unittest.TestCase):

    def test_iterator_returns_tweets(self):
        collection = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        for tweet in collection.get_iterator():
            print(tweet)
        # self.assertTrue(len(list(collection.get_iterator())) > 0)

    # special test because custom logic is different on mongo
    def test_json_collection_custom_filter_filters(self):
        collectionone = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        full_collection_len = len(list(collectionone.get_iterator()))
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        num_retweets = len(list(collectionone.set_custom_filter(is_tweet_a_retweet).get_iterator()))

        collectiontwo = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        def is_not_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return False
            else:
                return True
        num_non_retweets = len(list(collectiontwo.set_custom_filter(is_not_a_retweet).get_iterator()))

        #the numbes of retweets and non retweets should add up to the whole collection
        self.assertEqual(num_retweets + num_non_retweets, full_collection_len)

if __name__ == '__main__':
    unittest.main()