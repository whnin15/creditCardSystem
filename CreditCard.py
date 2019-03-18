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
			# what should be the right behavior when over draft?
			raise Exception('charge is over limit. Failed.')
		self.balance = charge
		# add to transaction when there is a charge (need to find a way not to circle between modules)
		self.interest = interest
		self.openDate = openDate.replace(hour=0, minute=0, second=0, microsecond=0)
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
			self.apr = newVal/100
		elif fieldName=='creditLimit':
			self.creditLimit = newVal
		elif fieldName=='balance':
			if ((self.balance+newVal) > self.creditLimit):
				# what if the over limit comes from interest. May be add a overdraft fee when over credit limit
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