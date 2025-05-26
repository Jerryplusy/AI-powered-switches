from flask import Flask
from .api import api_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 注册蓝图
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app