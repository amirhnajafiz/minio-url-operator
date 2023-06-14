from flask import Blueprint

from .handler import Handler


class API(object):
    def __init__(self):
        # create a blueprint for application apis
        self.blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")

        # create a new handler
        api = Handler()

        @self.blueprint.route("/objects", methods=['GET'])
        def get_objects():
            api.get_objects()

    def get_blue_print(self):
        return self.blueprint
