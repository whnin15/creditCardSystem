import unittest
from dbConnect import DBConnect
from sqlalchemy.orm import sessionmaker
from DBActions import DBActions
from User import User
from CreditCard import CreditCard
from Transaction import Transaction
from Transaction import TransactionType

class Test:

	db = DBConnect()
	db.run()

	# workspace
	Session = sessionmaker(bind=db.getEngine())
	session = Session()

	#creating a credit card
	c1=CreditCard(34, 1000)
	c1.create(session)
	c1=session.query(CreditCard).first()

	#adding user accounts
	u1 = User(username='wint', password='wint', fullname='WYH', email='test', creditCardNumber=c1.accountNumber) # creating a user instance
	u2 = User(username='test', password='wint', fullname='Testing', email='test@') # creating a user instance
	u3 = User(username='nnn', password='newpwd', fullname='WYH', email='test~') # creating a user instance
	u1.create(session)
	u2.create(session)

	#updating User u1 object
	u1.update('password','pwd', session)

	#testing transactions
	t1 = Transaction(u1.username, 1000, TransactionType.CHARGE)
	t1.create(session)
	t2 = Transaction(u1.username, 200, TransactionType.PAYMENT)
	t2.create(session)

	session.commit() #close the sesssion