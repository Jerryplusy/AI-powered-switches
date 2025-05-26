# 解析中文命令逻辑
from flask import request, jsonify
from ...services.ai_service import get_network_config
from ...exceptions import InvalidInputError


@api_blueprint.route('/parse_command', methods=['POST'])
def parse_command_handler():
    """处理自然语言命令解析"""
    try:
        data = request.get_json()
        if not data or 'command' not in data:
            raise InvalidInputError("缺少命令参数")

        command = data['command']
        config = get_network_config(command)

        return jsonify({
            "status": "success",
            "config": config
        })

    except InvalidInputError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"服务器内部错误: {str(e)}"}), 500