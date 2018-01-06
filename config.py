import os
basedir = os.path.abspath(os.path.dirname(__file__))
	
WTF_CSRF_ENABLED = True
SECRET_KEY = 'something very secretive and no one knows it!!'

UPLOAD_FOLDER = "/reports"
MAX_CONTENT_PATH = 10000

MONGOALCHEMY_SERVER = os.getenv('DBHOST', 'localhost')
MONGOALCHEMY_DATABASE = "hospital"
MONGOALCHEMY_USER = "testuser"
MONGOALCHEMY_PASSWORD = "testpassd"
MONGOALCHEMY_SERVER_AUTH = False