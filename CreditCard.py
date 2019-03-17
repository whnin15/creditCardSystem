from datetime import datetime
from datetime import timedelta
from enum import Enum
from DBActions import DBActions

class AccountType(Enum):
	checking = 1
	savings = 2
	credit = 3

class CreditCard(DBActions):

	def __init__(self, apr, creditLimit, charge=0, interest=0, openDate=datetime.today(), lastTransactionDate=None, dueDate=None):
		self.apr = apr/100
		self.creditLimit = creditLimit
		self.balance = charge
		self.interest = interest
		self.openDate = openDate
		self.lastTransactionDate = openDate
		if dueDate is None:
			self.dueDate = self.openDate+timedelta(days=30)
		else:
			self.dueDate = dueDate

	def __repr__(self):
		return "<CreditCard (apr='{}', creditLimit='{}', balance='{}', interest='{}', openDate='{:%Y-%m-%d}', lastTransactionDate,='{:%Y-%m-%d}', dueDate='{:%Y-%m-%d}') >".format(self.apr, self.creditLimit, self.balance, self.interest, self.openDate, self.lastTransactionDate, self.dueDate)

	def update(self, fieldName, newVal, session):
		if fieldName=='apr':
			self.apr = newVal
		elif fieldName=='creditLimit':
			self.creditLimit = newVal
		elif fieldName=='balance':
			self.balance += newVal
		elif fieldName=='interest':
			self.interest += newVal
		elif fieldName=='openDate':
			self.openDate = newVal
		elif fieldName=='lastTransactionDate':
			self.lastTransactionDate = newVal
		elif fieldName=='dueDate':
			self.dueDate = newVal
		else:
			raise 'Transaction.py: getByFieldName - not valid field'

		session.flush()