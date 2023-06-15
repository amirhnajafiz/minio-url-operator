from flask import Blueprint
import sqlite3
import minio

from .handler.handler import Handler


class API(object):
    """API manages the backend rest api"""

    def __init__(self, database: sqlite3.Connection, minio_connection: minio.Minio):
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
