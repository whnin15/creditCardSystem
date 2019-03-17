from datetime import datetime
from datetime import timedelta
from CreditCard import AccountType
from User import User
from CreditCard import CreditCard

class Util:

	def updateBalance(username, changeInBalance, session):
		user = session.query(User).filter_by(username=username).all()
		if len(user) > 1:
			raise 'duplicate usernames'

		transactionCard = session.query(CreditCard).filter_by(accountNumber=user[0].creditCardNumber).all()
		if len(transactionCard) > 1:
			raise 'duplicate credit card account number'
		transactionCard[0].update('balance', changeInBalance, session)


	def cardIsOverDue(card, session):
		creditCard = session.query(CreditCard).filter_by(cardNumber=card).all()
		if (creditCard.dueDate < datetime.now().date() ):
			return true
		else:
			return false

	def calculateInterest(name, session):
		username = session.query(User).filter_by(username=name).all()
		username.creditCardNumber()

		while ( overDue(creditCard) ):
			pastDueDate = creditCard.dueDate()
			updateBalance( pastDueDate, 0, TransactionType.dueInterest )
			updateDueDate( pastDueDate + timedelta(days=30) )
		updateInterest( pastDueDate, datetime.now().date() )
		return creditCard.getInterest()


	# u1 = User("mg mg", "test")
	# card1 = CreditCard( 35, 1000 )
	# u1.addCard( AccountType.credit, card1 )

	# u2 = User("aa", "test")
	# card2 = CreditCard( 35, 300 )
	# u2.addCard( AccountType.credit, card2 )

	# addTransaction(u1, u2, 300)
	# print(card1.getBalance(), card2.getBalance() )