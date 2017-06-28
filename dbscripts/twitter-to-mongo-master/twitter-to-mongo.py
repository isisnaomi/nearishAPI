# ===============================================
# twitter-to-mongo.py v1.0 Created by Sam Delgado
# ===============================================
from pymongo import Connection
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime

# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
connection = Connection('localhost', 27017)
db = connection.nearish
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets

# Add the keywords you want to track. They can be cashtags, hashtags, or words.


places = db.place.find().skip(0).limit(10).distinct( "name" )
keywords = places[:len(places)/2]
print keywords

# Optional - Only grab tweets of specific language
language = ['es']

# You need to replace these with your own values that you get after creating an app on Twitter's developer portal.
consumer_key = "knG07Vm589enLm9HYWG2VRW7k"
consumer_secret = "x2ouDJr64iavCY4nQ0poYdKNSdrrgdeV7zuQAhJvMWgvd78OxM"
access_token = "36515835-MN7aTa1VxKxZWZXiZ2WR7hryx9nczfBGpYvGnE5Xq"
access_token_secret = "rSO6CcCgPs6WjZ5iq7HgfUmdlxkYhkfoDUQRcn2dDRRDS"

# The below code will get Tweets from the stream and store only the important fields to your database
class StdOutListener(StreamListener):

    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        username = t['user']['screen_name']  # The username of the Tweet author
        text = t['text']  # The entire body of the Tweet
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        dt = t['created_at']  # The timestamp of when the Tweet was created

        # Convert the timestamp string given by Twitter to a date object called "created". This is more easily manipulated in MongoDB.
        created = datetime.datetime.strptime(dt, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id':tweet_id, 'username':username,'text':text, 'hashtags':hashtags}

        # Save the refined Tweet data to MongoDB
        collection.save(tweet)

        # Optional - Print the username and text of each Tweet to your console in realtime as they are pulled from the stream
        print username + ':' + ' ' + text
        return True

    # Prints the reason for an error to your console
    def on_error(self, status):
        print status

# Some Tweepy code that can be left alone. It pulls from variables at the top of the script
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=keywords, languages=language)
