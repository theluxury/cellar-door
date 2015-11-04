import unittest
import tweets_cleaned

class TweetsCleanedTest(unittest.TestCase):
    def setUp(self):
        tweets = tweets_cleaned.get_tweets_text_and_time("")
