from pymongo import Connection
# The MongoDB connection info. This assumes your database name is TwitterStream, and your collection name is tweets.
connection = Connection('localhost', 27017)
db = connection.nearish
keywords = db.place.distinct( "name" )
print len(keywords)
for key in keywords:
    print key
    results = db.tweets.find({"text": {'$regex' : '.* ' + key + ' .*'}})
    print list(results)
    for result in results:
        db.twitter.insert(result)
