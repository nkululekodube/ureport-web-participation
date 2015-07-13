import os

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

USERNAME = 'admin'

PASSWORD = 'admin'

SQLALCHEMY_DATABASE_URI = "postgresql://" + USERNAME + ":" + PASSWORD+"@localhost/test"
	
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"