import json
from enum import Enum

CONST_JSON_TEXT = "text"
CONST_JSON_CREATED_AT = "created_at"
CONST_JSON_ENTITIES = "entities"
CONST_JSON_HASHTAGS = "hashtags"
CONST_JSON_HASHTAG_TEXT = "text"
_Assignment = Enum("Assignment", "filter_unicode avg_hashtag_graph")


def parse_tweets_text_and_created_at_time(filename):
    return parse_tweets(filename, {CONST_JSON_CREATED_AT: [CONST_JSON_CREATED_AT],
                                   CONST_JSON_TEXT: [CONST_JSON_TEXT]}, _Assignment.filter_unicode)


def parse_tweets_hashtag_and_created_at_time(filename):
    return parse_tweets(filename, {CONST_JSON_CREATED_AT: [CONST_JSON_CREATED_AT],
                                   CONST_JSON_HASHTAGS: [CONST_JSON_ENTITIES, CONST_JSON_HASHTAGS]},
                        _Assignment.avg_hashtag_graph)


def parse_tweets(filename, json_fields_dict, assignment):
    with open(filename) as tweet_file:
        tweets = []
        for line in tweet_file:
            tweet_json = json.loads(line)
            json_fields_dict_values = json_fields_dict.values()
            # if False in is_wellformed_json_generator(tweet_json, json_fields_dict_values):
            #     continue

            tweet = {}
            # since we only need these two fields, only save these two to save space.
            if assignment == _Assignment.filter_unicode:
                try:
                    for key, value in json_fields_dict.iteritems():
                        tweet[key] = nested_json_fields_value(tweet_json, value)
                except ValueError: #usually happens if some tweet doesn't have the right keys. Can skip.
                    continue

            elif assignment == _Assignment.avg_hashtag_graph:
                hashtags = set()  # set to ensure uniqness.
                tweet[CONST_JSON_CREATED_AT] = tweet_json[CONST_JSON_CREATED_AT]
                print type(tweet_json[CONST_JSON_ENTITIES][CONST_JSON_HASHTAGS])
                for inner_hashtag_object in tweet_json[CONST_JSON_ENTITIES][CONST_JSON_HASHTAGS]:
                    decoded_string = inner_hashtag_object[CONST_JSON_HASHTAG_TEXT]\
                        .encode('ascii', errors='ignore').lower()
                    hashtags.add(decoded_string)

                # if less than 2 unique hashtags, don't add it.
                if len(hashtags) < 2:
                    continue
                tweet[CONST_JSON_HASHTAGS] = hashtags
            else:
                raise ValueError("Wrong input assignment for parse_tweets")

            tweets.append(tweet)

        return tweets

#TODO: Since clean for both number 1 and number 2 should probably move it here.

def nested_json_fields_value(tweet_json, nested_json_fields):
    if not nested_json_fields:
        raise LookupError("Got a malformed json key list")

    value = tweet_json.get(nested_json_fields[0])

    if not value:  # empty json key. might just be malformed tweet, skip.
        raise ValueError
    elif type(value) == dict:  # nested json object, recurse.
        return nested_json_fields_value(value, nested_json_fields[1:])
    elif type(value) == list and type(value[0]) == dict:  # array of nested json objects, recurse.
        response_list = []
        for item in value:
            response_list.append(nested_json_fields(item, nested_json_fields[1:]))
        return response_list
    else:  # anything else is the correct response. 
        return value


# def nested_json_fields_value(tweet_json, nested_json_fields):
#     for field in nested_json_fields:
#         tweet_json = tweet_json[field]
#     return tweet_json


def is_wellformed_json_generator(tweet_json, nested_json_fields_list):
    for nested_json_fields in nested_json_fields_list:
        yield json_contains_field(tweet_json, nested_json_fields)


def json_contains_field(tweet_json, nested_json_fields):
    for field in nested_json_fields:
        if field not in tweet_json:
            return False
        tweet_json = tweet_json[field]
    return True
