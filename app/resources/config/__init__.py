from os import environ, path, curdir

ROOT_DIR = path.abspath(curdir)


class AppConfig(object):
    DATABASE_SQL_NAME = environ.get("DATABASE_SQL_NAME")
    DATABASE_HOST = environ.get("DATABASE_HOST")
    DATABASE_USERNAME = environ.get("DATABASE_USERNAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_PORT = environ.get("DATABASE_PORT")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    SQLALCHEMY_DATABASE_URI = '{postgresql}://{user_name}:{password}@{host}:{port}/{database_name}'.format(
        postgresql=DATABASE_SQL_NAME,
        user_name=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        database_name=DATABASE_NAME
    )
    ROOT_DIR = ROOT_DIR
    APP_URL = environ.get("APP_URL")
    RABBITMQ_HOST = environ.get("RABBITMQ_HOST")
    RABBITMQ_QUEUE = environ.get("RABBITMQ_QUEUE")
    RABBITMQ_EXCHANGE = environ.get("RABBITMQ_EXCHANGE")
    RABBITMQ_ROUTINGKEY = environ.get("RABBITMQ_ROUTINGKEY")
    THREADS = environ.get("THREADS")
