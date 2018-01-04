from app import app,models,lm
import os
from flask_login import LoginManager,login_required,login_user,logout_user
from app import db
from flask_mongoalchemy import MongoAlchemy
from flask import Flask, flash, render_template, json, request, redirect, session, url_for
from werkzeug import generate_password_hash, check_password_hash

@app.route('/')
def main():
    return "Hello World"