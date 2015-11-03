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
    request1 = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
    request2 = json_helper\
        .JsonRequestList(config.TWEET_DICTIONARY_HASHTAGS_KEY, config.TWEET_JSON_HASHTAGS_LOCATION,
                         require_lower_case=True, require_ascii_format=True,
                         require_unique_elements=True, min_length=2)
    tweets = json_helper.parse_tweets(sys.argv[1], [request1, request2])
    sorted_tweets = sorted(tweets, key=lambda t: t[config.TWEET_DICTIONARY_DATE_TIME_KEY])

    # deque to check for how many edges to remove when adding new tweet.
    deque = collections.deque()

    graph = networkx.Graph()
    for tweet in sorted_tweets:
        # since the hashtags have been encoded to ascii and made unique, this should only increment the edge
        # if and only if tweet had set of >=2 hashtags.
        if len(tweet.get(config.TWEET_DICTIONARY_HASHTAGS_KEY, [])) >= 2:
            for x, y in itertools.combinations(tweet[config.TWEET_DICTIONARY_HASHTAGS_KEY], 2):
                increment_edge(x, y, graph)
            deque.append(tweet)

        # However, even if does not have >=2, still use to remove old tweets.
        time_limit = date_parse(tweet[config.TWEET_DICTIONARY_DATE_TIME_KEY]) \
            - relativedelta(seconds=_TIME_LIMIT_IN_SECONDS)
        remove_old_tweets(time_limit, graph, deque)

        if graph.number_of_nodes():
            print "%.2f" % (graph.number_of_edges() * 2 / float(graph.number_of_nodes()))
        else:
            print 0.00


def remove_old_tweets(time_limit, graph, deque):
    while deque and date_parse(deque[0][config.TWEET_DICTIONARY_DATE_TIME_KEY]) < time_limit:
        # removes from head until we get one less than 1 minute prior.
        stale_tweet = deque.popleft()
        for x, y in itertools.combinations(stale_tweet[config.TWEET_DICTIONARY_HASHTAGS_KEY], 2):
            decrement_edge(x, y, graph)


def increment_edge(x, y, graph):
    weight = graph.get_edge_data(x, y, {'weight': 0})["weight"]
    graph.add_edge(x, y, weight=weight + 1)


def decrement_edge(x, y, graph):
    # No error here if no edge exists because of default value.
    weight = graph.get_edge_data(x, y, {'weight': 1})["weight"]
    if weight == 1:
        # error here if no such edge or node. Reason for three try loops is want to remove nodes for accuracy
        # even if it doesn't have edge.
        try:
            graph.remove_edge(x, y)
        except networkx.exception.NetworkXError:
            config.logger.error("Tried to remove a non existent edge (%s, %s)." % (x, y))

        # if these nodes don't have edges anymore, remove them
        for node in [x, y]:
            check_node_for_removal(node, graph)
    else:
        graph.add_edge(x, y, weight=weight - 1)


def check_node_for_removal(node, graph):
    try:
        if not graph.neighbors(node):
            graph.remove_node(node)
    except networkx.exception.NetworkXError:
        config.logger.error("Tried to remove a non existent node %s." % node)


if __name__ == '__main__':
    main()
