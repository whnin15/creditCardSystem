from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, String, Numeric, Integer, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import mapper
from User import User
from CreditCard import CreditCard
from Transaction import Transaction


class DBConnect:
	
	def __init__(self):
		# connected to database and bind with engine
		self.engine = create_engine('mysql://root@localhost/CreditCardSystem')
		self.connection = self.engine.connect()
		self.Base = declarative_base()
		self.meta = MetaData(bind=self.engine)
		self.meta.create_all(self.engine)

	def createCreditCardTable(self):
		#credit card table object
		creditCards = Table('CreditCards', self.meta,
			Column( 'accountNumber', BigInteger, primary_key=True),
			Column( 'apr', Integer, nullable=False),
			Column( 'creditLimit', Integer, nullable=False),
			Column( 'balance', Integer, nullable=False, default=0),
			Column( 'openDate', DateTime, nullable=False ),
			Column( 'dueDate', DateTime, nullable=False ),
			# Column( 'lastTransactionID', Integer, nullable=False, ForeignKey("Transaction.transactionID") ), #maybe connect with transaction table and get it from there
			Column( 'interest', Integer, nullable=False, default=0)
		)
		creditCards.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(CreditCard, creditCards) # mapping creditCards table object to the CreditCard class∂aw

	def createUserTable(self):
		# user table object
		users = Table('Users', self.meta,
			Column( 'user_id', Integer, primary_key=True ),
			Column( 'username', String(50), nullable=False, unique=True),
			Column( 'password', String(50), nullable=False ),
			Column( 'fullname', String(50), nullable=False ),
			Column( 'email', String(50), nullable=False, unique=True),
			Column( 'streetAddress', String(200) ),
			Column( 'city', String(20) ),
			Column( 'state', String(20) ),
			Column( 'zipCode', Numeric(5) ),
			Column( 'preferredPhoneNumber', Numeric(10) ),
			Column( 'phoneNumber1', Numeric(10) ),
			Column( 'creditCardNumber', BigInteger, ForeignKey("CreditCards.accountNumber") ) #foreign key
		)
		users.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(User, users) # mapping users table object to the User class

	def createTransactionTable(self):	
		# transaction table object
		transactions = Table('Transactions', self.meta,
			Column( 'transaction_id', Integer, primary_key=True ),
			Column( 'payerCard', BigInteger, ForeignKey("CreditCards.accountNumber"), nullable=False),
			Column( 'payeeCard', BigInteger, ForeignKey("CreditCards.accountNumber"), nullable=False),
			Column( 'amount', Integer, nullable=False ),
			Column( 'transactionType', String(20), nullable=False),
			Column( 'transactionDate', DateTime, nullable=False )
		)
		transactions.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(Transaction, transactions) # mapping transactions table object to the Transaction class

	def run(self):
		self.createCreditCardTable()
		self.createUserTable()
		self.createTransactionTable

	def getEngine(self):
		return self.engine