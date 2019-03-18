from abc import ABC, abstractmethod

#abstract class with genearl database actions
class DBActions():

	# insert row
	@abstractmethod
	def create(self, session):
		session.add(self)
		session.flush()

	# update field value in the row
	@abstractmethod
	def update(self, fieldName, newValue, session):
		pass

	# delete row
	def delete(queryObj, session):
		session.delete(queryObj)
		session.flush()
		