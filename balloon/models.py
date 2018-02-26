import sqlite3 as db
from flask import Flask,jsonify,json

# Accesses sqlite3.db 
# Responsible for managing data from balloon table
class Balloon:

	def __init__(self):
		self.table = "balloons"
		self.connect = db.connect('sqlite3.db')
		self.connect.row_factory = db.Row

	# Retrieves list of balloons or a specific ballon based on flight number
	def get_balloons(self, flight_number):
		balloons = []

		if flight_number:
			sql = 'SELECT * FROM {} WHERE {} = {}'.format(self.table, "flight_number", flight_number)
		else:
			sql = 'SELECT * FROM {}'.format(self.table)

		try: 
			balloonCursor = self.connect.execute(sql)

			# Get the name of columns
			columns = [column[0] for column in balloonCursor.description]
			
			# Add row from db to dictionary with column name and row value
			for balloon in balloonCursor.fetchall():
				balloon_dict = dict(zip(columns, balloon))
				balloon_dict['links'] = [{
					"rel": "self",
					"href": "/balloons/" + str(balloon['flight_number'])
				}]

				balloons.append(balloon_dict)

		except db.Error as error:
			return {} 

		self.connect.close()
		return balloons 

	# Update a balloon information based on id
	def update_balloon(self, flight_number, location, technician, recovered, balloon_id):
		updatedBalloon = []

		sql = 'UPDATE {} SET flight_number={}, location={}, technician={}, recovered={} WHERE id={}'.format(self.table, flight_number, "\"%s\"" % location, "\"%s\"" % technician, recovered, balloon_id)
		try:
			self.connect.execute(sql)
			self.connect.commit() # Commit update changes

			# Get updated row
			sql = 'SELECT * FROM {} WHERE {} = {}'.format(self.table, "id", balloon_id)
			balloonCursor = self.connect.execute(sql)

			# Get the name of columns 
			columns = [column[0] for column in balloonCursor.description]

			# Update row from db to dictionary with column name and row value
			balloons = balloonCursor.fetchall()
			for balloon in balloons:
				balloon_dict = dict(zip(columns, balloon))
				balloon_dict['links'] = [{
					"rel": "self",
					"href": "/balloons/" + str(flight_number)
				}]

				updatedBalloon.append(balloon_dict)

		except db.Error as error:
			print (error)
			return {} 

		self.connect.close()
		return updatedBalloon 



