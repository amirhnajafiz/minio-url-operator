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
            return render_template('index.j2', title="MUO: Home")

        @self.blueprint.route('/search', methods=['GET'])
        def search_page():
            return render_template('bucket.j2', title="MUO: Buckets")

        @self.blueprint.route('/docs', methods=['GET'])
        def help_page():
            return render_template('help.j2', title="MUO: Docs")

    def get_blue_print(self) -> Blueprint:
        """get views blueprint

        :return: flask blueprint
        """
        return self.blueprint
