from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

POSTS_PER_PAGE = 3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:4095687imm@localhost:3306/zqb'
db = SQLAlchemy(app)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    pwd = db.Column(db.String)
    money = db.Column(db.Integer)
    yoyo_date = db.Column(db.String)
    yoyo_trycount = db.Column(db.Integer)
    share_date = db.Column(db.String)

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.username, self.pwd)
# end class user

class MkCoin(db.Model):
	__tablename__ = 'mkcoin'

	key_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, ForeignKey('user.user_id'))
	coins = db.Column(db.Integer)
	mktime = db.Column(db.String)

	user = relationship("User", backref=backref('mkcoin', order_by=key_id))

	def __repr__(self):
		return "<MkCoin(key_id='%d', user_id='%d', coins='%d')>" % (self.key_id, self.user_id,
			self.coins)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		return render_template('hello.html', username = request.form['username'])
	else:
		return render_template('hello.html')

@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
   	posts = User.query.paginate(page, POSTS_PER_PAGE, False).items
   	return render_template('hello.html',
        title = 'Home',
        form = request.form,
        posts = posts)

if __name__ == '__main__':
	#for i in MkCoin.query.join(User).filter(MkCoin.user_id == User.user_id).all():
   	posts = MkCoin.query.join(User).filter(MkCoin.user_id == User.user_id).paginate(1, POSTS_PER_PAGE, False).items
	for i, j in db.session.query(MkCoin, User).filter(MkCoin.user_id == User.user_id).all():
		print(i)
		print(j)
	app.run(debug=True)
