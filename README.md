Mark Wang's Entry for Insight Data Engineering - Coding Challenge
===========================================================
 

## Requirements

* [Networkx](https://networkx.github.io/)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

Both are included in requirements.txt. Simply run pip install -r requirements.txt to install them. 


## Assumptions for Feature One

1. Tweets with empty text after unicode has been removed will still be printed in \<text> (date) format with empty text.

2. The full list of escapes that are replaced with one whitespace are as follows. 
  * \r\n
  * \n
  * \r
  * \t
  * \v
  * \b

  Note that performance can be slightly improved by trimming this list, as none of the example tweets actually had \t \v or \b in them. However, they were added to the list for completeness. 

3. An empty line has been added after the tweets and before the unicode count for styling as in the example in the output.


## Assumptions for Feature Two

1. All hashtags with empty text after removing the unicode is considered the same node.

2. The 60 seconds window given is exclusive (tweets that are older than or equal to 60 seconds from the new tweet are evicted).

3. If the graph contains no edges and no nodes, then the output with be 0.00.

4. The tweet inputs will be sorted chronologically, as stated in the FAQ. If for whatever reason they are not, my code will work if line 18 in average_degree.py is uncommented and tweets in line 19 is replace with sorted_tweets. 


## Error Handling

There are two noteworthy possible sources of error.

1. JSON Parsing Errors

   JSON lines that cannot be parsed are skipped and logged into ./log/log.txt and the program continues to run as normal. This is in response to the various limit JSON lines that were in the example tweets.txt. Though the test input won't have such lines, it seems like it would be best practice to leave in this error handling for future use.

2. Graph Edge/Node Removal Errors

   The program will crash if it attempts to remove an edge that is non-existent. This is the intended behavior, as this error means that the graph data is corrupt and any future rolling average calculation will be inaccurate. This error should not happen in general, but is something to be aware of.

For both of these errors, a message will be written into ./log/log.txt for debugging. 


## Tests

A suite of unit and e2e tests have been included. Note that the inputs for these tests are not real tweets in the sense they only contain keys necessary for our tests. This was done for easier readability as real tweet json is hard to read. Unit tests inputs are coded directly in ./src/unit_test.py while e2e_test.py inputs are in ./test_files. This was done to to better replcate fact the real program reads from a .txt file.


### Unit Tests

Currently covers the following:

1. JSON parsing and error handling.

2. Formatting the parsed values. This includes
  * Making hashtags lower case
  * Removing unicode
  * Replacing escapes.
  * Removing duplicate hashtags from tweets (includes hashtags that become identical after removing unicode).

3. Graph and deque arithmetic to ensure edge, node, and deque counts are consistent with requirements.


### E2E Tests

Contains two e2e tests, one for each feature. The input tweets haven been chosen to try to test for all edge cases that may arise from escapes, unicode, duplicate hashtags, etc. 


### Future To Test

All the tweets were +0000 timezone offset, so behavior with tweets of different offsets in untested. Dateutil should deal with this intelligently, but is definitely something to keep in mind. Also, the current e2e test input file system is not ideal, as it is possible to alter the files without altering the expected output and vice versa, leading to possible future confusion. Look into future solution of writing the input files from the test file itself. 


## Donald Trump

Donald Trump's last name is used frequently for sample hashtags. This is because #Trump appeared in the first tweet from tweets.txt to contain a hashtag and I thought it would be both topical and humorous to keep using it. Note that this does not mean I support him, his party, nor the wall.   


Please send any comments or questions to Mark Wang at zhengkaw@gmail.com