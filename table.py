from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    pwd = Column(String)
    money = Column(Integer)
    yoyo_date = Column(String)
    yoyo_trycount = Column(Integer)
    share_date = Column(String)

    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.userName, self.pwd)
# end class user