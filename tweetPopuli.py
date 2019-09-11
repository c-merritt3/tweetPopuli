import tweepy 
import secret
import re
from textblob import TextBlob

auth = tweepy.OAuthHandler(secret.consumer_key, secret.consumer_secret) 
auth.set_access_token(secret.access_token, secret.access_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

def tweet_sentiment(tweet):
    '''
    using NLP textblob method, return wether the tweet was considered neg or pos
    '''
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > .20:
        return 'Positive'
    else:
        return 'Negative'

def clean_tweet(tweet):  
    '''
    using regex expressions "clean up" the tweet
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

def getReplies(username, user_tweets):
    responses_to_user = []
    for tweet in user_tweets:
        print(tweet.text)
        replies = tweepy.Cursor(api.search, q='to:{}'.format(username),since_id= tweet.id, result_type = 'mixed', tweet_mode='extended').items()
        while True:
            reply = replies.next()
            responses_to_user.append(tweet_sentiment(clean_tweet(reply.full_text)))
            if len(responses_to_user) > 100:
                break;
    return responses_to_user

def pos_neg_sort(replies_to_user, name):
    ptweets = []
    ntweets = []
    for tweets in replies_to_user:
        if tweets == "Positive":
            ptweets.append(tweets)
        elif tweets == "Negative":
            ntweets.append(tweets)
    
    print("{} pos tweet percentage : {} %".format(name, 100*len(ptweets)/len(replies_to_user)))
    print("{}neg tweet percentage : {} % \n".format(name, 100*len(ntweets)/len(replies_to_user)))
    
def get_tweets_for_user(user_screen_name):
    screen_name_tweets = []
    screen_name_tweets = api.user_timeline(screen_name = user_screen_name, count = 1, include_rts = False)
    return screen_name_tweets

politician_list = ["realDonaldTrump", "AOC","JoeBiden", "SenWarren","BorisJohnson"]
for politician in politician_list:
    politician_tweets = get_tweets_for_user(politician)
    replies_to_politcian = getReplies(politician, politician_tweets)
    pos_neg_sort(replies_to_politcian,politician)




