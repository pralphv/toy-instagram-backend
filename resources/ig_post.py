from datetime import datetime
import os

from flask import request
from flask_restful import Resource
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from model import db, IgPost, IgPostSchema
from resources import utils

from config import IMG_PATH


IGPOSTS_SCHEMA = IgPostSchema(many=True)
IGPOST_SCHEMA = IgPostSchema()

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def rename_filename(filename: str) -> str:
    """
    Renames image name to the number
    of files in IMG_PATH.
    Guarantee all filenames are unique
    """
    return '{}.{}'.format(len(os.listdir(IMG_PATH)), filename.split('.')[-1])


class IgPostResource(Resource):
    def delete(self) -> tuple:
        json_data = utils.get_json_data()
        IgPost.query.filter(
            IgPost.img_path == 'static/img/{}'.format(json_data['filename'])
        ).delete()
        db.session.commit()
        return {'status': 'success'}, 200

    def get(self) -> tuple:
        query = IgPost.query.order_by(desc(IgPost.update_date)).all()
        query = IGPOSTS_SCHEMA.dump(query).data
        return {'status': 'success', 'data': query}, 200

    def post(self) -> tuple:
        """
        The uploaded file is saved as
        a path in the database. The file is
        saved in IMG_PATH, named by the number
        of files in IMG_PATH to guarantee unique
        name.
        If 'test' is in the body of request,
        the file will not upload to IMG_PATH
        for testing purposes.
        """
        if 'file' not in request.files:
            return {'status': 'fail', 'error': 'no file'}, 400
        token = request.headers.get('Authorization').replace('Bearer ', '')
        decoded = utils.TokenEncoder.decode_auth_token(token)
        if 'Invalid token' in decoded:
            return {'status': 'fail', 'error': 'Invalid token'}, 400
        username = decoded['name']
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            return {'status': 'fail', 'error': 'wrong file extension'}, 400
        # filename = rename_filename(filename)
        filename_path = os.path.join(IMG_PATH, filename)
        if 'test' not in request.form:  # for unittest
            file.save(filename_path)
        instagram_post = IgPost(
            author=username,
            description=request.form['description'],
            update_date=datetime.now(),
            img_path=filename_path,
        )
        db.session.add(instagram_post)
        db.session.commit()
        result = IGPOST_SCHEMA.dump(instagram_post).data
        return {"status": 'success', 'data': result}, 201

