from flask import Blueprint, request, jsonify, redirect

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

            objects = api.get_objects_metadata(bucket, request.args.get("prefix", ""))

            return jsonify([item.object_name for item in objects])

        @self.blueprint.route("/objects/<address>", methods=['GET'])
        def redirect_address(address):
            """redirect to shared storage if enabled

            :param address: object address in our system
            """
            url = api.get_object_url_by_address(address)
            if len(url) == 0:
                return "Address does not exists", 404

            return redirect(url)

        @self.blueprint.route("/objects/<object_id>", methods=['POST'])
        def update_object(object_id):
            """update object enable or disable

            :param object_id: object id
            """
            status = request.args.get("status", 1)

            api.update_object(object_id, status)

            return "OK", 200

        @self.blueprint.route("/objects/<bucket>/<key>", methods=['GET'])
        def get_object_address(bucket, key):
            """get object url

            :param bucket: object bucket
            :param key: object key
            :return: object url
            """
            return {
                'address': api.get_object_address(bucket, key)
            }

    def get_blue_print(self) -> Blueprint:
        """get api blueprint

        :return: flask blueprint
        """
        return self.blueprint
