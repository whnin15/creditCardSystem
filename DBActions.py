from abc import ABC, abstractmethod

class DBActions():

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def __repr__(self):
		pass

	def create(self, session):
		session.add(self)
		session.commit()

	@abstractmethod
	def update(self, fieldName, newValue, session):
		pass

	def delete(queryObj, session):
		session.delete(queryObj)
		session.commit()
		