# Following Method Based Dispatching
# For RESTful API's, it helps execute different functions for each HTTP method
# Method Based Dispatching info: http://flask.pocoo.org/docs/0.12/views/
from flask.views import MethodView
from flask import jsonify, request, abort
from balloon.models import Balloon
from geopy.geocoders import Nominatim

class BalloonAPI(MethodView):

	def get(self, flight_number):
		if flight_number: # Get specific balloon item based on id
			balloon = Balloon().get_balloons(flight_number)
			
			if balloon: 
				response = {
					"result": "ok",
					"balloon": balloon
				}
				return jsonify(response), 200 # Sucessfully found balloon
			else:
				return jsonify({"error": "Cannot find balloon with flight number: " + flight_number}), 404  # Failed, unable to find balloon

		else: # Get the list of balloons
			balloons = Balloon().get_balloons(None)
			
			if balloons: 

				response = {
					"result": "ok",
					"balloons": balloons
				}
				return jsonify(response), 200 # Sucessfully found balloon

	def put(self, balloon_id):
		if (not request.json or (not 'flight_number' in request.json and 
								 not 'location' in request.json and
								 not 'technician' in request.json and
								 not 'recovered' in request.json)):
			abort(400)

		# Edge cases 
		if not isinstance(request.json['flight_number'], int):
			return jsonify({"error": "Invalid flight number"}), 400
		if int(request.json['recovered']) > 1 or int(request.json['recovered']) < 0:
			return jsonify({"error": "Invalid statement"})
		
		geolocator = Nominatim()
		location = geolocator.geocode(request.json['location'], timeout=10, language="en")
		if location is None:
			return jsonify({"error": "Invalid location"})

		# Update balloon data 
		balloon = Balloon().update_balloon(request.json['flight_number'], 
										   location, 
										   request.json['technician'], 
										   request.json['recovered'], 
										   balloon_id)

		if balloon:
			response = {
				"result": "ok",
				"balloon": balloon
			}
			return jsonify(response), 200
		else:
			return jsonify({}), 404 # balloon data not found


