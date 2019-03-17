from datetime import datetime
from DBActions import DBActions

class Transaction(DBActions):
	def __init__(self, payer, payee, amount, transactionType):
		self.payerCard = payer
		self.payeeCard = payee
		self.amount = amount
		self.transactionType = transactionType
		self.transactionDate = datetime.now()
	
	def __repr__(self):
		return "<Transaction (payerUsername='%s', payeeUsername='%s', amount='%d', transactionType='%s' transactionDate='{%Y-%m-%d}'>" % (self.payerCard, self.payeeCard, self.amount, self.transactionType, self.transactionDate)

	def update(self, fieldName, newVal, session):
		if fieldName=='payerCard':
			self.payerCard = newVal
		elif fieldName=='payeeCard':
			self.payeeCard = newVal
		elif fieldName=='amount':
			self.amount = newVal
		elif fieldName=='transactionType':
			self.transactionType = newVal
		elif fieldName=='transactionDate':
			self.transactionDate = newVal
		else:
			raise 'Transaction.py: getByFieldName - not valid field'

		session.commit()


	#add interest whenever i call this transaction