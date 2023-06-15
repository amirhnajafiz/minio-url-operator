from flask import Blueprint

from .handler import Handler


class API(object):
    """API manages the backend rest api"""

    def __init__(self, database, minio):
        # create a blueprint for application apis
        self.blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")

        # create a new handler
        api = Handler(database, minio)

        @self.blueprint.route("/objects", methods=['GET'])
        def get_objects():
            api.get_objects()

    def get_blue_print(self):
        return self.blueprint
