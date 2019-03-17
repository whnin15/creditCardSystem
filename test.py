import unittest
from dbConnect import DBConnect
from sqlalchemy.orm import sessionmaker
from User import User
from CreditCard import CreditCard
from DBActions import DBActions

class Test:

	db = DBConnect()
	db.run()

	# workspace
	Session = sessionmaker(bind=db.getEngine())
	session = Session()

	#clearing the user table
	result = session.query(User).all()
	if isinstance(result, (list,) ):
		for i in result:
			DBActions.delete(i, session)
	else:
		DBActions.delete(result, session)

	#creating a credit card
	c1=CreditCard(apr=34, creditLimit=1000)
	c1.create(session)

	#adding user accounts
	u1 = User(username='wint', password='wint', fullname='WYH', email='test') # creating a user instance
	u2 = User(username='test', password='wint', fullname='Testing', email='test@') # creating a user instance
	u3 = User(username='nnn', password='newpwd', fullname='WYH', email='test~') # creating a user instance
	u1.create(session)
	u2.create(session)

	#updating User u1 object
	u1.update('password','pwd', session)

	# payerCard = session.query(User).filter_by(username='wint').all()
	# payeeCard = session.query(User).filter_by(username='test').all()
	# t1 = Transaction()