import datetime

from flask import request
import jwt

try:
    from config import TOKENKEY
except ModuleNotFoundError:
    from ..config import TOKENKEY


def get_json_data() -> tuple:
    json_data = request.get_json(force=True)
    if not json_data:
        return {'message': 'No input data provided'}, 400
    else:
        return json_data


class TokenEncoder(object):
    @staticmethod
    def encode_auth_token(username: any, id: any) -> dict:
        payload = {
            'exp': datetime.datetime.utcnow()
                   + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'name': username,
            'sub': id,
        }
        token = jwt.encode(payload, TOKENKEY, algorithm='HS256')
        return {'status': 'success', 'token': token.decode('utf-8')}

    @staticmethod
    def decode_auth_token(auth_token: str) -> str:
        try:
            payload = jwt.decode(auth_token, TOKENKEY, algorithms='HS256')
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

