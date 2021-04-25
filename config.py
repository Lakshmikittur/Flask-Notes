import os

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__name__))
DATABASE_NAME = "notes.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR,DATABASE_NAME)}"
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "medhasession"
SECRET_KEY = "medhasecret"