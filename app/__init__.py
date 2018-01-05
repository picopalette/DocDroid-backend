import os
from flask_login import LoginManager
from flask import Flask, render_template, json, request, redirect, session
from werkzeug import generate_password_hash, check_password_hash
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = MongoAlchemy(app)
lm = LoginManager()
lm.init_app(app)

from app import views, routes, models