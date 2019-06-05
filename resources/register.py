from flask_restful import Resource
from passlib.hash import sha256_crypt

from model import db, User, UserSchema
from config import SALT
from resources import utils

USERS_SCHEMA = UserSchema(many=True)
USER_SCHEMA = UserSchema()


class RegisterResource(Resource):
    @staticmethod
    def check_user_in_database(username: str) -> bool:
        response = User.query.filter(User.username == username).first()
        return bool(response)

    @staticmethod
    def check_same_password(password: str, retype: str) -> bool:
        return password == retype

    def post(self) -> tuple:
        """
        Password is saved as hashed.
        sha256 + salt is used.
        """
        json_data = utils.get_json_data()
        data, errors = USER_SCHEMA.load(json_data)
        if errors:
            return errors, 422
        user_in_database = self.check_user_in_database(json_data['username'])
        if user_in_database:
            return {"status": 'fail', 'error': 'User already exists'}, 400
        if not self.check_same_password(
                json_data['password'],
                json_data['retype_password']
        ):
            return {"status": 'fail', 'error': 'Password not same'}, 400

        new_user = User(
            username=json_data['username'],
            password=sha256_crypt.hash(SALT + json_data['password']),
        )
        db.session.add(new_user)
        db.session.commit()
        result = USER_SCHEMA.dump(new_user).data
        return {"status": 'success', 'data': result}, 201

    def delete(self) -> tuple:
        json_data = utils.get_json_data()
        User.query.filter(
            User.username == json_data['username']
        ).delete()
        db.session.commit()
        return {'status': 'success'}, 200
