import sys
import unittest
import tweets_cleaned
import average_degree
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

tweet6: {"created_at": "Thu Oct 29 18:10:49 +0000 2015", "text":
"\u00b7\u00a3"}
"""


class TweetsCleanedTest(unittest.TestCase):
    def setUp(self):
        test_input_location = os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), "test_files"), "tweets_cleaned_test.txt")
        self.tweets = tweets_cleaned.get_tweets_text_and_time(test_input_location)

        self.expected_text_array = [
            "I'm at Terminal de Integrao do Varadouro in Joo Pessoa, "  # tweet 1
            "PB https://t.co/HOl34REL1a (timestamp: Thu Oct 29 18:10:49 +0000 2015)",
            "6A has decided to postpone final vote until appeals are heard by executive board. "  # tweet 2
            "What seems set: 7 regions. (timestamp: Thu Oct 29 17:51:51 +0000 2015)",
            "@i_am_sknapp Thanks for following us, Seth. (timestamp: Thu Oct 29 18:10:49 +0000 2015)",  # tweet 3
            "#Football Card Specialist - SDPW  Tips 170 Won 88 Profit +219.10 ROI 12.89%  "  # tweet 4
            "1 Tip from #LaLiga this evening &gt;&gt;&gt; https://t.co/tdkGo2rCKa "
            "(timestamp: Fri Oct 30 15:29:45 +0000 2015)",
            "@lezlielowe That one for @skimber is *literally* the only name I can take credit (blame) for. "  # tweet 5
            "Thanks for noticingyou really are magical. (timestamp: Thu Oct 29 18:10:49 +0000 2015)",
            " (timestamp: Thu Oct 29 18:10:49 +0000 2015)",  # tweet 6
            "\n3 tweets contained unciode"  # final with empty line for styling
        ]

        self.expected_output = ""
        for expected_text in self.expected_text_array:
            self.expected_output += expected_text + "\n"

    def test_e2e_tweets_cleaned(self):
        tweets_cleaned.format_and_print_tweets(self.tweets)
        output = sys.stdout.getvalue()
        self.assertEqual(self.expected_output, output)


"""
Raw JSON for averag_degree_test
First three make sure don't do anything
tweet1: {"created_at":"Fri Oct 30 00:00:00 +0000 2015", "hashtags": ["Trump"]}
tweet2: {"created_at":"Fri Oct 30 00:00:00 +0000 2015", "hashtags": []}
tweet3: {"created_at":"Fri Oct 30 00:00:00 +0000 2015", "hashtags": ["kusugawa", "\u4e45\u5bff\u5ddd"]}
avg should be 0.00 for all 3.

tweet4: {"created_at":"Fri Oct 30 00:00:00 +0000 2015", "hashtags": ["Trump", "Election", "News"]}
avg should be 2.00
tweet5: {"created_at":"Fri Oct 30 00:00:10 +0000 2015", "hashtags": ["hiring", "BusinessMgmt", "NettempsJobs",
"MenloPark", "Job", "Jobs", "CareerArc"]}
avg should be (6 * 7 + 2 * 3) / 10 = 4.80


tweet6: {"created_at":"Fri Oct 30 00:00:20 +0000 2015", "hashtags": ["tRuMp", "Rhonda"]}
avg should be 6 * 7 + 1 * 1 + 2 * 2 + 3 * 1 / 11 = 4.55

tweet7: {"created_at":"Fri Oct 30 00:00:30 +0000 2015", "hashtags": ["\u00e7trU\u00e7Mp", "LaLiga"]}
avg should be 6 * 7 + 1 * 1 + 1 * 1 + 2 * 2 + 4 * 1 / 11 = 4.33
tweet8: {"created_at":"Fri Oct 30 00:00:40 +0000 2015", "hashtags": ["\u00e7trU\u00e7mP", "LalIga"]}
avg should still be be 6 * 7 + 1 * 1 + 1 * 1 + 2 * 2 + 4 * 1 / 11 = 4.33

tweet9: {"created_at":"Fri Oct 30 00:01:01 +0000 2015", "hashtags": ["a", "b"]}
avg should be 6 * 7 + 2 * 1 + 1 * 4 / 12 = 4.00

tweet10: {"created_at":"Fri Oct 30 00:01:31 +0000 2015", "hashtags": []}
avg should be 1 * 4 / 4 = 1.00

tweet11: {"created_at":"Fri Oct 30 00:03:00 +0000 2015", "hashtags": []}
avg should be 0.00

"""


class AverageDegreeTest(unittest.TestCase):
    def setUp(self):
        test_input_location = os.path.join(os.path.join(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))), "test_files"), "average_degree_test.txt")
        self.tweets = average_degree.get_tweets_hashtags_and_time(test_input_location)

        self.expected_avg_array = [0.00, 0.00, 0.00, 2.00, 4.80, 4.55, 4.33, 4.33, 4.00, 1.00, 0.00]
        self.expected_output = ""
        for expected_value in self.expected_avg_array:
            self.expected_output += "%.2f" % expected_value + "\n"

    def test_e2e_averge_degree(self):
        average_degree.format_and_print_averages(self.tweets)
        output = sys.stdout.getvalue()
        self.assertEqual(self.expected_output, output)


if __name__ == '__main__':
    # Need to do this to test the output.
    unittest.main(module=__name__, buffer=True, exit=False)
