from datetime import datetime
from datetime import timedelta
from enum import Enum
from DBActions import DBActions
from User import User

class AccountType(Enum):
	checking = 1
	savings = 2
	credit = 3

class CreditCard(DBActions):

	def __init__(self, username, apr, creditLimit, charge=0, interest=0, openDate=datetime.today(), lastTransactionDate=None, dueDate=None):
		self.username = username
		self.apr = apr/100
		self.creditLimit = creditLimit
		if (charge > self.creditLimit):
			raise Exception('charge is over limit. Failed.')
		self.balance = charge
		self.interest = interest
		self.openDate = openDate
		self.lastTransactionDate = openDate
		if dueDate is None:
			self.dueDate = self.openDate+timedelta(days=30)
		else:
			self.dueDate = dueDate

	def __repr__(self):
		return "<CreditCard (Owner='{}', apr='{}', creditLimit='{}', balance='{}', interest='{}', openDate='{:%Y-%m-%d}', lastTransactionDate,='{:%Y-%m-%d}', dueDate='{:%Y-%m-%d}') >".format(self.username, self.apr, self.creditLimit, self.balance, self.interest, self.openDate, self.lastTransactionDate, self.dueDate)

	def update(self, fieldName, newVal, session):
		if fieldName=='username':
			self.username = newVal
		elif fieldName=='apr':
			self.apr = newVal
		elif fieldName=='creditLimit':
			self.creditLimit = newVal
		elif fieldName=='balance':
			if (charge > self.creditLimit):
				raise Exception('charge is over limit. Failed.')
			self.balance += newVal
		elif fieldName=='interest':
			self.interest = newVal
		elif fieldName=='openDate':
			self.openDate = newVal
		elif fieldName=='lastTransactionDate':
			self.lastTransactionDate = newVal
		elif fieldName=='dueDate':
			self.dueDate = newVal
		else:
			raise Exception('Transaction.py: update failed - not valid field:', fieldName)

		session.flush()