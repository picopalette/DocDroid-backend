from app import app,models,lm
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
	return jsonify(content)


@app.route('/api/signUpDriver',methods = ['POST','GET'])
def signUpDriver():
	content = request.get_json()
	obj = models.Ambulance()
	obj.create(content)
	obj.save()
	return jsonify(content)


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

		response.set_cookie('id',value=obj.phone)

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
		);	

		response.set_cookie('id',value=obj.phone)

	else:
		response = current_app.response_class(
			response = json.dumps(content),	
			status=401,
			mimetype="application/json"
		);	
	return response
	