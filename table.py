from main import db

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
        return "<User(name='%s', password='%s')>" % (self.userName, self.pwd)
# end class user