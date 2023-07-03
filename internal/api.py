import logging
from flask import Blueprint, request, jsonify, redirect

from storage.sql import SQLConnector
from storage.minio import MinioConnector
from .handler.handler import Handler


class API(object):
    """API manages the backend rest api"""

    def __init__(self, database: SQLConnector, minio_connection: MinioConnector, host="", private=False):
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

            return jsonify(api.get_objects_metadata(bucket, request.args.get("prefix", ""))), 200

        @self.blueprint.route("/objects/<address>", methods=['GET'])
        def redirect_address(address):
            """redirect to shared storage if enabled

            :param address: object address in our system
            """
            url = api.get_object_url_by_address(address)
            if len(url) == 0:
                return "Address does not exists", 404

            if private:
                uri = f"https://{host}/api/objects/{url}"
            else:
                uri = f"http://{host}/api/objects/{url}"

            return redirect(uri), 303

        @self.blueprint.route("/objects/<bucket>/<key>", methods=['POST'])
        def update_object(bucket, key):
            """update object enable or disable

            :param bucket: object bucket
            :param key: object key
            """
            status = request.args.get("status", 1)

            api.update_object(bucket, key, status)

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

        @self.blueprint.route("/objects/<bucket>/<key>/register", methods=['GET'])
        def register(bucket, key):
            """register an object in our system

            :param bucket: bucket name
            :param key: object key
            """
            url = api.register_object(bucket, key)
            if url is None:
                return "Failed to register", 503

            return "OK", 200

    def get_blue_print(self) -> Blueprint:
        """get api blueprint

        :return: flask blueprint
        """
        return self.blueprint
