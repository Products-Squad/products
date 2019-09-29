
from flask import Flask
# Create Flask application
app = Flask(__name__)

# Import the rutes After the Flask app is created
from service import service

# Set up logging for production
# service.initialize_logging()

#app.logger.info('Service inititalized!')

if __name__ == '__main__':
    app.run()