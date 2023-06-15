from flask import Flask

from http.api import API
from http.views import Views

from storage.minio import MinioConnector
from storage.sql import SQLConnector

from config.config import Config


# load app configs
cfg = Config()
cfg.load()

# open connection to storages
sqlC = SQLConnector(host=cfg.sql['host'])
minioC = MinioConnector(
    host=cfg.minio['host'],
    access=cfg.minio['access'],
    secret=cfg.minio['secret']
)

# create a new flask application
app = Flask(__name__)
app.register_blueprint(API().get_blue_print())
app.register_blueprint(Views().get_blue_print())


if __name__ == "__main__":
    app.run("127.0.0.1", cfg.port, debug=cfg.debug)
