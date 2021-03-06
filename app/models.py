from app import db

class User(db.Document):
	name = db.StringField()
	phone = db.StringField()
	password = db.StringField()
	blood_group = db.StringField()
	blood_donate = db.BoolField()
	address = db.StringField()
	issues = db.StringField(required=False)
	emergency_contacts = db.ListField(db.StringField(),required=False)
	aadhar = db.StringField(required=False)
	location = db.DictField(db.StringField(),required=False)
	friends = db.ListField(db.StringField(),required=False)

	def create(self,obj):
		self.name = obj["name"]
		self.phone = obj["phone"]
		self.password = obj["password"]
		self.blood_group = obj["blood_group"]
		self.blood_donate = False
		self.address = obj["address"]
		self.emergency_contacts = list()
		self.friends = list()
		self.location = { "lat": "0", "log": "0"}
		self.issues = ""
		self.aadhar = ""
		# self.aadhar = obj["aadhar"]
		# self.location = obj["location"]
		# self.friends = obj["friends"]

	def toJSON(self):
		json = dict()
		json['name'] = self.name
		json['phone'] = self.phone
		json['blood_group'] = self.blood_group
		json['blood_donate'] = self.blood_donate
		json['address'] = self.address
		json['issues'] = self.issues
		json['aadhar'] = self.aadhar
		return json


class Hospital(db.Document):
	name = db.StringField()
	email = db.StringField()
	password = db.StringField()
	address = db.StringField()
	location = db.DictField(db.StringField())
	blood_units = db.DictField(db.FloatField())

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.email

	def create(self,obj):
		self.name = obj["name"]
		self.email = obj["email"]
		self.password = obj["password"]
		self.blood_units = obj["blood_units"]
		self.address = obj["address"]
		self.location = obj["location"]


class Ambulance(db.Document):
	name = db.StringField()
	agency = db.StringField()
	phone = db.StringField()
	status = db.StringField(required=False)
	password = db.StringField()
	location = db.DictField(db.StringField())

	def create(self,obj):
		self.name = obj["name"]
		self.agency = obj["agency"]
		self.password = obj["password"]
		self.phone = obj["phone"]
		self.location = { "lat": "0", "log": "0"}
		# self.status = obj["status"]
		# self.location = obj["location"]


class Case(db.Document):
	patient_name = db.StringField()
	ambulance_driver = db.StringField()
	patient_id = db.StringField()
	driver_id = db.StringField()
	hospital = db.StringField()
	report = db.StringField(required=False)
	issues = db.StringField()
	problem = db.StringField()
	status = db.BoolField(required=False)
	active = db.BoolField()

	def create(self,obj):
		self.patient_name = obj["patient_name"]	
		self.ambulance_driver = obj["ambulance_driver"]	
		self.hospital = obj["hospital"]	
		self.problem = obj["problem"]
		self.issues = obj["issues"]
		self.patient_id = obj["patient_id"]
		self.driver_id = obj["driver_id"]	
		self.active = True
		# report = obj["report"]		
