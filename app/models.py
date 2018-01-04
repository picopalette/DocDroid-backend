from app import db

class User(db.Document):
	name = db.StringField()
	phone = db.StringField()
	password = db.StringField()
	blood_group = db.StringField()
	address = db.StringField()
	issues = db.StringField()
	emergency_contacts = db.ListField(db.StringField())
	aadhar = db.StringField()
	location = db.DictField(db.FloatField())
	friends = db.ListField(db.StringField())

	def __init__(self,obj):
		name = obj["name"]
		phone = obj["phone"]
		password = obj["password"]
		blood_group = obj["blood_group"]
		address = obj["address"]
		issues = obj["issues"]
		emergency_contacts = obj["emergency_contacts"]
		aadhar = obj["aadhar"]
		location = obj["location"]
		friends = obj["friends"]

class Hospital(db.Document):
	name = db.StringField()
	email = db.StringField()
	password = db.StringField()
	address = db.StringField()
	location = db.ListField(db.FloatField())
	blood_units = db.DictField(db.IntField())


	def __init__(self,obj):
		name = obj["name"]
		email = obj["email"]
		password = obj["password"]
		blood_units = obj["blood_units"]
		address = obj["address"]
		location = obj["location"]


class Ambulance(db.Document):
	name = db.StringField()
	agency = db.StringField()
	phone = db.StringField()
	status = db.StringField()
	password = db.StringField()
	location = db.DictField(db.FloatField())

	def __init__(self,obj):
		name = obj["name"]
		agency = obj["agency"]
		password = obj["password"]
		phone = obj["phone"]
		status = obj["status"]
		location = obj["location"]


class Case(db.Document):
	patient_name = db.DocumentField(User)
	ambulance_driver = db.DocumentField(Ambulance)
	hospital = db.DocumentField(Hospital)
	report = db.StringField()

	def __init__(self,obj):
		patient_name = obj["patient_name"]	
		ambulance_driver = obj["ambulance_driver"]	
		hospital = obj["hospital"]	
		report = obj["report"]		


class CaseHistory(db.Document):
	patient_name = db.DocumentField(User)
	ambulance_driver = db.DocumentField(Ambulance)
	hospital = db.DocumentField(Hospital)
	report = db.StringField()

	def __init__(self,obj):
		patient_name = obj["patient_name"]	
		ambulance_driver = obj["ambulance_driver"]	
		hospital = obj["hospital"]	
		report = obj["report"]
