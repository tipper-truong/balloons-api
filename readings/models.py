import sqlite3 as db
import math
from flask import Flask, jsonify, json

# Accesses sqlite3.db
# Responsible for managing data from readings
class Readings:

	def __init__(self):
		self.balloon_table = "balloons"
		self.readings_table = "readings"
		self.connect = db.connect('sqlite3.db')
		self.connect.row_factory = db.Row

	def get_readings(self, balloon_id, altitude, page):

		readings = [] 
		# Get a list of all readings for a single balloon
		# Example: select * from readings where balloon_id in (select id from balloons where id = 3);
		
		if balloon_id and not altitude:
			# Pagination, showing 10 items at a time
			# Example: http://localhost/readings/1/?page=1
			if page:
				items_per_page = 10 # how many to display per page
				start_index = (page - 1) * items_per_page # where should the query start from
				sql = 'SELECT * FROM {} WHERE {} IN {}SELECT {} FROM {} WHERE {} = {}{} LIMIT {}, {}'.format(self.readings_table, 'balloon_id', '(', 'id', self.balloon_table, 'id', balloon_id, ')', start_index, items_per_page)
			# Get a list of all readings for a single balloon
			# Example: select * from readings where balloon_id in (select id from balloons where id = 3);
			else: 
				sql = 'SELECT * FROM {} WHERE {} IN {}SELECT {} FROM {} WHERE {} = {}{}'.format(self.readings_table, 'balloon_id', '(', 'id', self.balloon_table, 'id', balloon_id, ')')
		elif balloon_id and altitude:
			# Get a single reading for a balloon and altitude
			# Example: select * from readings where balloon_id=3 and altitude=(select min(altitude) from readings where altitude >= 100 union select max(altitude) from readings where altitude <= 100 limit 1);
			sql = 'SELECT * FROM {} WHERE {}={} AND {}={}SELECT min({}) FROM {} WHERE {} >= {} UNION SELECT max({}) FROM {} WHERE {} <= {} LIMIT 1{}'.format('readings', 'balloon_id', balloon_id, 'altitude', '(', 'altitude', 'readings', 'altitude', altitude, 'altitude', 'readings', 'altitude', altitude, ')')

		try:
			readingsCursor = self.connect.execute(sql)

			# Get the name of columns
			columns = self.get_column_names(readingsCursor)
			
			# Add row from db to dictionary with column name and row value
			for reading in readingsCursor.fetchall():
				readings_dict = dict(zip(columns, reading))
				if page:
					readings_dict['links'] = [{
						"rel": "self",
						"href": "/readings/" + str(balloon_id) + "/" + "?page=" + str(page)
					}]
				else:
					readings_dict['links'] = [{
						"rel": "self",
						"href": "/readings/" + str(balloon_id) + "/" + str(reading[3])
					}]
				readings.append(readings_dict)

		except db.Error as error:
			print(error)


		self.connect.close()
		return readings

	def add_readings(self, balloon_id, altitude, humidity, pressure, reading_time, temperature):
		readings = []
		sql = 'INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ({}, {}, {}, {}, {}, {})'.format(self.readings_table, 'balloon_id', 'altitude', 'humidity', 'pressure', 'reading_time', 'temperature', balloon_id, altitude, humidity, pressure, reading_time, temperature)

		try:
		
			self.connect.execute(sql)
			self.connect.commit() # Commit adding new readings data
			
			# Get the inserted data id
			last_row_sql = 'SELECT max({}) FROM {}'.format('id', self.readings_table)
			row = self.connect.execute(last_row_sql).fetchone()
			prev_id = row[0]

			# Get the new reading data that just got added
			new_readings_sql = 'SELECT * FROM {} WHERE {}={}'.format(self.readings_table, 'id', prev_id)

			readingsCursor = self.connect.execute(new_readings_sql)

			# Get the name of columns 
			columns = self.get_column_names(readingsCursor)

			for reading in readingsCursor.fetchall():
				readings_dict = dict(zip(columns, reading))
				readings.append(readings_dict)

		except db.Error as error:
			print(error)
		self.connect.close()
		return readings
	

	def delete_readings(self, reading_id):
		if id:
			try: 
				sql = 'DELETE FROM {} WHERE {}={}'.format(self.readings_table, 'id', reading_id)
				self.connect.execute(sql)
				self.connect.commit()
				self.connect.close()
				return True
			except db.Error as error:
				return False
		
	# Helper function to get the column names
	def get_column_names(self, cursor):
		columns = []
		for column in cursor.description:
			if "min" in column[0] or "max" in column[0]:
				column.append(column[0][column[0].find("(")+1:column[0].find(")")])
			columns.append(column[0])
		return columns

