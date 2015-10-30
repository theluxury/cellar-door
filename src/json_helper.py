import json

JSON_TEXT_CONST = "text"
JSON_CREATED_AT_CONST = "created_at"

def parse_tweets__text_and_created_at_time(file):
    tweet_file = open(file)
    tweets = []
    for line in tweet_file:
        tweet_json = json.loads(line)
        if JSON_TEXT_CONST not in tweet_json or JSON_CREATED_AT_CONST not in tweet_json:
            continue

        # since we only need these two fields, only save these two to save space.
        tweet = {JSON_TEXT_CONST: tweet_json[JSON_TEXT_CONST],
                 JSON_CREATED_AT_CONST: tweet_json[JSON_CREATED_AT_CONST]}
        tweets.append(tweet)

    tweet_file.close()
    return tweets