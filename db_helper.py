from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import table
engine = create_engine('mysql+mysqlconnector://imm:4095687imm@localhost:3306/zqb', echo = True)


sessionMain = sessionmaker()
sessionMain.configure(bind = engine)

session = sessionMain()
user1 = table.User(user_id = 2, username = 'imm2', pwd = '4095687imm', money = 10, yoyo_date = '1988-08-08', yoyo_trycount = 0, share_date = '2014-08-25')
session.add(user1)
session.commit()

print(user1.user_id)