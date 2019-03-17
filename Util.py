from datetime import datetime
from datetime import timedelta
from CreditCard import AccountType
from User import User
from CreditCard import CreditCard

class Util:

	def updateCreditCard(username, changeInBalance, currTransactionDate, session):
		user = session.query(User).filter_by(username=username).all()
		if len(user) > 1:
			raise 'duplicate usernames'

		transactionCard = session.query(CreditCard).filter_by(accountNumber=user[0].creditCardNumber).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'
		#get last transaction date

		# if the card is not overdue yet
		interest = Util.calculateInterest( transactionCard[0], transactionCard[0].lastTransactionDate, currTransactionDate ) #only call update interest only when update balance is called
		transactionCard[0].update('interest', interest, session)
		transactionCard[0].update('balance', changeInBalance, session)

	def getInterest( username, fromDate, toDate, session ):
		user = session.query(User).filter_by(username=username).all()
		if len(user) > 1:
			raise 'duplicate usernames'

		transactionCard = session.query(CreditCard).filter_by(accountNumber=user[0].creditCardNumber).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'

		return Util.calculateInterest( transactionCard[0], fromDate, toDate )

	def calculateInterest( transactionCard, fromDate, toDate ):
		if (transactionCard.balance <= 0):
			return 0
		dayRange = (toDate - fromDate).days
		return (transactionCard.balance * (transactionCard.apr/365) * dayRange )

	def cardIsOverDue(transactionCard, currTransactionDate):
		if (transactionCard.dueDate < currTransactionDate ):
			return true
		else:
			return false

	# def calculateInterest(name, session):
	# 	username = session.query(User).filter_by(username=name).all()
	# 	username.creditCardNumber()

	# 	while ( overDue(creditCard) ):
	# 		pastDueDate = creditCard.dueDate()
	# 		updateBalance( pastDueDate, 0, TransactionType.dueInterest )
	# 		updateDueDate( pastDueDate + timedelta(days=30) )
	# 	updateInterest( pastDueDate, datetime.now().date() )
	# 	return creditCard.getInterest()


	# u1 = User("mg mg", "test")
	# card1 = CreditCard( 35, 1000 )
	# u1.addCard( AccountType.credit, card1 )

	# u2 = User("aa", "test")
	# card2 = CreditCard( 35, 300 )
	# u2.addCard( AccountType.credit, card2 )

	# addTransaction(u1, u2, 300)
	# print(card1.getBalance(), card2.getBalance() )