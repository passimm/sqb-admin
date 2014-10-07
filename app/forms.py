from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, IntegerField	
from wtforms.validators import Required, EqualTo, NumberRange, ValidationError
from models import Admin

class LoginForm(Form):
	username = TextField('username', validators = [Required()])
	password = PasswordField('password', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)
#end class LoginForm

class ModifyAdminForm(Form):
	can_approve_mobile = BooleanField('can_approve_mobile')
	can_approve_alipay = BooleanField('can_approve_alipay')
	can_charge = BooleanField('can_charge')
	user_admin = BooleanField('user_admin')
	can_statistic = BooleanField('can_statistic')
	approve_limit = IntegerField('approve_limit', [NumberRange(0, 10000, "must within 0 ~ 10000")])
	charge_limit = IntegerField('charge_limit', [NumberRange(0, 10000, "must within 0 ~ 10000")])

	def setAdmin(self, admin):
		self.can_approve_mobile.data = admin.can_approve_mobile
		self.can_approve_alipay.data = admin.can_approve_alipay
		self.can_charge.data = admin.can_charge
		self.user_admin.data = admin.user_admin
		self.can_statistic.data = admin.can_statistic
		self.approve_limit.data = admin.approve_limit
		self.charge_limit.data = admin.charge_limit
#end class ModifyAdminForm

class AddAdminForm(ModifyAdminForm):
	username = TextField('username', [Required()])
	pwd = PasswordField('password', [Required(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('confirm')
	def validate_username(form, field):
		admin = Admin.query.filter(Admin.username == field.data).first()
		if admin is not None:
			raise ValidationError('username already exists!!!')
	def setAdmin(self, admin):
		assert False #should not call this!
#end class AddAdminForm