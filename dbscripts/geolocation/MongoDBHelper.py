from pymongo import *


class MongoDBHelper:



	KEY_GEOMETRY = "geometry"
	KEY_LOCATION = "location"
	KEY_LATITUDE = "lat"
	KEY_LONGITUDE = "lng"
	KEY_PHOTOS = "photos"
	KEY_PHOTO_REFERENCE = "photo_reference"

	KEY_NAME = "name"
	KEY_PLACE_ID = "place_id"
	KEY_RATING = "rating"

	KEY_OPENING_HOURS = "opening_hours"

	KEY_TYPES = "types"
	KEY_VICINITY = "vicinity"


	collection_places = "places"
	collection_comments = "comments"

	def __init__(self):
		self.db_name = 'nearish'
		self.db_host = '127.0.0.1'
		self.db_port = 27017
		self.db_user = 'isisnaomi'
		self.db_password = ''
		self.KEY_GEOMETRY = "geometry"
		self.KEY_LOCATION = "location"
		self.KEY_LATITUDE = "lat"
		self.KEY_LONGITUDE = "lng"
		self.KEY_PHOTOS = "photos"
		self.KEY_PHOTO_REFERENCE = "photo_reference"

		self.KEY_NAME = "name"
		self.KEY_PLACE_ID = "place_id"
		self.KEY_RATING = "rating"

		self.KEY_OPENING_HOURS = "opening_hours"

		self.KEY_TYPES = "types"
		self.KEY_VICINITY = "vicinity"


		self.collection_places = "places"
		self.collection_comments = "comments"
		


	def connection(self):
		db = None
		try:
			client = MongoClient(self.db_host, self.db_port)
			db = client[str(self.db_name)]
		except Exception as exception:
			print (exception)
		return db

	def addPlace(self, data):
		try:

			if(self.ifexists(data.getplaceid()) == False):
				dict_data = { '_id' : data.getplaceid() ,self.KEY_NAME : data.getname(), self.KEY_PHOTO_REFERENCE : data.getphoto(), self.KEY_TYPES : data.gettypes(), self.KEY_OPENING_HOURS : data.getopeninghours(), self.KEY_LATITUDE : data.getlatitude(), self.KEY_LONGITUDE : data.getlongitude(), self.KEY_RATING : data.getrating(), self.KEY_VICINITY : data.getvicinity(), "loc":{ 'type' : 'Point', 'coordinates' : [float(data.getlongitude()), float(data.getlatitude())]}}
				db = self.connection()
				db['places'].insert_one(dict_data)
				print('\nInserted data successfully\n')
			else:
				print('\nElement exists in collection\n')

		except Exception as e:
			print(e)


	def ifexists(self,placeid):

		try:
			db = self.connection()
			if db['places'].find({'_id' : placeid}).count() > 0:
				return True
			else:
				return False
		except Exception as e:
			print(e)
