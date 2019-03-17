from abc import ABC, abstractmethod

class DBActions():

	@abstractmethod
	def __init__(self):
		pass

	@abstractmethod
	def __repr__(self):
		pass

	@abstractmethod
	def create(self, session):
		session.add(self)
		session.flush()

	@abstractmethod
	def update(self, fieldName, newValue, session):
		pass

	def delete(queryObj, session):
		session.delete(queryObj)
		session.flush()
		