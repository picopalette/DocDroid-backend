from app import app,models,lm
from ml import geotest
import os
from flask_login import LoginManager,login_required,login_user,logout_user
from app import db
from flask_mongoalchemy import MongoAlchemy
from flask import Flask, current_app, jsonify, flash, render_template, json, request, redirect, session, url_for
from werkzeug import generate_password_hash, check_password_hash

# Login and Registration 

@app.route('/api/')
def apimain():
    return "Hello New World"

@app.route('/api/signUpUser',methods = ['POST','GET'])
def signUpUser():
	content = request.get_json()
	obj = models.User()
	obj.create(content)
	obj.save()
	response = jsonify(content)
	response.set_cookie('user_id',value=obj.phone)
	return response


@app.route('/api/signUpDriver',methods = ['POST','GET'])
def signUpDriver():
	content = request.get_json()
	obj = models.Ambulance()
	obj.create(content)
	obj.save()
	response = jsonify(content)
	response.set_cookie('driver_id',value=obj.phone)
	return response


@app.route('/api/loginUser',methods = ['POST','GET'])
def loginUser():
	content = request.get_json()
	obj = models.User.query.filter(models.User.phone == content["phone"],models.User.password == content["password"]).first()
	if obj is not None:
		response = current_app.response_class(
			response = json.dumps(content),
			status=200,
			mimetype="application/json"
		);	
		response.set_cookie('user_id',value=obj.phone)
	else:
		response = current_app.response_class(
			response = json.dumps(content),
			status=401,
			mimetype="application/json"
		);	
	return response
	

@app.route('/api/loginDriver',methods = ['POST','GET'])
def loginDriver():
	content = request.get_json()
	obj = models.Ambulance.query.filter(models.Ambulance.phone == content["phone"],models.Ambulance.password == content["password"]).first()
	if obj is not None:
		response = current_app.response_class(
			response = json.dumps(content),
			status=200,
			mimetype="application/json"
		)
		response.set_cookie('driver_id',value=obj.phone)
	else:
		response = current_app.response_class(
			response = json.dumps(content),	
			status=401,
			mimetype="application/json"
		)
	return response

@app.route('/api/updateUserProfile', methods= ['POST'])
def updateUserProfile():
	content = request.get_json()
	body = dict()
	if 'user_id' not in request.cookies:
		body['error'] = 'Not Authorized'
		response = current_app.response_class(
			response = json.dumps(body),	
			status=401,
			mimetype="application/json"
		)
		return response
	obj = models.User.query.filter(models.User.phone == request.cookies['user_id']).first()
	print(obj)
	obj.blood_donate = content['blood_donate']
	obj.issues = content["issues"]
	obj.aadhar = content["aadhar"]
	obj.save()
	body['saved'] = 'success'
	return jsonify(body)

@app.route('/api/getEmergencyContacts', methods=['GET'])
def getEmergencyContacts():
	if 'user_id' not in request.cookies:
		body = dict()
		body['error'] = 'Not Authorized'
		response = current_app.response_class(
			response = json.dumps(body),	
			status=401,
			mimetype="application/json"
		)
		return response
	obj = models.User.query.filter(models.User.phone == request.cookies['user_id']).first()
	return jsonify(obj.emergency_contacts)

@app.route('/api/updateEmergencyContacts', methods=['POST'])
def updateEmergencyContacts():
	content = request.get_json()
	if 'user_id' not in request.cookies:
		body = dict()
		body['error'] = 'Not Authorized'
		response = current_app.response_class(
			response = json.dumps(body),	
			status=401,
			mimetype="application/json"
		)
		return response
	obj = models.User.query.filter(models.User.phone == request.cookies['user_id']).first()
	obj.emergency_contacts = content[:]
	obj.save()
	for num in content:
		friend = models.User.query.filter(models.User.phone == num).first()
		if friend:
			friend.friends.append(obj.phone)
			friend.save()
	return jsonify(obj.emergency_contacts)

@app.route('/api/getUserProfile', methods=['GET'])
def getUserProfile():
	body = dict()
	body['error'] = 'Not Authorized'
	response = current_app.response_class(
	response = json.dumps(body),	
	status=401,
	mimetype="application/json"
	)
	if 'user_id' not in request.cookies:
		return response
	obj = models.User.query.filter(models.User.phone == request.cookies['user_id']).first()
	if obj is None:
		response.set_cookie('user_id', value='', expires=0)
		return response
	return jsonify(obj.toJSON())


@app.route('/api/sos', methods=['POST'])
def sos():
	content = request.get_json()
	if 'user_id' in request.cookies:
			obj = models.User.query.filter(models.User.phone == request.cookies['user_id']).first()
			locdict = { 'lat': content['lat'], 'log': content['log']}
			obj.location = locdict
			obj.save()
			userloc = str(content["lat"]) + "," + str(content["log"])
			bestHospital = geotest.predictHospital(userloc)
			#print(bestHospital)
			problem = content['problem']
			hospital = models.Hospital.query.filter(models.Hospital.location == bestHospital).first()
			content['email'] = hospital.email
			aobj = models.Ambulance.query.filter(models.Ambulance.status=="free").all()
			diff = float(aobj[0].location['lat'])-float(bestHospital['lat'])
			diff = diff + float(aobj[0].location['log'])-float(bestHospital['log'])
			mini = diff
			bestDriver = aobj[0]	
			for i in aobj:
				diff = float(i.location['lat'])-float(bestHospital['lat'])
				diff = diff + float(i.location['log'])-float(bestHospital['log'])
				if diff < mini:
					mini = diff
					bestDriver = i

			#bestDriver.status="active"
			#bestDriver.save()


			content = { "patient_name": obj.name,"ambulance_driver": bestDriver.name,"hospital": hospital.name,"problem": problem,"issues": obj.issues, "patient_id":obj.phone,"driver_id":bestDriver.phone }
			caseobj = models.Case()
			caseobj.create(content)
			caseobj.save()

	return jsonify(content)


@app.route('/api/getLocation', methods=['GET'])
def getLocation():
	content = request.args.get('phone')
	obj = models.Ambulance.query.filter(models.Ambulance.phone == content).first()
	if obj is not None:	
		loc = obj.location;
		return jsonify(loc)
	else:
		body = dict()
		body['error'] = 'Not Authorized'
		response = current_app.response_class(
			response = json.dumps(body),	
			status=401,
			mimetype="application/json"
		)
		return response


@app.route('/api/setLocation', methods=['POST'])
def setLocation():
		content = request.get_json()
		obj = models.Ambulance.query.filter(models.Ambulance.phone == content['phone']).first()
		if obj is not None:
			loc = { "lat": content['lat'], "log": content['log']}
			obj.location = loc
			obj.save()
			body = dict()
			body['saved']="success"
			response = current_app.response_class(
				response = json.dumps(body),	
				status=200,
				mimetype="application/json"
			)
			return response
		else:
			body = dict()
			body['error'] = 'Not Authorized'
			response = current_app.response_class(
				response = json.dumps(body),	
				status=401,
				mimetype="application/json"
			)
			return response


@app.route('/api/getLocationUser', methods=['GET'])
def getLocationUser():
	content = request.args.get('phone')
	obj = models.Case.query.filter(models.Case.driver_id == content).first()
	if obj is not None:	
		tempobj = models.User.query.filter(models.User.phone == obj.patient_id).first()
		loc = tempobj.location
		return jsonify(loc)
	else:
		body = dict()
		body['error'] = 'Not Authorized'
		response = current_app.response_class(
			response = json.dumps(body),	
			status=401,
			mimetype="application/json"
		)
		return response


@app.route('/api/setLocationUser', methods=['POST'])
def setLocationUser():
		content = request.get_json()
		obj = models.User.query.filter(models.User.phone == content['phone']).first()
		if obj is not None:
			loc = { "lat": content['lat'], "log": content['log']}
			obj.location = loc
			obj.save()
			body = dict()
			body['saved']="success"
			response = current_app.response_class(
				response = json.dumps(body),	
				status=200,
				mimetype="application/json"
			)
			return response
		else:
			body = dict()
			body['error'] = 'Not Authorized'
			response = current_app.response_class(
				response = json.dumps(body),	
				status=401,
				mimetype="application/json"
			)
			return response

