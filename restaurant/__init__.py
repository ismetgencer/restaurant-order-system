import os

from flask import Flask

from restaurant.db import init_db
from restaurant.menu import MENU, MENU_IMAGES
from restaurant.routes import bp


def create_app():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(
        __name__,
        template_folder=os.path.join(root, 'templates'),
        static_folder=os.path.join(root, 'static'),
    )
    app.register_blueprint(bp)

    @app.context_processor
    def inject_menu():
        return {'menu': MENU, 'menu_images': MENU_IMAGES}

    init_db()
    return app
