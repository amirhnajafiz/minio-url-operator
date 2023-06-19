from flask import Blueprint, request, jsonify

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
            """get objects metadata

            :return: list of objects of a bucket with prefix
            """
            bucket = request.args.get("bucket", "")
            if bucket == "":
                return "Bucket cannot be empty", 400

            return jsonify(api.get_objects_metadata(bucket, request.args.get("prefix", "")))

        @self.blueprint.route("/objects/<bucket>/<key>", methods=['GET'])
        def get_object_url(bucket, key):
            """get object url

            :param bucket: object bucket
            :param key: object key
            :return: object url
            """
            return {
                'address': api.get_object_url(bucket, key)
            }

    def get_blue_print(self) -> Blueprint:
        """get api blueprint

        :return: flask blueprint
        """
        return self.blueprint
