# example of program that calculates the number of tweets cleaned

import sys
import json_helper
import config

"""
Note: also tried decoded = filter(lambda x: x in string.printable, tweet["text"]) for decoding, but that was much slower
"""


def main():
    request1 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
    request2 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_TEXT_KEY, config.TWEET_JSON_TEXT_LOCATION)
    tweets = json_helper.parse_tweets(sys.argv[1], [request1, request2])
    count = 0
    for tweet in tweets:
        # normally could actually make ascii in request, but doing it here for count.
        decoded_string = json_helper.make_ascii(tweet[config.TWEET_DICTIONARY_TEXT_KEY])
        if decoded_string != tweet[config.TWEET_DICTIONARY_TEXT_KEY]:
            count += 1

        print "%s (timestamp: %s)" % (decoded_string, tweet[config.TWEET_DICTIONARY_DATE_TIME_KEY])

    print()  # empty line for styling.
    print "%d tweets contained unciode" % count

if __name__ == '__main__':
    main()
