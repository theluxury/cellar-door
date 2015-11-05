Mark Wang's Entry for Insight Data Engineering - Coding Challenge
===========================================================
 

## Requirements

* [Networkx](https://networkx.github.io/)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

Both are included in requirements.txt. Simply run pip install -r requirements.txt to install them. 

## Assumptions for Feature One

1. Tweets with empty text after unicode has been removed will still be printed in \<text> (date) format with empty text.

2. The full list of escapes that are replaced with one whitespace are
  * \r\n
  * \n
  * \r
  * \t
  * \v
  * \b
Note that performance can be slightly improved by trimming this list, as none of the example tweets actually had \t \v or \b on them. However, they were added to the replace list for completness. 

3. An empty line has been added after the tweets and before the unicode count for styling as in the example in the output.

## Assumptions for Feature Two

1. Hashtag text that is empty after removing the unicode is ignored and not made into a node.

2. The 60 seconds window given is inclusive (tweets must be older than 60 seconds from the new tweet to be evicted as opposed to older than or equal to 60 seconds from the new tweet).

3. In tweets.txt, there were lines of JSON that indicated the API was at it's limit for tweets being read. These are ignored even though they have a timestamp.

4. All tweets (even those without any hashtags) have the ability to evict old tweets. 

5. The tweet inputs will be sorted chronologically, as stated in the FAQ. If for whatever reason they are not, my code will work if line 18 in average_degree.py is uncommented and tweets in line 19 is replace with sorted_tweets. 

Please send any comments or questions to Mark Wang at zhengkaw@gmail.com