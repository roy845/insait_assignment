from http import HTTPStatus
from flask_restx import Namespace,Resource

health_api = Namespace('health', description='Health')


@health_api.route('/')
class Health(Resource):
    @health_api.doc(
        responses={HTTPStatus.OK: 'Return status about server health'})
    def get(self):                     
        return {"ok":True}