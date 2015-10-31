import json
from enum import Enum

CONST_JSON_TEXT = "text"
CONST_JSON_CREATED_AT = "created_at"
CONST_JSON_ENTITIES = "entities"
CONST_JSON_HASHTAGS = "hashtags"
CONST_JSON_HASHTAG_TEXT = "text"
_Assignment = Enum("Assignment", "filter_unicode avg_hashtag_graph")


class JsonRequest:
    def __init__(self, key, json_chain, to_lower=False, make_ascii=False):
        self.key = key
        self.json_chain = json_chain
        self.to_lower = to_lower
        self.make_ascii = make_ascii

class JsonRequestList(JsonRequest):
    def __init__(self, key, json_chain, to_lower=False, make_ascii=False, make_unique=False, min_length=1):
        JsonRequest.__init__(self, key, json_chain, to_lower, make_ascii)
        self.make_unique = make_unique
        self.min_length = min_length


def parse_tweets_hashtag_and_created_at_time(filename):
    request1 = JsonRequest(CONST_JSON_CREATED_AT, [CONST_JSON_CREATED_AT])
    request2 = JsonRequestList(CONST_JSON_HASHTAGS, [CONST_JSON_ENTITIES, CONST_JSON_HASHTAGS, CONST_JSON_TEXT],
                               to_lower=True, make_unique=True, min_length=2)
    return parse_tweets(filename, [request1, request2])


def parse_tweets(filename, requests_list):
    with open(filename) as tweet_file:
        tweets = []
        for line in tweet_file:
            tweet_json = json.loads(line)
            tweet = {}
            try:
                for request in requests_list:
                    value = nested_json_fields_value(tweet_json, request.json_chain)
                    value = format_value(value, request)
                    tweet[request.key] = value
                tweets.append(tweet)
            except ValueError:  # usually happens if some tweet doesn't have the right keys or lists to add
                                # don't have the required length. Can skip.
                continue

        return tweets



def format_value(value, request):
    if request.__class__ == JsonRequest:
        return format_primitive_value(value, request)
    elif request.__class__ == JsonRequestList:
        return format_list_value(value, request)
    else:
        raise ValueError("Got an odd JSON request.")


def format_list_value(list, request):
    placeholder_list = []
    for value in list:
        placeholder_list.append(format_primitive_value(value, request))

    if request.make_unique:
        placeholder_list = make_unique(placeholder_list)

    if len(placeholder_list) < request.min_length:
        raise ValueError("List doesn't contain minimum amount of elements needed to be added.")
    return placeholder_list


def format_primitive_value(value, request):
    if isinstance(value, basestring):
        if request.to_lower:
            value = value.lower()
        if request.make_ascii:
            value = make_ascii(value)

    return value


# TODO: test this funciton.
def make_unique(input_list):
    placeholder_set = set()
    try:
        for item in input_list:
            placeholder_set.add(item)
    except TypeError:
        raise TypeError("Could not make elements in list unique. "
                        "This is usually because the elements are not hashtable.")

    return list(placeholder_set)


def make_ascii(text):
    return text.encode('ascii', errors='ignore')


def nested_json_fields_value(tweet_json, nested_json_fields):
    if not nested_json_fields:
        raise LookupError("Got a malformed json key list: list did not conclude with value.")

    value = tweet_json.get(nested_json_fields[0])

    if not value:  # empty json key. might just be malformed tweet, skip.
        raise ValueError
    elif type(value) == dict:  # nested json object, recurse.
        return nested_json_fields_value(value, nested_json_fields[1:])
    elif type(value) == list and type(value[0]) == dict:  # array of nested json objects, recurse.
        response_list = []
        for item in value:
            response_list.append(nested_json_fields_value(item, nested_json_fields[1:]))
        return response_list
    else:  # candidates for return
        if nested_json_fields[1:]:
            # still have unused fields in nested_json_fields, so should raise error.
            raise LookupError("Could not finish json key lookup chain: found value before list concluded.")
        else:
            return value

