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
    tweets = get_tweets_text_and_time(sys.argv[1])
    format_and_print_tweets(tweets)


def get_tweets_text_and_time(filename):
    request1 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
    request2 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_TEXT_KEY, config.TWEET_JSON_TEXT_LOCATION)
    return json_helper.parse_tweets(filename, [request1, request2])


def format_and_print_tweets(tweets):
    count = 0
    for tweet in tweets:
        # TODO: Make note of fact json.loads get rid of a lot of escapes in readme
        escapes_removed_string = remove_whitespace_escapes(tweet[config.TWEET_DICTIONARY_TEXT_KEY])
        # normally could actually make ascii in request, but doing it here for count.
        decoded_string = json_helper.make_ascii(escapes_removed_string)
        if decoded_string != escapes_removed_string:
            count += 1

        print "%s (timestamp: %s)" % (decoded_string, tweet[config.TWEET_DICTIONARY_DATE_TIME_KEY])

    print  # empty line for styling.
    print "%d tweets contained unciode" % count


def remove_whitespace_escapes(original_string):
    return original_string.replace("\r\n", " ").replace("\r", " ").replace("\n", " ") \
        .replace("\t", " ").replace("\b", " ").replace("\v", " ")


if __name__ == '__main__':
    main()
