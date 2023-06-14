from flask import Blueprint


# create a blueprint for application apis
api_blueprint = Blueprint('api_blueprint', __name__, url_prefix="/api")


@api_blueprint.route("/url", methods=['GET'])
def get_urls():
    pass
