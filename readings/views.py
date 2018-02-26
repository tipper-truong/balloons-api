from flask import Blueprint
from readings.api import ReadingsAPI

readings_app = Blueprint('readings_app', __name__)
readings_view = ReadingsAPI.as_view('reading_api')

# POST: /readings/add/--> Adds a new reading
readings_app.add_url_rule('/readings/add/',
						view_func=readings_view,
						methods=['POST',])

# DELETE: /readings/delete/<reading_id> --> Deletes reading based on id
readings_app.add_url_rule('/readings/delete/<reading_id>/',
						view_func=readings_view,
						methods=['DELETE',])

# GET: /readings/<balloon_id>/ --> Get a list of all readings for a single balloon
readings_app.add_url_rule('/readings/<balloon_id>/',
						defaults={'altitude': None},
						view_func=readings_view,
						methods=['GET',])

# GET: /readings/<balloon_id>/<altitude>/ --> Get a single reading for a balloon and altitude
readings_app.add_url_rule('/readings/<balloon_id>/<altitude>/',
						view_func=readings_view,
						methods=['GET',])