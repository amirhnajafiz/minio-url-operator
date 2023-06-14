from flask import Blueprint, render_template


# create a blueprint for views
views_blueprint = Blueprint('views_blueprint', __name__)


@views_blueprint.route('/', methods=['GET'])
def index_page():
    """home page of application

    :return: index.html template
    """
    return render_template('index.html')


@views_blueprint.route('/docs', methods=['GET'])
def help_page():
    return render_template('help.html')


@views_blueprint.route('/docs/snappline', methods=['GET'])
def snappline_help_page():
    return render_template('help.snappline.html')
