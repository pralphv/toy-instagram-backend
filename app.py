from flask_cors import CORS
from flask import Flask

from config import SECRET_KEY


def create_app(config_filename: str) -> Flask:
    """
    :param config_filename: {'DevelopmentConfig', 'TestingConfig'}
    :return: app
    """
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(config_filename)
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SECRET_KEY'] = SECRET_KEY
    from modules import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from model import db
    db.init_app(app)

    return app


app = create_app('config.DevelopmentConfig')

@app.route("/")
def hello():
    return "Hello World!"
if __name__ == '__main__':
    app.run(debug=True)
