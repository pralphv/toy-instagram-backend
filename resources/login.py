from flask_restful import Resource
from passlib.hash import sha256_crypt

from model import User, UserSchema
from config import SALT
from resources import utils


USERS_SCHEMA = UserSchema(many=True)
USER_SCHEMA = UserSchema()


class LoginResource(Resource):
    def post(self) -> tuple:
        json_data = utils.get_json_data()
        data, errors = USER_SCHEMA.load(json_data)
        if errors:
            return errors, 422
        username = json_data['username']
        password = SALT + json_data['password']

        user_details = User.query.filter(User.username == username).first()
        if user_details is None:
            return {"status": 'failed', 'error': 'user does not exist'}, 400

        correct_password = sha256_crypt.verify(password, user_details.password)

        if user_details.username == username and correct_password:
            response = utils.TokenEncoder.encode_auth_token(
                username,
                user_details.id
            )
        else:
            return {'status': 'failed', 'error': 'wrong password'}, 400
        return {"status": 'success', 'token': response['token']}, 201

