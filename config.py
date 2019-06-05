import os


basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
os.environ['DATABASE_URL'] = "postgres://vvufmiexzaibyf:a9864ec63ba51b5dce47b5dab51825b273de1b03f691d4f18077649737840337@ec2-107-20-155-148.compute-1.amazonaws.com:5432/df22gt2tpb3hvl"
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SALT = 'salt'
TOKENKEY = 'token'
IMG_PATH = r'static/img/'
SECRET_KEY = 'super secret key'
CORS_HEADERS = 'Content-Type'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False

