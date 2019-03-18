from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, String, Numeric, Integer, BigInteger, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import mapper
from User import User
from CreditCard import CreditCard
from Transaction import Transaction
from Transaction import TransactionType

# connecting to DB and creating tables
class DBConnect:
	
	def __init__(self):
		# connected to database and bind with engine
		self.engine = create_engine('mysql://root@localhost/CreditCardSystem')
		self.connection = self.engine.connect()
		self.Base = declarative_base()
		self.meta = MetaData(bind=self.engine)
		self.meta.create_all(self.engine)

	def createUserObj(self):
		# user table object
		self.users = Table('Users', self.meta,
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
			Column( 'phoneNumber1', Numeric(10) )
		)

	def createUserTable(self):
		self.users.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(User, self.users) # mapping users table object to the User class

	def createCreditCardObj(self):
		#credit card table object
		self.creditCards = Table('CreditCards', self.meta,
			Column( 'accountNumber', BigInteger, primary_key=True),
			Column( 'apr', Float, nullable=False),
			Column( 'creditLimit', Float, nullable=False),
			Column( 'balance', Float, nullable=False, default=0),
			Column( 'interest', Float, nullable=False, default=0),
			Column( 'openDate', DateTime, nullable=False ),
			Column( 'lastTransactionDate', DateTime, nullable=False ),
			Column( 'dueDate', DateTime, nullable=False ),
			Column( 'username', String(50), ForeignKey("Users.username"), nullable=False ) #foreign key
		)

	def createCreditCardTable(self):
		self.creditCards.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(CreditCard, self.creditCards) # mapping creditCards table object to the CreditCard class∂aw

	def createTransactionObj(self):	
		# transaction table object
		self.transactions = Table('Transactions', self.meta,
			Column( 'transaction_id', Integer, primary_key=True ),
			Column( 'username', String(50), ForeignKey("Users.username"), nullable=False),
			Column( 'amount', Integer, nullable=False ),
			Column( 'transactionType', Enum(TransactionType), nullable=False),
			Column( 'transactionDate', DateTime, nullable=False )
		)

	def createTransactionTable(self):
		self.transactions.create(self.engine, checkfirst=True) # create the table if it doesn't exist yet
		mapper(Transaction, self.transactions) # mapping transactions table object to the Transaction class

	def clearTables(self):
		# deleting all tables (so that we can run test.py again and again)
		self.meta.drop_all()

	def createObjs(self):
		# creating the table objects
		self.createUserObj()
		self.createCreditCardObj()
		self.createTransactionObj()

	def createTables(self):
		# creating the tables
		self.createUserTable()
		self.createCreditCardTable()
		self.createTransactionTable()

	def run(self):
		# create objs, delete existing ones and re-creating new ones
		self.createObjs()
		self.clearTables()
		self.createTables()

	def getEngine(self):
		return self.engine