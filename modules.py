from flask import Blueprint
from flask_restful import Api
from resources.ig_post import IgPostResource
from resources.register import RegisterResource
from resources.login import LoginResource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(IgPostResource, '/igpost')
api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
