
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 启用CORS（开发环境）
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 注册蓝图
    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app