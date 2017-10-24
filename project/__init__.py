import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(app)

from project.users.views import users_api
from project.warbles.views import warbles_api

app.register_blueprint(users_api.blueprint, url_prefix='/api/users')
app.register_blueprint(warbles_api.blueprint, url_prefix='/api/screens')
