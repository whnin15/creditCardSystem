from datetime import datetime
from datetime import timedelta
from User import User
from CreditCard import CreditCard

class Util:

	def updateCreditCard(username, changeInBalance, currTransactionDate, session):
		user = session.query(User).filter_by(username=username).all()
		if len(user) > 1:
			raise 'duplicate usernames'

		transactionCard = session.query(CreditCard).filter_by(username=user[0].username).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'

		while Util.cardIsOverDue(transactionCard[0].dueDate, currTransactionDate):
			interest = Util.calculateInterest( transactionCard[0].balance, transactionCard[0].apr, transactionCard[0].lastTransactionDate, transactionCard[0].dueDate ) # calculate interest up to due date
			transactionCard[0].update('balance', transactionCard[0].interest+interest, session) #update balance (balance + interest)
			transactionCard[0].update('interest', 0, session) #update interest to 0
			transactionCard[0].update('lastTransactionDate', transactionCard[0].dueDate, session) #update last transaction date to due date
			transactionCard[0].update('dueDate', transactionCard[0].dueDate+timedelta(days=30), session) #update due date to next 30 days

		# the card is not overdue anymore - update the balance based on transaction we are doing
		interest = Util.calculateInterest( transactionCard[0].balance, transactionCard[0].apr, transactionCard[0].lastTransactionDate, currTransactionDate ) #only call update interest only when update balance is called
		transactionCard[0].update('interest', transactionCard[0].interest+interest, session)
		transactionCard[0].update('balance', changeInBalance, session)
		transactionCard[0].update('lastTransactionDate', currTransactionDate, session)


	def getInterest( username, fromDate, toDate, session ):
		user = session.query(User).filter_by(username=username).all()
		if len(user) > 1:
			raise 'duplicate usernames'

		transactionCard = session.query(CreditCard).filter_by(username=user[0].username).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'

		balance = transactionCard[0].balance
		dueDate = transactionCard[0].dueDate
		prev_interest = transactionCard[0].interest
		while Util.cardIsOverDue(dueDate, toDate):
			balance += prev_interest + Util.calculateInterest( balance, transactionCard[0].apr, fromDate, dueDate ) # calculate interest up to due date
			prev_interest = 0
			fromDate = dueDate
			dueDate = dueDate + timedelta(days=30)
		
		return Util.calculateInterest( balance, transactionCard[0].apr, fromDate, toDate ) + (balance - transactionCard[0].balance)


	def calculateInterest( balance, apr, fromDate, toDate ):
		print('inside: ', balance, fromDate, toDate, (fromDate - toDate).days, apr )
		if (balance <= 0):
			return 0
		dayRange = (toDate - fromDate).days
		return round( (balance * (apr/365) * dayRange), 2)


	def cardIsOverDue(dueDate, currTransactionDate):
		if (dueDate < currTransactionDate ):
			return True
		else:
			return False