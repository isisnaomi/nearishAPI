import requests
import json
from Place import Place
from MongoDBHelper import MongoDBHelper

API_KEY = 'AIzaSyAD0mAUNtwC7ihAullxyv6n6zAKPnBgybA'
RADIUS = 500

latitude = 21.021258
longitude = -89.678835

limit_longitude_right = -89.566754

increment_longitude = .007966
count = 0


def add_place(data):
    global count

    dao_db = MongoDBHelper()

    results = data['results']

    for item in range(0, len(results)):
        count = count +1
        print(len(results))
        data = Place()

        if MongoDBHelper.KEY_PLACE_ID in results[item]:
            data.setplaceid(str(count))

            if MongoDBHelper.KEY_NAME in results[item]:
                data.setname(results[item][MongoDBHelper.KEY_NAME])

            if MongoDBHelper.KEY_PHOTOS in results[item]:
                if MongoDBHelper.KEY_PHOTO_REFERENCE in results[item][MongoDBHelper.KEY_PHOTOS][0]:
                    data.setphoto(str(results[item][MongoDBHelper.KEY_PHOTOS][0][MongoDBHelper.KEY_PHOTO_REFERENCE]))

            if MongoDBHelper.KEY_TYPES in results[item]:
                data.settypes(','.join(str(element) for element in results[item][MongoDBHelper.KEY_TYPES]))

            if MongoDBHelper.KEY_OPENING_HOURS in results[item]:
                data.setopeninghours(','.join(
                    str(element) for element in results[item][MongoDBHelper.KEY_OPENING_HOURS]['weekday_text']))

            if MongoDBHelper.KEY_RATING in results[item]:
                data.setrating(str(results[item][MongoDBHelper.KEY_RATING]))

            if MongoDBHelper.KEY_GEOMETRY in results[item]:
                if MongoDBHelper.KEY_LOCATION in results[item][MongoDBHelper.KEY_GEOMETRY]:
                    data.setlatitude(str(results[item][MongoDBHelper.KEY_GEOMETRY][MongoDBHelper.KEY_LOCATION][
                                             MongoDBHelper.KEY_LATITUDE]))
                    data.setlongitude(str(results[item][MongoDBHelper.KEY_GEOMETRY][MongoDBHelper.KEY_LOCATION][
                                              MongoDBHelper.KEY_LONGITUDE]))

            if MongoDBHelper.KEY_VICINITY in results[item]:
                data.setvicinity(results[item][MongoDBHelper.KEY_VICINITY])

            print(data)
            dao_db.addPlace(data)


types = [
    "restaurant", "bakery", "bar", "cafe", "casino", "convenience_store"
    , "meal_delivery", "meal_takeaway", "night_club"
    , "shopping_mall", "store"]


for type_item in types:
    latitude = 21.021258
    longitude = -89.678835

    while longitude < limit_longitude_right:
		#print (latitude)
		url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(latitude) + ',' + str(longitude) + '&radius=' + str(RADIUS) + '&type=' + str(type_item) + '&key=' + str(API_KEY)
		#print(url)
		response = requests.get(url)
		status = response.status_code
		#print(response.headers['content-type'])
		if int(status) == 200:
			data = response.content.decode('utf-8')


			data = json.loads(data)
			if (data['status'] == 'OK'):
				add_place(data)

		longitude = float("{0:.6f}".format(longitude + increment_longitude))
