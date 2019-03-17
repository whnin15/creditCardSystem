from datetime import datetime
from datetime import timedelta
from CreditCard import AccountType
from CreditCard import TransactionType
from CreditCard import CreditCard
from User import User

class Util:

	# def addTransaction(payer, payee, amount):
	# 	# create a transaction ID

	# 	# what if more than one card per account
	# 	transactionDate = datetime.now().date()

	# 	CardToWithdraw = payer.getCard(AccountType.credit)
	# 	CardToDeposit = payee.getCard(AccountType.credit)

	# 	CardToWithdraw.updateBalance(transactionDate, amount, TransactionType.withdrawal)
	# 	CardToDeposit.updateBalance(transactionDate, amount, TransactionType.deposit)
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