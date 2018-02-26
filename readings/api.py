# Following Method Based Dispatching
# For RESTful API's, it helps execute different functions for each HTTP method
# Method Based Dispatching info: http://flask.pocoo.org/docs/0.12/views/
from flask.views import MethodView
from flask import jsonify, request, abort
from readings.models import Readings

class ReadingsAPI(MethodView):

	def get(self, balloon_id, altitude):
		
		if(request.args.get('page')):
			page = int(request.args.get('page')) or 1
			readings = Readings().get_readings(balloon_id, altitude, page)
		else:
			readings = Readings().get_readings(balloon_id, altitude, None)

		if readings:
			response = {
				"result": "ok",
				"readings": readings
			}
			return jsonify(response), 200 # Successfully found reading(s)
		
		else:
			return jsonify({}), 404 # reading data not found

	def post(self):
		if (not request.json or (not 'balloon_id' in request.json and 
								 not 'altitude' in request.json and
								 not 'humidity' in request.json and
								 not 'pressure' in request.json and
								 not 'reading_time' in request.json and
								 not 'temperature' in request.json)):
			abort(400)

		balloon_id = request.json['balloon_id']
		altitude = request.json['altitude']
		humidity = request.json['humidity']
		pressure = request.json['pressure']
		reading_time = request.json['reading_time']
		temperature = request.json['temperature']

		readings = Readings().add_readings(balloon_id, altitude, humidity, pressure, reading_time, temperature)

		if(readings):
			response = {
				"result": "ok",
				"readings": readings
			}
			return jsonify(response), 201
		else:
			return jsonify({"error": "Unable to add readings"}), 400

	def delete(self, reading_id):
		deleteReading = Readings().delete_readings(reading_id)
		if(deleteReading):
			return jsonify({"result": "ok"}), 204
		return jsonify({"error": "Delete reading unsuccessful"}), 404
