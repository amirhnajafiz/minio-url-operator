from flask import Blueprint, render_template


# create a blueprint for views
views_blueprint = Blueprint('views_blueprint', __name__)


@views_blueprint.route('/', methods=['GET'])
def index():
    """home page of application

    :return: index.html template
    """
    return render_template('index.html')
