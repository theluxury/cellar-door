import sys
import unittest
import tweets_cleaned
import os.path


"""
Raw JSON for tweets_cleaned_test:
tweet1: {"created_at": "Thu Oct 29 18:10:49 +0000 2015", "text":
"I'm at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa, PB https:\/\/t.co\/HOl34REL1a"}

tweet2: {"created_at":"Thu Oct 29 17:51:51 +0000 2015",
"text":"6A has decided to postpone final vote until appeals are heard by executive board. What seems set: 7 regions."}

tweet3: {"created_at":"Thu Oct 29 18:10:49 +0000 2015",
"text":"@i_am_sknapp Thanks for following us, Seth."}

tweet4: {"created_at":"Fri Oct 30 15:29:45 +0000 2015","text":"#Football Card Specialist -
SDPW\n\nTips 170\nWon 88\nProfit +219.10\nROI 12.89%\n\n1 Tip from #LaLiga this evening
&gt;&gt;&gt; https:\/\/t.co\/tdkGo2rCKa"}

tweet5: {"created_at":"Thu Oct 29 18:10:49 +0000 2015",
"text":"@lezlielowe That one for @skimber is *literally* the only name I can take credit (blame) for.
Thanks for noticing\u2014you really are magical."}
"""


class TweetsCleanedTest(unittest.TestCase):
    def setUp(self):
        test_input_location = os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), "data-gen"), "tweets_cleaned_test.txt");
        self.tweets = tweets_cleaned.get_tweets_text_and_time(test_input_location)

    def test(self):
        tweets_cleaned.format_and_print_tweets(self.tweets)
        output = sys.stdout.getvalue()
        self.assertEqual("test", output)

if __name__ == '__main__':
    # Need to do this to test the output.
    unittest.main(module=__name__, buffer=True, exit=False)