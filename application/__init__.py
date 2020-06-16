from flask import Flask
from os import getenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI']=getenv('SURF_URI')
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = getenv('MY_SECRET_KEY')

from application import routes
