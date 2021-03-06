from datetime import datetime
from datetime import timedelta
from User import User
from CreditCard import CreditCard

# includes actions that are not database actions
class Util:

	# update the balance in the credit card (called when a new transaction is added)
	def updateCreditCard(username, changeInBalance, currTransactionDate, session):
		# get the credit card based on the username
		transactionCard = session.query(CreditCard).filter_by(username=username).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'

		# when the card is overdue, calculate upto the due date first - update balance, interest, lastTransactionDate and dueDate
		while Util.cardIsOverDue(transactionCard[0].dueDate, currTransactionDate):
			interest = Util.calculateInterest( transactionCard[0].balance, transactionCard[0].apr, transactionCard[0].lastTransactionDate, transactionCard[0].dueDate ) # calculate interest up to due date
			transactionCard[0].update('balance', transactionCard[0].interest+interest, session) #update balance (balance + interest)
			transactionCard[0].update('interest', 0, session) #update interest to 0
			transactionCard[0].update('lastTransactionDate', transactionCard[0].dueDate, session) #update last transaction date to due date
			transactionCard[0].update('dueDate', transactionCard[0].dueDate+timedelta(days=30), session) #update due date to next 30 days

		# the card is not overdue (anymore) - update the balance based on transaction we are doing
		interest = Util.calculateInterest( transactionCard[0].balance, transactionCard[0].apr, transactionCard[0].lastTransactionDate, currTransactionDate ) #only call update interest only when update balance is called
		transactionCard[0].update('interest', transactionCard[0].interest+interest, session)
		transactionCard[0].update('balance', changeInBalance, session)
		transactionCard[0].update('lastTransactionDate', currTransactionDate, session)


	# calculate the interest for the given parameters
	def getInterest( username, fromDate, toDate, session, balance=None ):
		# get the credit card based on the username
		transactionCard = session.query(CreditCard).filter_by(username=username).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'

		# when the card is overdue, calculate upto the due date first - update balance, interest, lastTransactionDate and dueDate
		if balance is None:
			balance = transactionCard[0].balance
		totalInterest = 0
		dueDate = transactionCard[0].dueDate
		while Util.cardIsOverDue(dueDate, toDate):
			interest = Util.calculateInterest( balance, transactionCard[0].apr, fromDate, dueDate ) # calculate interest up to due date
			totalInterest += interest
			balance += interest
			fromDate = dueDate
			dueDate = dueDate + timedelta(days=30)
		
		# the card is not overdue. calculate the interest upto the transactionDate
		return Util.calculateInterest( balance, transactionCard[0].apr, fromDate, toDate ) + totalInterest

	# performing the calculation
	def calculateInterest( balance, apr, fromDate, toDate ):
		if (balance <= 0):
			return 0
		dayRange = (toDate - fromDate).days
		return round( (balance * (apr/365) * dayRange), 2)

	# check if card is overdue
	def cardIsOverDue(dueDate, currTransactionDate):
		if (dueDate < currTransactionDate ):
			return True
		else:
			return False