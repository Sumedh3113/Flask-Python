
# we import os to user environment variable to hide sensitive info like username and password
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# we need mail server for this functionality
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = '53b73a29a3667dc1ea23f4a484ea'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# here we have assigned path of sql file site.db it will be created in same directory as our project as we used ///
#dummy data

db = SQLAlchemy(app)

bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = 'login'
#@loginrequired will redirect you to this link
login_manager.login_message_category = 'info'
# this is just to change appearence of flash message at login page

#Mail Server#
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sumedhdeshpande31@gmail.com'
app.config['MAIL_PASSWORD'] = 'medhamai1331'
# this variable is imported in routes.py
mail = Mail(app)

from flask_blog import routes
#to avoid circular import