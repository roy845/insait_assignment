import logging
from flask_app import create_app


logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('Starting the Flask application...')

    app = create_app()

    app.run(host="0.0.0.0", debug=True)
    
    logger.info('Flask application has stopped.')
