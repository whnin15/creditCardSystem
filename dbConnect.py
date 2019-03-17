from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, String, Numeric, Integer, BigInteger, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import mapper
from User import User
from CreditCard import CreditCard
from Transaction import Transaction
from Transaction import TransactionType

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
			Column( 'apr', Float, nullable=False),
			Column( 'creditLimit', Float, nullable=False),
			Column( 'balance', Float, nullable=False, default=0),
			Column( 'interest', Float, nullable=False, default=0),
			Column( 'openDate', DateTime, nullable=False ),
			Column( 'lastTransactionDate', DateTime, nullable=False ),
			Column( 'dueDate', DateTime, nullable=False )
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
			Column( 'creditCardNumber', BigInteger, ForeignKey("CreditCards.accountNumber"), unique=True ) #foreign key
		)
		users.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(User, users) # mapping users table object to the User class

	def createTransactionTable(self):	
		# transaction table object
		transactions = Table('Transactions', self.meta,
			Column( 'transaction_id', Integer, primary_key=True ),
			Column( 'username', String(50), ForeignKey("Users.username"), nullable=False),
			# Column( 'payeeCard', BigInteger, ForeignKey("CreditCards.accountNumber"), nullable=False),
			Column( 'amount', Integer, nullable=False ),
			Column( 'transactionType', Enum(TransactionType), nullable=False),
			Column( 'transactionDate', DateTime, nullable=False )
		)
		transactions.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(Transaction, transactions) # mapping transactions table object to the Transaction class

	def run(self):
		self.createCreditCardTable()
		self.createUserTable()
		self.createTransactionTable()

	def getEngine(self):
		return self.engine