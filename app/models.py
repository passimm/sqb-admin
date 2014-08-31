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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.username, self.pwd)

    def my_mkcoin(self):
        return MkCoin.query.filter(MkCoin.user_id == self.user_id).order_by(MkCoin.mktime.desc())
# end class User
class MkCoin(db.Model):
    __tablename__ = 'mkcoin'

    key_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    coins = db.Column(db.Integer)
    mktime = db.Column(db.String)

    def __repr__(self):
        return "<MkCoin(key_id='%d', user_id='%d', coins='%d')>" % (self.key_id, self.user_id,
            self.coins)
# end class MkCoin