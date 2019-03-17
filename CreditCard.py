from datetime import datetime
from datetime import timedelta
import random
from enum import Enum
from DBActions import DBActions

class AccountType(Enum):
	checking = 1
	savings = 2
	credit = 3

class TransactionType(Enum):
	withdrawal = 1
	deposit = -1
	dueInterest = 0

### NEED TO CHECK CREDIT LIMIT
class CreditCard(DBActions):

	def __init__(self, apr, creditLimit, charge=0):
		self.apr = apr
		self.creditLimit = creditLimit
		self.balance = charge
		self.openDate = datetime.now().date()
		self.dueDate = self.openDate + timedelta(days=30)
		self.interest = 0

	def __repr__(self):
		return "<CreditCard (apr='%d', creditLimit='%d', balance='%d', openDate='{%Y-%m-%d}', dueDate='{%Y-%m-%d}', interest='%d') >" % (self.apr, self.creditLimit, self.balance, self.openDate, self.dueDate, self.interest)

	def update(self, fieldName, newVal, session):
		if fieldName=='apr':
			self.apr = newVal
		elif fieldName=='creditLimit':
			self.creditLimit = newVal
		elif fieldName=='balance':
			self.balance = newVal
		elif fieldName=='openDate':
			self.openDate = newVal
		elif fieldName=='dueDate':
			self.dueDate = newVal
		elif fieldName=='interest':
			self.interest = newVal
		else:
			raise 'Transaction.py: getByFieldName - not valid field'

		session.commit()