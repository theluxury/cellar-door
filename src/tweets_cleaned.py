# example of program that calculates the number of tweets cleaned

import sys
import json_helper
import config

"""
Performance notes:
Tried decoded = filter(lambda x: x in string.printable, tweet["text"]) for decoding, but that was much slower
Also, the .replace chains to replace escape characters is considered the pythonic way to replace multiple characters.
If performance is slower, could consider for other ways, such as for ch in ['\r\n', '\r', ...]
Go to http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python for a fairly exahustive list.
"""


def main():
    request1 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
    request2 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_TEXT_KEY, config.TWEET_JSON_TEXT_LOCATION)
    tweets = json_helper.parse_tweets(sys.argv[1], [request1, request2])
    count = 0
    for tweet in tweets:
        escapes_removed_string = tweet[config.TWEET_DICTIONARY_TEXT_KEY].replace("\r\n", " ") \
        .replace("\r", " ").replace("\n", " ").replace("\t", " ").replace("\b", " ").replace("\v", " ")
        # normally could actually make ascii in request, but doing it here for count.
        decoded_string = json_helper.make_ascii(escapes_removed_string)
        if decoded_string != escapes_removed_string:
            count += 1

        print "%s (timestamp: %s)" % (decoded_string, tweet[config.TWEET_DICTIONARY_DATE_TIME_KEY])

    print()  # empty line for styling.
    print "%d tweets contained unciode" % count

if __name__ == '__main__':
    main()
