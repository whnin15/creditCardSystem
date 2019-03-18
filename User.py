from DBActions import DBActions

# User class (mapped to users table)
class User(DBActions):

	#constructor
	def __init__(self, username, password, fullname, email, streetAddress="", city="", state="", zipCode=0, preferredPhoneNumber=0, phoneNumber1=0):
		self.username = username
		self.password = password
		self.fullname = fullname
		self.email = email
		self.streetAddress = streetAddress
		self.city = city
		self.state = state
		self.zipCode = zipCode
		self.preferredPhoneNumber = preferredPhoneNumber
		self.phoneNumber1 = phoneNumber1

	#representation of a user row
	def __repr__(self):
		return "<User(username='{}', fullname='{}', email='{}', address='{}','{}','{}','{}', preferredPhone='{}')>".format(self.username, self.fullname, self.email, self.streetAddress, self.city, self.state, self.zipCode, self.preferredPhoneNumber)

	#updating the column value in the field for the user object
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
		else:
			raise Exception('User.py: update failed - not valid field:', fieldName)

		session.flush()