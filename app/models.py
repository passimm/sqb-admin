from app import db

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    pwd = db.Column(db.String)
    money = db.Column(db.Integer)
    yoyo_date = db.Column(db.String)
    yoyo_trycount = db.Column(db.Integer)
    share_date = db.Column(db.String)

    mkcoins = db.relationship('MkCoin', backref = 'user', lazy = 'dynamic')
    approved = db.relationship('Approved', backref = 'user', lazy = 'dynamic')

class Admin(db.Model):
    __tablename__ = 'admin'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    pwd = db.Column(db.String)
    super_user = db.Column(db.Boolean)
    can_approve_mobile = db.Column(db.Boolean)
    can_approve_alipay = db.Column(db.Boolean)
    can_charge = db.Column(db.Boolean)
    user_admin = db.Column(db.Boolean)
    can_statistic = db.Column(db.Boolean)
    approve_limit = db.Column(db.Integer)
    charge_limit = db.Column(db.Integer)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return "<Admin(name='%s', password='%s')>" % (self.username, self.pwd)
# end class Admin

class MkCoin(db.Model):
    __tablename__ = 'mkcoin'

    key_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    coins = db.Column(db.Integer)
    mktime = db.Column(db.String)
    charge_type = db.Column(db.Integer)

    def __repr__(self):
        return "<MkCoin(key_id='%d', user_id='%d', coins='%d')>" % (self.key_id, self.user_id,
            self.coins)

    def str_charge_type(self):
        if self.charge_type == 0:
            return 'mobile'
        elif self.charge_type == 1:
            return 'alipay'
        else:
            return 'unknown'
# end class MkCoin

class Approved(db.Model):
    __tablename__ = 'approved'

    key_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    coins = db.Column(db.Integer)
    mktime = db.Column(db.String)
    charge_type = db.Column(db.Integer)
    approvetime = db.Column(db.String)
    approveby = db.Column(db.Integer, db.ForeignKey('admin.user_id'))

    def __init__(self, user_id, coins, mktime, charge_type, approvetime, approveby):
        self.user_id = user_id
        self.coins = coins
        self.mktime = mktime
        self.charge_type = charge_type
        self.approvetime = approvetime
        self.approveby = approveby
# end class MkCoin