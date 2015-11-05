Mark Wang's Entry for Insight Data Engineering - Coding Challenge
===========================================================
 

## Requirements

* [Networkx](https://networkx.github.io/)
* [python-dateutil](https://pypi.python.org/pypi/python-dateutil)

Both are included in requirements.txt. Simply run pip install -r requirements.txt to install them. 

## Assumptions for Feature One

1. Tweets with empty text after unicode has been removed will still be printed in \<text> (date) format with empty test.

2. The full list of escapes that are replaced with one whitespace are
  * \r\n
  * \n
  * \r
  * \t
  * \v
  * \b
3. An empty line has been added after the tweets and before the unicode count for styling as in the example in the output.

## Assumptions for Feature Two

1. Hashtag text that is empty after removing the unicode is not accounted for for node. 
2. The 60 seconds window given is inclusive (tweets must be older than 60 seconds from the new tweet to be evicted as opposed to older than or equal to 60 seconds from the new tweet).
3. Limit JSON lines that were included in the example tweets.txt are ignored even though they have a timestamp.
4. All tweets (even those without any hashtags) have the ability to evict old tweets. 