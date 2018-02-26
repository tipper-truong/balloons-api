from flask import Blueprint
from balloon.api import BalloonAPI

balloon_app = Blueprint('balloon_app', __name__)

balloon_view = BalloonAPI.as_view('balloon_api')
 
# GET: /balloons/ --> gets the list of balloons
balloon_app.add_url_rule('/balloons/', 
					defaults={'flight_number': None},
                 	view_func=balloon_view, 
                 	methods=['GET',])

# GET: /balloons/<flight_number>/ -->  gets specific balloon based on flight_number
balloon_app.add_url_rule('/balloons/<flight_number>/', 
					view_func=balloon_view,
                 	methods=['GET',])

# PUT: /balloons/<balloon_id>/ --> updates balloon data based on given balloon id
balloon_app.add_url_rule('/balloons/<balloon_id>/', 
					view_func=balloon_view,
                 	methods=['PUT',])