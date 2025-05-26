# 注册api蓝图
from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from . import command_parser, network_config