import json
import config


# Don't instantiate this one directly.
class _JsonRequestBase(object):
    def __init__(self, key, json_chain, require_lower_case=False, require_ascii_format=False):
        self.key = key
        self.json_chain = json_chain
        self.require_lower_case = require_lower_case
        self.require_ascii_format = require_ascii_format


# Use this one for json keys where you expect a single value
class JsonRequestSingle(_JsonRequestBase):
    def __init__(self, key, json_chain, require_lower_case=False, require_ascii_format=False):
        _JsonRequestBase.__init__(self, key, json_chain, require_lower_case, require_ascii_format)


# Use this onefor json keys where you expect a list
class JsonRequestList(_JsonRequestBase):
    def __init__(self, key, json_chain, require_lower_case=False, require_ascii_format=False,
                 require_unique_elements=False):
        _JsonRequestBase.__init__(self, key, json_chain, require_lower_case, require_ascii_format)
        self.require_unique_elements = require_unique_elements


def parse_tweets(filename, requests_list):
    with open(filename) as tweet_file:
        tweets = []
        for line in tweet_file:
            tweet_json = json.loads(line)
            tweet = {}
            ignore_tweet = False
            for request in requests_list:
                try:
                    value = nested_json_fields_value(tweet_json, request.json_chain)
                except ValueError:
                    # this usually happens if the json is missing a vital field or if we got a wrong json line.
                    # behavior now is just to skip the line.
                    ignore_tweet = True
                    break
                value = format_value(value, request)
                tweet[request.key] = value

            if ignore_tweet:
                continue
            else:
                tweets.append(tweet)

        return tweets


def nested_json_fields_value(tweet_json, nested_json_fields):
    if not nested_json_fields or nested_json_fields[0] not in tweet_json:
        # bad json chain given, skip.
        config.logger.warning("Could not find value %s in %s, skipping." % (nested_json_fields[0], tweet_json))
        raise ValueError()

    value = tweet_json.get(nested_json_fields[0])
    if len(nested_json_fields) == 1:
        return value
    elif isinstance(value, list):
        # array of nested json objects or lists, recurse while adding to list.
        response_list = []
        for item in value:
            response_list.append(nested_json_fields_value(item, nested_json_fields[1:]))
        return response_list
    else:
        return nested_json_fields_value(value, nested_json_fields[1:])


def format_value(value, request):
    if isinstance(request, JsonRequestSingle):
        return format_primitive_value(value, request)
    elif isinstance(request, JsonRequestList):
        return format_list_value(value, request)
    else:
        raise ValueError("Got an odd JSON format request object.")


def format_primitive_value(value, request):
    if isinstance(value, basestring):
        if request.require_lower_case:
            value = value.lower()
        if request.require_ascii_format:
            value = make_ascii(value)

    return value


def format_list_value(values_list, request):
    placeholder_list = []
    for value in values_list:
        placeholder_list.append(format_primitive_value(value, request))

    # It's important that this happens after the formatting_primitive_values, since
    # we might want to make unique two elements that differ only in unicode or capitalization.
    if request.require_unique_elements:
        placeholder_list = make_unique(placeholder_list)

    return placeholder_list


def make_unique(input_list):
    placeholder_set = set()
    try:
        for item in input_list:
            placeholder_set.add(item)
    except TypeError:
        raise TypeError("Could not make elements in list unique. "
                        "This is usually because the elements are not hashable.")

    return list(placeholder_set)


def make_ascii(text):
    return text.encode('ascii', errors='ignore')
