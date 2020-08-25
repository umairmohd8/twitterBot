import logging
import tweepy
import random
import time

logging.basicConfig(level=logging.INFO, filename="requests.log",
                    format='%(asctime)s -  %(levelname)s -  %(message)s')
logging.getLogger("tweepy").setLevel(logging.DEBUG)
logging.disable(logging.DEBUG)

#use the twitter api keys here,by removing hashtags

#CONSUMER_KEY = 
#CONSUMER_SECRET = 
#ACCESS_KEY = 
#ACCESS_SECRET = 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE_NAME = 'last_seen.txt'


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def getquote():
    file1 = open('sw_quotes.txt', encoding='utf8')
    Lines1 = file1.readlines()
    return random.choice(Lines1)


def getswear():
    file2 = open('shakespeare_sw.txt', encoding='utf8')
    Lines2 = file2.readlines()
    return random.choice(Lines2)


def reply_to_tweets():
    logging.info('retrieving and replying to tweets...')
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')
    for mention in reversed(mentions):
        logging.info('@' + mention.user.screen_name + " " + str(mention.id)
                     + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#quoteme' in mention.full_text.lower():
            logging.info('found #quoteme!')
            logging.info('responding a quote\n')
            quote = getquote()
            api.update_status('@' + mention.user.screen_name +
                              quote, mention.id)
            logging.info("quote sent successfully\n")
        elif '#swearme' in mention.full_text.lower():
            logging.info('found #swearme!')
            logging.info('responding a Shakespeare insult\n')
            swear = getswear()
            api.update_status('@' + mention.user.screen_name +
                              swear, mention.id)
            logging.info("sent successfully\n")


while True:
    reply_to_tweets()
    time.sleep(10)
