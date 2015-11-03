import logging as logger

LOG_LOCATION = "tweet_parser.log"
logger.basicConfig(filename=LOG_LOCATION, level=logger.DEBUG,
                   format='%(asctime)s.%(msecs)d %(levelname)s %(module)s '
                          '- %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

"""
***IMPORTANT***
Locations should be put in lists even if only one key.
"""
TWEET_JSON_DATE_TIME_LOCATION = ["created_at"]
TWEET_JSON_TEXT_LOCATION = ["text"]
TWEET_JSON_HASHTAGS_LOCATION = ["entities", "hashtags", "text"]

TWEET_DICTIONARY_DATE_TIME_KEY = "created_at"
TWEET_DICTIONARY_TEXT_KEY = "text"
TWEET_DICTIONARY_HASHTAGS_KEY = "hashtags"
