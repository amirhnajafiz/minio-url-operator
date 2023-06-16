from flask import Blueprint, render_template


class Views(object):
    def __init__(self):
        # create a blueprint for views
        self.blueprint = Blueprint('views_blueprint', __name__)

        @self.blueprint.route('/', methods=['GET'])
        def index_page():
            """home page of application

            :return: index.html template
            """
            return render_template('index.html')

        @self.blueprint.route('/docs', methods=['GET'])
        def help_page():
            return render_template('help.html')

        @self.blueprint.route('/docs/snappline', methods=['GET'])
        def snappline_help_page():
            return render_template('help.snappline.html')

    def get_blue_print(self) -> Blueprint:
        """get views blueprint

        :return: flask blueprint
        """
        return self.blueprint
