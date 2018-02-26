from flask import Flask

def create_app(**config_overrides):
	app = Flask(__name__)

	# Load config
	app.config.from_pyfile('settings.py')

	# Apply overrides for tests
	app.config.update(config_overrides)

	# Import blueprints
	from home.views import home_app
	from balloon.views import balloon_app
	from readings.views import readings_app

	# Register blueprints
	app.register_blueprint(home_app)
	app.register_blueprint(balloon_app)
	app.register_blueprint(readings_app)

	return app