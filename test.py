import unittest
from dbConnect import DBConnect
from sqlalchemy.orm import sessionmaker
from DBActions import DBActions
from User import User
from CreditCard import CreditCard
from Transaction import Transaction
from Transaction import TransactionType
from Util import Util
from datetime import datetime
from datetime import timedelta

class Test:

	db = DBConnect()
	db.run()

	# workspace
	Session = sessionmaker(bind=db.getEngine())
	session = Session()

	#adding user accounts
	u1 = User(username='wint', password='wint', fullname='WYH', email='test') # creating a user instance
	u1.create(session)

	#creating a credit card
	c1=CreditCard(u1.username, 35, 1000, 500)
	c1.create(session)
	c1=session.query(CreditCard).first()

	# u2 = User(username='test', password='wint', fullname='Testing', email='test@') # creating a user instance
	# u3 = User(username='nnn', password='newpwd', fullname='WYH', email='test~') # creating a user instance
	# u2.create(session)

	#updating User u1 object
	u1.update('password','pwd', session)

	#testing transactions
	# u1=session.query(User).filter_by(username='wint').first()

	# t1 = Transaction(u1.username, 200, TransactionType.PAYMENT, c1.openDate+timedelta(days=15) )
	# t1.create(session)
	# t2 = Transaction(u1.username, 100, TransactionType.CHARGE, c1.openDate+timedelta(days=25) )
	# t2.create(session)
	# t3 = Transaction(u1.username, 400, TransactionType.PAYMENT, c1.openDate+timedelta(days=35) )
	# t3.create(session) 

	# # print( Util.getInterest( u1.username, c1.lastTransactionDate, c1.openDate+timedelta(days=35), session ) )

	session.commit() #close the sesssion