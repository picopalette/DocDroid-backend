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
	location = db.DictField(db.FloatField(),required=False)
	friends = db.ListField(db.StringField(),required=False)

	def create(self,obj):
		self.name = obj["name"]
		self.phone = obj["phone"]
		self.password = obj["password"]
		self.blood_group = obj["blood_group"]
		self.blood_donate = False
		self.address = obj["address"]
		# self.issues = obj["issues"]
		# self.emergency_contacts = obj["emergency_contacts"]
		# self.aadhar = obj["aadhar"]
		# self.location = obj["location"]
		# self.friends = obj["friends"]

class Hospital(db.Document):
	name = db.StringField()
	email = db.StringField()
	password = db.StringField()
	address = db.StringField()
	location = db.ListField(db.FloatField())
	blood_units = db.DictField(db.IntField(),required=False)


	def create(self,obj):
		self.name = obj["name"]
		self.email = obj["email"]
		self.password = obj["password"]
		# blood_units = obj["blood_units"]
		self.address = obj["address"]
		self.location = obj["location"]


class Ambulance(db.Document):
	name = db.StringField()
	agency = db.StringField()
	phone = db.StringField()
	status = db.StringField(required=False)
	password = db.StringField()
	location = db.DictField(db.FloatField(), required=False)

	def create(self,obj):
		self.name = obj["name"]
		self.agency = obj["agency"]
		self.password = obj["password"]
		self.phone = obj["phone"]
		# self.status = obj["status"]
		# self.location = obj["location"]


class Case(db.Document):
	patient_name = db.DocumentField(User)
	ambulance_driver = db.DocumentField(Ambulance,required=False)
	hospital = db.DocumentField(Hospital)
	report = db.StringField(required=False)

	def create(self,obj):
		self.patient_name = obj["patient_name"]	
		# ambulance_driver = obj["ambulance_driver"]	
		self.hospital = obj["hospital"]	
		# report = obj["report"]		


class CaseHistory(db.Document):
	patient_name = db.DocumentField(User)
	ambulance_driver = db.DocumentField(Ambulance,required=False)
	hospital = db.DocumentField(Hospital)
	report = db.StringField(required=False)

	def create(self,obj):
		self.patient_name = obj["patient_name"]	
		# ambulance_driver = obj["ambulance_driver"]	
		self.hospital = obj["hospital"]	
		# report = obj["report"]
