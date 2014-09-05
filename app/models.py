from app import db

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

    mkcoins = db.relationship('MkCoin', backref = 'user', lazy = 'dynamic')

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

    def my_mkcoin(self):
        return MkCoin.query.filter(MkCoin.user_id == self.user_id).order_by(MkCoin.mktime.desc())
# end class Admin
class MkCoin(db.Model):
    __tablename__ = 'mkcoin'

    key_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.user_id'))
    coins = db.Column(db.Integer)
    mktime = db.Column(db.String)

    def __repr__(self):
        return "<MkCoin(key_id='%d', user_id='%d', coins='%d')>" % (self.key_id, self.user_id,
            self.coins)
# end class MkCoin