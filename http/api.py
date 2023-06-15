from flask import Blueprint

from storage.sql import SQLConnector
from storage.minio import MinioConnector
from .handler.handler import Handler


class API(object):
    """API manages the backend rest api"""

    def __init__(self, database: SQLConnector, minio_connection: MinioConnector):
        # create a blueprint for application apis
        self.blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")

        # create a new handler
        api = Handler(database, minio_connection)

        @self.blueprint.route("/objects", methods=['GET'])
        def get_objects():
            api.get_objects()

    def get_blue_print(self) -> Blueprint:
        """get api blueprint

        :return: flask blueprint
        """
        return self.blueprint
