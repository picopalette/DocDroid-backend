import os
basedir = os.path.abspath(os.path.dirname(__file__))
	
WTF_CSRF_ENABLED = True
SECRET_KEY = 'something very secretive and no one knows it!!'

MONGOALCHEMY_DATABASE = "hospital"
MONGOALCHEMY_USER = "testuser"
MONGOALCHEMY_PASSWORD = "testpassd"
MONGOALCHEMY_SERVER_AUTH = False