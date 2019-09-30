from flask import Flask

# Create Flask application
app = Flask(__name__)

# Import the routes After the Flask app is created
from service import service, logger

# Set up logging for production
logger.initialize_logging()
app.logger.info('  P R O D U C T   S E R V I C E   R U N N I N G  '.center(70, '*'))

if __name__ == '__main__':
    app.run()