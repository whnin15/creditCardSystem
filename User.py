from DBActions import DBActions

class User(DBActions):

	def __init__(self, username, password, fullname, email):
		# self.user_id = user_id
		self.username = username
		self.password = password
		self.fullname = fullname
		self.email = email
		self.streetAddress = ""
		self.city = ""
		self.state = ""
		self.zipCode = 00000
		self.preferredPhoneNumber = 0
		self.phoneNumber1 = 0
		self.creditCardNumber = 1

	def __repr__(self):
		return "<User(username='%s', fullname='%s', email='%s', address='%s','%s','%s','%d', preferredPhone='%d', creditCard='%d')>" % (self.username, self.fullname, self.email, self.streetAddress, self.city, self.state, self.zipCode, self.preferredPhoneNumber, self.creditCardNumber)

	def update(self, fieldName, newVal, session):
		if fieldName=='username':
			self.username = newVal
		elif fieldName=='password':
			print('updated')
			self.password = newVal
		elif fieldName=='fullname':
			self.fullname = newVal
		elif fieldName=='email':
			self.email = newVal
		elif fieldName=='streetAddress':
			self.streetAddress = newVal
		elif fieldName=='city':
			self.city = newVal
		elif fieldName=='state':
			self.state = newVal
		elif fieldName=='zipCode':
			self.zipCode = newVal
		elif fieldName=='preferredPhoneNumber':
			self.preferredPhoneNumber = newVal
		elif fieldName=='phoneNumber1':
			self.phoneNumber1 = newVal
		elif fieldName=='creditCardNumber':
			self.creditCardNumber = newVal
		else:
			raise 'User.py: getByFieldName - not valid field'

		session.commit()