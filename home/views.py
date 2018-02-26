from flask import Blueprint
from flask import send_file

home_app = Blueprint('home_app', __name__)

@home_app.route('/')
def home():
	try:
		return send_file('home/test_api_endpoints.pdf', attachment_filename='test_api_endpoints.pdf')
	except Exception as e:
		return str(e)