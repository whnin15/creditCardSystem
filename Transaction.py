from datetime import datetime
from enum import Enum
from DBActions import DBActions
from User import User
from Util import Util

class TransactionType(Enum):
	CHARGE = 1
	PAYMENT = -1
	ADDINTEREST = 0

class Transaction(DBActions):
	def __init__(self, username, amount, transactionType, transactionDate=datetime.today()):
		self.username = username
		# self.payeeCard = payee
		self.amount = amount
		self.transactionType = transactionType
		self.transactionDate = transactionDate.replace(hour=0, minute=0, second=0, microsecond=0)
	
	def __repr__(self):
		return "<Transaction (username='{}', amount='{}', transactionType='{}' transactionDate='{:%Y-%m-%d}'>".format(self.username, self.amount, self.transactionType.name, self.transactionDate)

	def create(self, session):
		super().create(session)
		changeInBalance = self.amount*self.transactionType.value
		Util.updateCreditCard(self.username, changeInBalance, self.transactionDate, session)

	def update(self, fieldName, newVal, session):
		if fieldName=='transactionCardNumber':
			self.transactionCardNumber = newVal
		elif fieldName=='amount':
			#### NEED TO UPDATE THE AMOUNT in CREDIT CARD
			self.amount = newVal
		elif fieldName=='transactionType':
			self.transactionType = newVal
		elif fieldName=='transactionDate':
			self.transactionDate = newVal
		else:
			raise Exception('Transaction.py: update failed - not valid field:', fieldName)

		session.flush()