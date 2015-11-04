import unittest
import json_helper
import config
import tweets_cleaned
import networkx
import average_degree

class TestParserMethods(unittest.TestCase):
    def setUp(self):
        self.correct_json = {"text": "sample text", "created_at": "Thu Oct 29 17:51:50 +0000 2015",
                "entities": [{"hashtags": {"text": "hashtag1"}}, {"hashtags": {"text": "hashtag2"}}]}
        self.incorrect_json = {"wrong_key": "sample text",
                   "entities": [{"hashtags": {"wrong_key": "hashtag1"}}, {"wrong_key": {"text": "hashtag2"}}]}

        self.correct_date_request = json_helper.JsonRequestSingle(config.TWEET_DICTIONARY_DATE_TIME_KEY,
                                             config.TWEET_JSON_DATE_TIME_LOCATION)
        self.correct_text_request = json_helper\
        .JsonRequestSingle(config.TWEET_DICTIONARY_TEXT_KEY, config.TWEET_JSON_TEXT_LOCATION)
        self.correct_hashtags_request = json_helper\
        .JsonRequestList(config.TWEET_DICTIONARY_HASHTAGS_KEY, config.TWEET_JSON_HASHTAGS_LOCATION,
                         require_lower_case=True, require_ascii_format=True,
                         require_unique_elements=True)

        self.too_long_json_field_chain = ["entities", "hashtags", "text", "text"]
        self.mispelled_json_field_chain = ["entities", "hashtags", "rext"]

    def test_parse_json_correctly(self):
        self.assertEqual("sample text", json_helper.nested_json_fields_value(self.correct_json,
                                                                             config.TWEET_JSON_TEXT_LOCATION))
        self.assertEqual("Thu Oct 29 17:51:50 +0000 2015",
                         json_helper.nested_json_fields_value(self.correct_json, config.TWEET_JSON_DATE_TIME_LOCATION))
        self.assertEqual(["hashtag1", "hashtag2"],
                         json_helper.nested_json_fields_value(self.correct_json, config.TWEET_JSON_HASHTAGS_LOCATION))

    def test_wrong_json_raises_error(self):
        self.assertRaises(ValueError, json_helper.nested_json_fields_value, self.incorrect_json,
                                                                             config.TWEET_JSON_TEXT_LOCATION)
        self.assertRaises(ValueError, json_helper.nested_json_fields_value, self.incorrect_json,
                                                                           config.TWEET_JSON_DATE_TIME_LOCATION)
        self.assertRaises(ValueError, json_helper.nested_json_fields_value, self.incorrect_json,
                                                                           config.TWEET_JSON_HASHTAGS_LOCATION)

    def test_wrong_json_field_chain_raises_error(self):
        self.assertRaises(ValueError, json_helper.nested_json_fields_value, self.correct_json,
                          self.too_long_json_field_chain)
        self.assertRaises(ValueError, json_helper.nested_json_fields_value, self.correct_json,
                          self.mispelled_json_field_chain)

class TestFormatterMethods(unittest.TestCase):
    def setUp(self):
        self.case_string = "AbCdE"
        self.unicode_string = u"I'm at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa"
        self.make_lower_request = json_helper.JsonRequestSingle("dummy", "dummy", require_lower_case=True)
        self.make_ascii_request = json_helper.JsonRequestSingle("dummy", "dummy", require_ascii_format=True)
        self.make_lower_and_ascii_request = json_helper.JsonRequestSingle("dummy", "dummy",
                                                            require_lower_case=True, require_ascii_format=True)

        self.list_case_strings = ["AbCdE", "abcde"]
        self.list_unicode_strings = [u"I'm at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa",
                                     u"I'm at Terminal de Integra\u00e2\u00f4o do Varadouro in Jo\u00b6o Pessoa"]
        self.list_case_and_unicode_strings = \
            [u"i'm at terMinAl De Integra\u00e7\u00e3o do varAdouro in Jo\u00e3o pEssoa",
             u"I'm at Terminal de Integra\u00e2\u00f4o do Varadouro in Jo\u00b6o Pessoa"]
        self.list_unicode_only_strings = ["", u"\u00e7\u00e3\u00c3\u00d2"]
        self.list_make_lower_and_unique = json_helper.JsonRequestList("dummy", "dummy",
                                                require_lower_case=True, require_unique_elements=True)
        self.list_make_ascii_and_unique = json_helper.JsonRequestList("dummy", "dummy",
                                                require_ascii_format=True, require_unique_elements=True)
        self.list_make_ascii_and_lower_and_unique = json_helper.JsonRequestList("dummy", "dummy",
                                    require_lower_case=True, require_ascii_format=True, require_unique_elements=True)

    def test_single_request_format(self):
        self.assertEqual("abcde", json_helper.format_value(self.case_string, self.make_lower_request))
        self.assertEqual("I'm at Terminal de Integrao do Varadouro in Joo Pessoa",
                         json_helper.format_value(self.unicode_string, self.make_ascii_request))
        self.assertEqual("i'm at terminal de integrao do varadouro in joo pessoa",
                         json_helper.format_value(self.unicode_string, self.make_lower_and_ascii_request))

    def test_list_request_format(self):
        # so need to test unique with ascii, case, and... empty.
        self.assertEqual(["abcde"], json_helper.format_value(self.list_case_strings, self.list_make_lower_and_unique))
        self.assertEqual(["I'm at Terminal de Integrao do Varadouro in Joo Pessoa"],
                         json_helper.format_value(self.list_unicode_strings, self.list_make_ascii_and_unique))
        self.assertEqual(["i'm at terminal de integrao do varadouro in joo pessoa"],
                         json_helper.format_value(self.list_case_and_unicode_strings,
                         self.list_make_ascii_and_lower_and_unique))
        self.assertEqual([""], json_helper.format_value(self.list_unicode_only_strings,
                                                        self.list_make_ascii_and_unique))


class TweetsCleanedMethods(unittest.TestCase):
    def setUp(self):
        self.whitespace_escape_chars_string = "lots\n of\r\n whitespace\n\n escape\t\n\r chars\b\b\r here\v\r\r\n"

    def test_whitespace_escape(self):
        self.assertEqual("lots  of  whitespace   escape    chars    here   ",
                         tweets_cleaned.remove_whitespace_escapes(self.whitespace_escape_chars_string))


class GraphMethods(unittest.TestCase):
    def setUp(self):
        # what to test? test the number of edges/nodes are consistent after adding/removing. okay...
        self.graph = networkx.Graph()

    def test_edge_arithmetic(self):
        # don't really have to test weight, since that should be accounted for
        average_degree.increment_edge(1, 2, self.graph)
        self.num_edge_and_nodes_assert(2, 1, self.graph)
        average_degree.increment_edge(2, 3, self.graph)
        self.num_edge_and_nodes_assert(3, 2, self.graph)
        average_degree.increment_edge(4, 5, self.graph)
        self.num_edge_and_nodes_assert(5, 3, self.graph)

        #increment edge but not node
        average_degree.increment_edge(1, 4, self.graph)
        self.num_edge_and_nodes_assert(5, 4, self.graph)

        # this checks that incrementing an already existing edge doesn't do anything
        average_degree.increment_edge(1, 2, self.graph)
        self.num_edge_and_nodes_assert(5, 4, self.graph)

        # this checks decrementing weight > 1 edge doesn't remove anything
        average_degree.decrement_edge(1, 2, self.graph)
        self.num_edge_and_nodes_assert(5, 4, self.graph)

        # this checks decrementing weight = 1 DOES remove something
        average_degree.decrement_edge(2, 3, self.graph)
        self.num_edge_and_nodes_assert(4, 3, self.graph)

        # remove edge but not node
        average_degree.decrement_edge(1, 4, self.graph)
        self.num_edge_and_nodes_assert(4, 2, self.graph)

        #remove two nodes and one edge
        average_degree.decrement_edge(4, 5, self.graph)
        self.num_edge_and_nodes_assert(2, 1, self.graph)


    def test_edge_errors(self):
        average_degree.increment_edge(1, 2, self.graph)
        # the following should fail, but also shouldn't raise an exception, since I want it to be handled
        # and not cause errors.
        try:
            average_degree.decrement_edge(1, 3, self.graph)
        except Exception:
            self.fail("Received an expcetion when trying to decement non existing edge.")

        self.num_edge_and_nodes_assert(2, 1, self.graph)
        self.assertEqual([1, 2], self.graph.nodes())
        self.assertEqual([(1, 2)], self.graph.edges())

    def num_edge_and_nodes_assert(self, num_nodes, num_edges, graph):
        self.assertEqual(num_nodes, graph.number_of_nodes())
        self.assertEqual(num_edges, graph.number_of_edges())


class GraphIntegration(unittest.TestCase):
    def setUp(self):
        # so make some tweets, and then test with update.
        tweet1 = self.make_tweet("Thu Oct 29 17:51:50 +0000 2015", ["a"])
        tweet2 = self.make_tweet("Thu Oct 29 17:51:50 +0000 2015", ["b", ""])

        # then assert edges and nodes and deque length. 



    def make_tweet(self, created_at, hashtags):
        tweet_dict = {}
        tweet_dict['created_at'] = created_at
        tweet_dict['hashtags'] = hashtags
        return tweet_dict






if __name__ == '__main__':
    unittest.main()