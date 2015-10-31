# example of program that calculates the number of tweets cleaned

import sys
import json_helper

"""
Note: also tried decoded = filter(lambda x: x in string.printable, tweet["text"]) for decoding, but that was much slower
"""


def main():
    request1 = json_helper.JsonRequest(json_helper.CONST_JSON_CREATED_AT, [json_helper.CONST_JSON_CREATED_AT])
    request2 = json_helper.JsonRequest(json_helper.CONST_JSON_TEXT, [json_helper.CONST_JSON_TEXT])
    tweets = json_helper.parse_tweets(sys.argv[1], [request1, request2])
    count = 0
    for tweet in tweets:
        # normally could actaully make ascii in request, but doing it here for count.
        decoded_string = json_helper.make_ascii(tweet[json_helper.CONST_JSON_TEXT])
        if decoded_string != tweet[json_helper.CONST_JSON_TEXT]:
            count += 1

        print "%s (timestamp: %s)" % (decoded_string, tweet[json_helper.CONST_JSON_CREATED_AT])

    # print()  # empty line for styling.
    print "%d tweets contained unciode" % count

if __name__ == '__main__':
    main()
