from flask import render_template, request, g, url_for, redirect, flash
from models import Admin, MkCoin
from forms import LoginForm
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required

POSTS_PER_PAGE = 2

@lm.user_loader
def load_user(user_id):
	return Admin.query.get(int(user_id))
#end def load_user

@app.before_request
def before_request():
    g.user = current_user
#end def before_request

@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		admin = Admin.query.filter(Admin.username == form.username.data).first()
		if admin is None:
			flash('Admin %s does not exist!' % form.username.data)
		elif admin.pwd != form.password.data:
			flash('Wrong password!')
		else:
			login_user(admin)
			return redirect(url_for('hello', type = 'approve'))			
	return render_template('login.html', title = 'Sign In', form = form)
#end def login

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#end def logout

'''
type -> {'approve', 'charge', 'declined', 'charged'}
'''
@app.route('/index/<type>', methods = ['GET', 'POST'])
@app.route('/index/<type>/<int:page>', methods = ['GET', 'POST'])
@login_required
def hello(type, page = 1):
	if request.method == 'POST':
		la = request.form.getlist('tn')
	mkcoin = g.user.my_mkcoin().paginate(page, POSTS_PER_PAGE, False)
	return render_template('index.html', user = current_user, mkcoin = mkcoin, type = type)
#end def hello

@app.route('/detail/<type>/<int:id>/<int:page>', methods = ['GET', 'POST'])
@login_required
def detail(type, id, page):
	if request.method == 'POST':
		return " %s %d success!" % (type, id)
	return render_template('detail.html', type = type, page = page)
#end def detail


