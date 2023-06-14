from flask import Blueprint
from .handler import Handler


# create a blueprint for application apis
api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")

# create a new handler
api = Handler()


@api_blueprint.route("/objects", methods=['GET'])
def get_objects():
    api.get_objects()
