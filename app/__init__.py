from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import *

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()


@app.errorhandler(404)
def not_found(error):
    return f"Not Found. Error: {error}"

# import after initialization of app, otherwise you will get something partially initialized app error
from app.accounts.routesAPI import accounts_api_router as accounts_api
app.register_blueprint(accounts_api)


from app.notes.routesAPI import notes_api_router as notes_api
app.register_blueprint(notes_api)


from app.accounts.routesWeb import accounts_web_router as accounts_web
app.register_blueprint(accounts_web)


from app.notes.routesWeb import notes_web_router as notes_web
app.register_blueprint(notes_web)

login_manager.login_view = 'accountsweb.login'
login_manager.login_message_category = 'info'
login_manager.init_app(app)
if not os.path.exists(os.path.join(BASE_DIR,DATABASE_NAME)):
    print(f"Database not present at {os.path.join(BASE_DIR,DATABASE_NAME)}. Initializing...")
    db.create_all()
else:
    print(f"Database found at {os.path.join(BASE_DIR,DATABASE_NAME)}")
