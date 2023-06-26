from flask import Flask
import sys
import logging

from internal.api import API
from internal.views import Views

from storage.minio import MinioConnector
from storage.sql import SQLConnector

from config.config import Config


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
)

# load app configs
cfg = Config()

error, flag = cfg.load()
if flag:  # if error occurs
    logging.error(error)
    sys.exit(-1)

# open connection to storages
sqlC = SQLConnector(host=cfg.sql['host'])

minioC = MinioConnector(
    host=cfg.minio['host'],
    access=cfg.minio['access'],
    secret=cfg.minio['secret'],
    secure=False,
)

errorC, flag = minioC.ping()
if flag:
    logging.error(error)
    sys.exit(-2)


# create a new flask application
app = Flask(__name__,
            static_url_path='/',
            static_folder='web/static',
            template_folder='web/template')

# register blueprints
app.register_blueprint(API(sqlC, minioC).get_blue_print())
app.register_blueprint(Views().get_blue_print())

logging.info(f"application started on port: {cfg.port}")

if __name__ == "__main__":
    app.run("127.0.0.1", cfg.port, debug=cfg.debug)
