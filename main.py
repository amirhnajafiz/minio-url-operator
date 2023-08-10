from flask import Flask

import sys
import logging

from internal.api import API
from internal.views import Views

# storage connections
from internal.storage.minio import MinioConnector
from internal.storage.mysql import MySQL

# config module
from internal.config.config import Config


# set logging module
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
# mysql
dbConnection = MySQL(
    host=cfg.mysql['host'],
    port=cfg.mysql['port'],
    user=cfg.mysql['user'],
    password=cfg.mysql['pass'],
    database=cfg.mysql['name']
)

# minio
minioConnection = MinioConnector(
    host=cfg.minio['host'],
    access=cfg.minio['access'],
    secret=cfg.minio['secret'],
    secure=False,
)


# create a new flask application
app = Flask(__name__,
            static_url_path='/',
            static_folder='web/static',
            template_folder='web/template')

# register blueprints
app.register_blueprint(API(dbConnection, minioConnection, f'{cfg.host}:{cfg.port}', cfg.private).get_blue_print())
app.register_blueprint(Views().get_blue_print())


if __name__ == "__main__":
    # check mysql connection
    if not dbConnection.ping():
        logging.error("mysql connection failed!")
        sys.exit(-2)

    # check minio connection
    errorM, flag = minioConnection.ping()
    if flag:
        logging.error(errorM)
        sys.exit(-3)

    logging.info(f"operator started on port: {cfg.port} ...")
    app.run("127.0.0.1", cfg.port, debug=cfg.debug)
