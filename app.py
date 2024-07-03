from http import HTTPStatus
import logging
from pydantic import ValidationError
from flask_app import create_app
import os
from flask import send_from_directory


logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('Starting the Flask application...')

    app = create_app()

    @app.route('/')
    def index():
        path = os.path.join(os.getcwd(), 'build')
        return send_from_directory(directory=path, path='index.html')

    @app.route('/static/<folder>/<file>')
    def serve_static(folder, file):
        path = os.path.join('build', 'static', folder, file)
        return send_from_directory(directory=os.path.dirname(path), path=os.path.basename(path))

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, ValidationError):
            return ({'errors': e.errors()}), HTTPStatus.BAD_REQUEST
       
        return ({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')


    app.run(host="0.0.0.0", debug=True)

    logger.info('Flask application has stopped.')
