from flask import render_template, request, g, url_for, redirect, flash, session
from models import Admin, MkCoin, Approved
from forms import LoginForm, ModifyAdminForm, AddAdminForm
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required
import time

POSTS_PER_PAGE = 2

'''
index.html:
	type -> {'approve', 'charge', 'declined', 'charged', 'blank'}

charge_type:
	0 -> mobile
	1 -> alipay
'''
@lm.user_loader
def load_user(user_id):
	return Admin.query.get(int(user_id))
#end def load_user

@app.before_request
def before_request():
    g.user = current_user
#end def before_request

def checkUser(user, type):
	if user.super_user:
		return True
	elif type == 'approve' or type == 'declined':
		return user.can_approve_mobile or user.can_approve_alipay
	elif type == 'charge':
		return user.can_charge
	else:
		return True
#end checkUser

def checkMkcoin(admin, mkcoin):
	if admin.super_user:
		return True
	elif mkcoin.charge_type == 0 and not admin.can_approve_mobile:
		return False
	elif mkcoin.charge_type == 1 and not admin.can_approve_alipay:
		return False
	else:
		return True
#end checkMkcoin

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
			return redirect(url_for('hello', type = 'blank'))			
	return render_template('login.html', title = 'Sign In', form = form)
#end def login

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#end def logout

@app.route('/index/<type>', methods = ['GET', 'POST'])
@app.route('/index/<type>/<int:page>', methods = ['GET', 'POST'])
@login_required
def hello(type, page = 1):
	if not checkUser(g.user, type):
		return "can't access this page!"
	if type == 'approve':
		mkcoin = MkCoin.query.paginate(page, POSTS_PER_PAGE, False)
	elif type == 'blank':
		mkcoin = None
	else:
		return 'fixme!'
	return render_template('index.html', user = current_user, mkcoin = mkcoin, type = type)
#end def hello

@app.route('/detail/<type>/<int:id>/<int:page>', methods = ['GET', 'POST'])
@login_required
def detail(type, id, page):
	if not checkUser(g.user, type):
		return "can't access this page!"
	if request.method == 'POST':
		if type == 'approve':
			mkcoin = MkCoin.query.get(int(id))
			if not checkMkcoin(g.user, mkcoin):
				flash('unauthorized operation : approve %s' % mkcoin.str_charge_type())
			else:	
				approved = Approved(mkcoin.user_id, mkcoin.coins, mkcoin.mktime, mkcoin.charge_type, str(time.asctime(time.localtime(time.time()))), g.user.user_id)
				db.session.delete(mkcoin)
				db.session.add(approved)
				db.session.commit()
				return redirect(url_for('hello', type = type, page = page))
	return render_template('detail.html', type = type, page = page)
#end def detail

@app.route('/statistic', methods = ['GET', 'POST'])
@login_required
def statistic():
	return "fix me!"

@app.route('/listadmin', methods = ['GET', 'POST'])
@app.route('/listadmin/<int:page>', methods = ['GET', 'POST'])
@login_required
def list_admin(page = 1):
	if not g.user.super_user:
		return "can't access this page"
	session['admin_page'] = page
	admin = Admin.query.filter(Admin.super_user == False).paginate(page, POSTS_PER_PAGE, False)
	return render_template('listadmin.html', admin = admin)

@app.route('/newadmin', methods = ['GET', 'POST'])
@login_required
def new_admin():
	if not g.user.super_user:
		return "can't access this page"
	form = AddAdminForm()
	if form.validate_on_submit():
		admin = Admin()
		admin.username = form.username.data
		admin.pwd = form.pwd.data
		admin.super_user = form.user_admin.data
		admin.can_approve_mobile = form.can_approve_mobile.data
		admin.can_approve_alipay = form.can_approve_alipay.data
		admin.can_charge = form.can_charge.data
		admin.user_admin = form.user_admin.data
		admin.can_statistic = form.can_statistic.data
		admin.approve_limit = form.approve_limit.data
		admin.charge_limit = form.charge_limit.data
		db.session.add(admin)
		db.session.commit()	
		return redirect(url_for('list_admin'))
	return render_template('addadmin.html', form = form)

@app.route('/modifyadmin/<int:id>', methods = ['GET', 'POST'])
@login_required
def modify_admin(id):
	if not g.user.super_user:
		return "can't access this page"
	admin = Admin.query.get(int(id))
	form = ModifyAdminForm()
	if form.validate_on_submit():
		admin.can_approve_mobile = form.can_approve_mobile.data
		admin.can_approve_alipay = form.can_approve_alipay.data
		admin.can_charge = form.can_charge.data
		admin.user_admin = form.user_admin.data
		admin.can_statistic = form.can_statistic.data
		admin.approve_limit = form.approve_limit.data
		admin.charge_limit = form.charge_limit.data
		db.session.commit()
		return redirect(url_for('list_admin', page = session['admin_page']))
	if request.method == 'GET':
		form.setAdmin(admin) 
	return render_template('modifyadmin.html', admin = admin, id = id, form = form)

