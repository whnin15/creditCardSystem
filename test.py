import unittest
from dbConnect import DBConnect
from sqlalchemy.orm import sessionmaker
from User import User
from CreditCard import CreditCard
from Transaction import Transaction
from Transaction import TransactionType
from Util import Util
from datetime import datetime
from datetime import timedelta


db = DBConnect()
db.run()

# workspace
Session = sessionmaker(bind=db.getEngine())
session = Session()

class TestTables(unittest.TestCase):
	
	# testing inserting rows - insert and assert it exists in the table
	def test01_insert_rows(self):
		#inserting to users table	
		u1 = User('customer1', 'customer1', 'Customer One', 'customer1@gmail.com', city="Chicago", state="IL") # creating a user instance
		u1.create(session) #adding user account
		session.commit()
		self.assertIsNotNone( session.query(User).filter_by(username='customer1').scalar(), "Row is not inserted for Users Table" )

		#inserting to creditcards table
		c1 = CreditCard( u1.username, 20, 1000)
		c1.create(session)
		session.commit()
		self.assertIsNotNone( session.query(CreditCard).filter_by(username='customer1').scalar(), "Row is not inserted for CreditCards Table" )

		#inserting to transactions table
		t1 = Transaction( u1.username, 500, TransactionType.CHARGE)
		t1.create(session)
		session.commit()
		self.assertIsNotNone( session.query(Transaction).filter_by(username='customer1').scalar(), "Row is not inserted for Transactions Table" )

	# testing updating rows - update and retrieve object and assert column value
	def test02_update_rows(self):
		#updating state column in users table
		u1 = session.query(User).filter_by(username='customer1').first()
		self.assertEqual( session.query(User).filter_by(username='customer1').first().state, 'IL', "Row is not updated for Users Table" )
		u1.update('state', 'MI', session)
		session.commit()
		self.assertEqual( session.query(User).filter_by(username='customer1').first().state, 'MI', "Row is not updated for Users Table" )

		#updating apr column in creditcards table
		c1 = session.query(CreditCard).filter_by(username='customer1').first()
		self.assertEqual( session.query(CreditCard).filter_by(username='customer1').first().apr, 0.2, "Row is not updated for CreditCards Table" )
		c1.update('apr', 35, session) #adding user account
		session.commit()
		self.assertEqual( session.query(CreditCard).filter_by(username='customer1').first().apr, 0.35, "Row is not updated for CreditCards Table" )

		#updating transaction type column in transactions table
		t1 = session.query(Transaction).filter_by(username='customer1').first()
		self.assertEqual( session.query(Transaction).filter_by(username='customer1').first().transactionType, TransactionType.CHARGE, "Row is not updated for Transactions Table" )
		t1.update('transactionType', TransactionType.PAYMENT, session) #adding user account
		session.commit()
		self.assertEqual( session.query(Transaction).filter_by(username='customer1').first().transactionType, TransactionType.PAYMENT, "Row is not updated for Transactions Table" )

	# testing deleting rows - delete and assert it doesn't exist
	def test03_delete_rows(self):

		# deleting the row with username 'customer1' in creditcards table
		c1 = session.query(CreditCard).filter_by(username='customer1').first()
		self.assertIsNotNone( session.query(CreditCard).filter_by(username='customer1').scalar(), "Row is already deleted for CreditCards Table" )
		c1.delete(session)
		session.commit()
		self.assertIsNone( session.query(CreditCard).filter_by(username='customer1').scalar(), "Row is not deleted for CreditCards Table" )

		# deleting the row with username 'customer1' in transactions table
		t1 = session.query(Transaction).filter_by(username='customer1').first()
		self.assertIsNotNone( session.query(Transaction).filter_by(username='customer1').scalar(), "Row is already deleted for Transactions Table" )
		t1.delete(session)
		session.commit()
		self.assertIsNone( session.query(Transaction).filter_by(username='customer1').scalar(), "Row is not deleted for Transactions Table" )

		# deleting the row with username 'customer1' in users table
		u1 = session.query(User).filter_by(username='customer1').first()
		self.assertIsNotNone( session.query(User).filter_by(username='customer1').scalar(), "Row is already deleted for Users Table" )
		u1.delete(session) #adding user account
		session.commit()
		self.assertIsNone( session.query(User).filter_by(username='customer1').scalar(), "Row is not deleted for Users Table" )


class TestUtil(unittest.TestCase):

	def createInstances(self):
		# inserting a user and a credit card in tables
		u1 = User('customer1', 'customer1', 'Customer One', 'customer1@gmail.com', city="Chicago", state="IL")
		u1.create(session)
		c1 = CreditCard( u1.username, 35, 1000, 500)
		c1.create(session)
		session.commit()

	def removedTime(self, fromDate):
		# to correctly calculate days, remove the time and keep track of only the date
		return fromDate.replace(hour=0, minute=0, second=0, microsecond=0)

	def test01_cardIsOverDue(self):
		# testing overdue method works correctly
		self.assertEqual( Util.cardIsOverDue( datetime.today(), datetime.today()+timedelta(days=1) ), True, "Test01: Util.cardIsOverDue() failed." )

	def test02_cardIsNotOverDue(self):
		# testing overdue method works correctly
		self.assertEqual( Util.cardIsOverDue( datetime.today()+timedelta(days=1), datetime.today() ), False, "Test02: Util.cardIsOverDue() failed." )

	def test03_interest(self):
		self.createInstances()
		# calculating interest (Scenario 1)
		today = self.removedTime(datetime.today())
		self.assertEqual( Util.getInterest( 'customer1', today, today+timedelta(days=30), session ), 14.38, "Test03: Util.getInterest() failed." )

	def test04_interest(self):
		# calculating interest (Scenario 2)
		interest = 0
		today = self.removedTime(datetime.today())
		interest += Util.getInterest( 'customer1', today, today+timedelta(days=15), session, 500 )
		interest += Util.getInterest( 'customer1', today+timedelta(days=15), today+timedelta(days=25), session, 300 )
		interest += Util.getInterest( 'customer1', today+timedelta(days=25), today+timedelta(days=30), session, 400 )
		session.commit()
		self.assertEqual( interest, 11.99, "Test04: Util.getInterest() failed." )

	def test05_overDueInterest(self):
		# calculating interest - overdue (balance is added with interest after dueDate)
		today = self.removedTime(datetime.today())
		self.assertEqual( Util.getInterest( 'customer1', today, today+timedelta(days=35), session, 500 ), 16.85, "Test05: Util.getInterest() failed." )


if __name__ == '__main__':
	unittest.main()