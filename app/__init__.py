from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:4095687imm@localhost:3306/zqb'
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models

# for debug
from models import User, MkCoin
print 'init!'
for i, j in db.session.query(MkCoin, User).filter(MkCoin.user_id == User.user_id).all():
	print(i)
	print(j)