import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("MY_FLASK_SECRET")
    SECRET_KEY = "do_not_ask"
    SECURITY_PASSWORD_SALT = "do_not_ask_me"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://djose1164:Kirito08.@localhost/cara"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://djose1164:Kirito08.@localhost/cara"
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://djose1164:Kirito08.@localhost/cara"
    SQLALCHEMY_ECHO = False
