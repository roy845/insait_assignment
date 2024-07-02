from flask import Flask
import logging
from flask_restx import Api
from config import settings
from routes.question import question_api as question_namespace
from routes.health import health_api as health_namespace
from database import db
from utils.create_database import create_database
from flask_cors import CORS

logger = logging.getLogger(__name__)

def create_app(testing: bool = False):
    logger.info("Initializing Flask app.....")

    DATABASE_URL: str = settings.database_test_url if testing else settings.database_prod_url

    database_url = DATABASE_URL.rsplit('/', 1)[0]
    database_name = DATABASE_URL.rsplit('/', 1)[-1]

    create_database(database_url, database_name)

    app = Flask(__name__,static_folder='build', static_url_path='')
    
    app.config['TESTING'] = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_test_url if testing else settings.database_prod_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.sqlalchemy_track_modifications

    api = Api(app, version='1.0', prefix='/api', title='Flask Questions Answers API', description='A simple Flask Questions API', doc='/api/docs/')
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    logger.info('Flask application initialized.')

    db.init_app(app)
    with app.app_context():
        db.create_all()

    logger.info('Adding namespaces to the API...')
    api.add_namespace(health_namespace, path='/health')
    api.add_namespace(question_namespace, path='/question')
    logger.info('Namespaces added to the API.')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
