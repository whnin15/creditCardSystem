from datetime import datetime
from enum import Enum
from DBActions import DBActions
from User import User
from CreditCard import CreditCard
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
		self.transactionDate = transactionDate
	
	def __repr__(self):
		return "<Transaction (username='{}', amount='{}', transactionType='{}' transactionDate='{:%Y-%m-%d}'>".format(self.username, self.amount, self.transactionType.name, self.transactionDate)

	def create(self, session):
		print(self)
		super().create(session)
		changeInBalance = self.amount*self.transactionType.value
		Util.updateCreditCard(self.username, changeInBalance, self.transactionDate, session)

	def update(self, fieldName, newVal, session):
		if fieldName=='transactionCardNumber':
			self.transactionCardNumber = newVal
		elif fieldName=='amount':
			self.amount = newVal
		elif fieldName=='transactionType':
			self.transactionType = newVal
		elif fieldName=='transactionDate':
			self.transactionDate = newVal
		else:
			raise 'Transaction.py: getByFieldName - not valid field'

		session.flush()


	#add interest whenever i call this transaction