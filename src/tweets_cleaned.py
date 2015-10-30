import json_helper
import sys
import time

"""
Note: also tried decoded = filter(lambda x: x in string.printable, tweet["text"]) for decoding, but that was much slower
"""

# example of program that calculates the number of tweets cleaned

def main():
    tweets = json_helper.parse_tweets(sys.argv[1])
    count = 0
    for tweet in tweets:
        decoded_string = tweet[json_helper.JSON_TEXT_CONST].encode('ascii',errors='ignore')
        if decoded_string != tweet[json_helper.JSON_TEXT_CONST]:
            count += 1

        print "%s (timestamp: %s)" %(decoded_string, tweet[json_helper.JSON_CREATED_AT_CONST])

    print() # empty line for stling.
    print "%d tweets contained unciode" %count

if __name__ == '__main__':
    main()