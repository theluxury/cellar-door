# example of program that calculates the average degree of hashtags

import networkx
import json_helper
import sys
import itertools
import collections
import config
from dateutil.parser import parse as date_parse
from dateutil.relativedelta import relativedelta

_TIME_LIMIT_IN_SECONDS = 60


def main():
    tweets = get_tweets_hashtags_and_time(sys.argv[1])
    # Can remove this sort for performance since they said they'd sort it.
    # sorted_tweets = sorted(tweets, key=lambda t: t[config.TWEET_DICTIONARY_DATE_TIME_KEY])
    format_and_print_averages(tweets)


def get_tweets_hashtags_and_time(filename):
    request1 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
    request2 = json_helper \
        .JsonRequestList(config.TWEET_DICTIONARY_HASHTAGS_KEY, config.TWEET_JSON_HASHTAGS_LOCATION,
                         require_lower_case=True, require_ascii_format=True,
                         require_unique_elements=True)
    return json_helper.parse_tweets(filename, [request1, request2])


def format_and_print_averages(tweets):
    # deque to check for how many edges to remove when adding new tweet.
    deque = collections.deque()
    graph = networkx.Graph()
    for tweet in tweets:
        update_graph_and_deque(tweet, graph, deque, _TIME_LIMIT_IN_SECONDS)
        print avg_edges_per_node(graph)


def update_graph_and_deque(tweet, graph, deque, seconds_to_go_back):
    # since the hashtags have been encoded to ascii and made unique, this should only increment the edge
    # if and only if tweet had set of >=2 hashtags.
    if len(tweet[config.TWEET_DICTIONARY_HASHTAGS_KEY]) >= 2:
        add_hashtags_to_graph_and_tweet_to_deque(tweet, graph, deque)
    # Even if tweet does not have >=2 unique hashtags, still use to remove old tweets.
    time_limit = date_parse(tweet[config.TWEET_DICTIONARY_DATE_TIME_KEY]) - relativedelta(seconds=seconds_to_go_back)
    remove_old_hashtags_from_graph_and_tweets_from_deque(time_limit, graph, deque)


def add_hashtags_to_graph_and_tweet_to_deque(tweet, graph, deque):
    for x, y in itertools.combinations(tweet[config.TWEET_DICTIONARY_HASHTAGS_KEY], 2):
        increment_edge(x, y, graph)
    deque.append(tweet)


def increment_edge(x, y, graph):
    weight = graph.get_edge_data(x, y, {'weight': 0})["weight"]
    graph.add_edge(x, y, weight=weight + 1)


def remove_old_hashtags_from_graph_and_tweets_from_deque(time_limit, graph, deque):
    while deque and date_parse(deque[0][config.TWEET_DICTIONARY_DATE_TIME_KEY]) <= time_limit:
        # removes from head until we get one less than 1 minute prior.
        stale_tweet = deque.popleft()
        for x, y in itertools.combinations(stale_tweet[config.TWEET_DICTIONARY_HASHTAGS_KEY], 2):
            decrement_edge(x, y, graph)


def decrement_edge(x, y, graph):
    # TODO: Maybe document tests a bit.
    # TODO: Document, uh...error handling. Yeah, that.
    # Designed to crash if we try to decement an edge that doesn't exist.
    # This is designed behavior since that means rolling average is not accurate.
    try:
        weight = graph.get_edge_data(x, y)["weight"]
    except TypeError:
        error_msg = "Tried to decrement edge (%s, %s) that doesn't exist. " \
                    "Something went wrong: check the input data." % (x, y)
        config.logger.critical(error_msg)
        raise TypeError(error_msg)
    if weight == 1:
        graph.remove_edge(x, y)
        for node in [x, y]:
            check_node_for_removal(node, graph)
    else:
        graph.add_edge(x, y, weight=weight - 1)


def check_node_for_removal(node, graph):
    if not graph.neighbors(node):
        graph.remove_node(node)


def avg_edges_per_node(graph):
    if graph.number_of_nodes():
        return "%.2f" % (graph.number_of_edges() * 2 / float(graph.number_of_nodes()))
    else:
        return "%.2f" % 0.00


if __name__ == '__main__':
    main()
