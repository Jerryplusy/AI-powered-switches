#配置生成和交换机交互逻辑
from flask import request, jsonify
from netmiko import ConnectHandler
from ...config import Config
from ...exceptions import NetworkDeviceError


@api_blueprint.route('/apply_config', methods=['POST'])
def apply_config_handler():
    """应用配置到网络设备"""
    try:
        data = request.get_json()
        required_fields = ['config', 'device_ip']
        if not all(field in data for field in required_fields):
            raise InvalidInputError("缺少必要参数")

        # 安全验证
        validate_configuration(data['config'])

        # 执行配置
        output = execute_switch_config(
            device_ip=data['device_ip'],
            commands=data['config'],
            username=Config.SWITCH_USERNAME,
            password=Config.SWITCH_PASSWORD
        )

        return jsonify({
            "status": "success",
            "output": output
        })

    except NetworkDeviceError as e:
        return jsonify({"status": "error", "message": str(e)}), 502
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def validate_configuration(commands):
    """配置安全验证"""
    dangerous_commands = ['delete', 'erase', 'format', 'reload']
    for cmd in dangerous_commands:
        if any(cmd in line.lower() for line in commands):
            raise InvalidInputError(f"检测到危险命令: {cmd}")


def execute_switch_config(device_ip, commands, username, password):
    """执行交换机配置"""
    device = {
        'device_type': 'cisco_ios',
        'host': device_ip,
        'username': username,
        'password': password,
        'timeout': 10
    }

    try:
        with ConnectHandler(**device) as conn:
            conn.enable()  # 进入特权模式
            output = conn.send_config_set(commands)
            conn.save_config()  # 保存配置
            return output
    except Exception as e:
        raise NetworkDeviceError(f"设备配置失败: {str(e)}")