from app import app,models,lm
import os
from flask_login import LoginManager,login_required,login_user,logout_user
from app import db
from flask_mongoalchemy import MongoAlchemy
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from werkzeug import generate_password_hash, check_password_hash

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUpHospital',methods = ['POST','GET'])
def showSignUpHospital():
	return render_template('signup.html')

@app.route('/signUpHospital',methods = ['POST','GET'])
def signUpHospital():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	address = request.form['address']
	lat = request.form['lat']
	log = request.form['log']
	location = [float(lat),float(log)]

	content = { "name": name, "email": email, "password": password, "address": address, "location": location }
	obj = models.Hospital()
	obj.create(content)
	obj.save() 
	
	flash("Successfully Registered..")
	return redirect(url_for('showLoginHospital'))

@app.route('/showLoginHospital',methods = ['POST','GET'])
def showLoginHospital():
	return render_template('login.html')


@app.route('/loginHospital',methods = ['POST','GET'])
def loginHospital():
	email = request.form['email']
	password = request.form['password']
	obj = models.Hospital.filter(models.Hospital.email == email,models.Hospital.password == password).first()

	if obj is not None:
		login_user(obj)
		flash("Successfully Logged In")
		return redirect(url_for('main'))
	else:
		flash("Invalid Credentials")
		return redirect(url_for('showLoginHospital'))

@lm.user_loader
def load_user(email):
	obj = models.Hospital.query.filter(models.Hospital.email == email).first()
	return obj;

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('main'))