# example of program that calculates the number of tweets cleaned

import sys
import json_helper
from json_helper import CONST_JSON_TEXT, CONST_JSON_CREATED_AT

"""
Note: also tried decoded = filter(lambda x: x in string.printable, tweet["text"]) for decoding, but that was much slower
"""


def main():
    tweets = json_helper.parse_tweets_text_and_created_at_time(sys.argv[1])
    count = 0
    for tweet in tweets:
        decoded_string = tweet[CONST_JSON_TEXT].encode('ascii', errors='ignore')
        if decoded_string != tweet[CONST_JSON_TEXT]:
            count += 1

        print "%s (timestamp: %s)" % (decoded_string, tweet[CONST_JSON_CREATED_AT])

    # print()  # empty line for styling.
    print "%d tweets contained unciode" % count

if __name__ == '__main__':
    main()
