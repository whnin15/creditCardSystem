from datetime import datetime
from enum import Enum
from DBActions import DBActions
from User import User
from Util import Util

# type of transaction enum
class TransactionType(Enum):
	CHARGE = 1
	PAYMENT = -1

# transaction class (mapped to transactions table)
class Transaction(DBActions):

	#constructor
	def __init__(self, username, amount, transactionType, transactionDate=datetime.today()):
		self.username = username
		# self.payeeCard = payee
		self.amount = amount
		self.transactionType = transactionType
		self.transactionDate = transactionDate.replace(hour=0, minute=0, second=0, microsecond=0)
	
	#representation of a transaction row
	def __repr__(self):
		return "<Transaction (username='{}', amount='{}', transactionType='{}' transactionDate='{:%Y-%m-%d}'>".format(self.username, self.amount, self.transactionType.name, self.transactionDate)

	#creating the row in the transaction table, updating the value in credit card
	def create(self, session):
		super().create(session)
		changeInBalance = self.amount*self.transactionType.value
		Util.updateCreditCard(self.username, changeInBalance, self.transactionDate, session)

	#updating the value in transaction row - this should not be called in general, and when we need to make a change, add a new transaction row
	def update(self, fieldName, newVal, session):
		### TODO: NEED TO UPDATE THE AMOUNT in CREDIT CARD
		if fieldName=='transactionCardNumber':
			self.transactionCardNumber = newVal
		elif fieldName=='amount':
			self.amount = newVal
		elif fieldName=='transactionType':
			self.transactionType = newVal
		elif fieldName=='transactionDate':
			self.transactionDate = newVal
		else:
			raise Exception('Transaction.py: update failed - not valid field:', fieldName)

		session.flush()