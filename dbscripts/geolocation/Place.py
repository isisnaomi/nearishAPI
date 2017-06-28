

class Place:

	def __init__(self):
		self.place_id = None
		self.name = None
		self.photo = None
		self.types = None
		self.opening_hours = None
		self.latitude = None
		self.longitude = None
		self.rating = None
		self.vicinity = None

	def setplaceid(self, value):
		self.place_id = value

	def setname(self, value):
		self.name = 'Not defined' if value is None or len(value) < 1 else value

	def setphoto(self, value):
		self.photo = 'Not defined' if value is None or len(value) < 1 else value

	def settypes(self, value):
		self.types = 'Not defined' if value is None or len(value) < 1 else value

	def setopeninghours(self, value):
		self.opening_hours = 'Not defined' if value is None or len(value) < 1 else value

	def setlatitude(self, value):
		self.latitude = 'Not defined' if value is None or len(value) < 1 else value

	def setlongitude(self, value):
		self.longitude = 'Not defined' if value is None or len(value) < 1 else value

	def setrating(self, value):
		self.rating = 'Not defined' if value is None or len(value) < 1 else value

	def setvicinity(self, value):
		self.vicinity = 'Not defined' if value is None or len(value) < 1 else value


	def getplaceid(self):
		return self.place_id 

	def getname(self):
		return self.name 

	def getphoto(self):
		return self.photo 

	def gettypes(self):
		return self.types 

	def getopeninghours(self):
		return self.opening_hours 

	def getlatitude(self):
		return self.latitude 

	def getlongitude(self):
		return self.longitude 

	def getrating(self):
		return self.rating 

	def getvicinity(self):
		return self.vicinity 
