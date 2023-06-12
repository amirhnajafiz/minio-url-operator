from flask import Flask

from http.api import api_blueprint
from http.views import views_blueprint
from config.config import Config


# load app configs
cfg = Config()
cfg.load()


# create a new flask application
app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(views_blueprint)


if __name__ == "__main__":
    app.run("127.0.0.1", cfg.port, debug=cfg.debug)
