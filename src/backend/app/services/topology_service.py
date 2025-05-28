#拓补处理逻辑
def generate_multi_device_config(topology):
    """
    topology示例:
    {
        "core_switches": [sw1, sw2],
        "access_switches": {
            "sw1": [sw3, sw4],
            "sw2": [sw5, sw6]
        }
    }
    """
    configs = {}
    # 生成核心层配置（如MSTP根桥选举）
    for sw in topology['core_switches']:
        configs[sw] = generate_core_config(sw)

    # 生成接入层配置（如端口绑定）
    for core_sw, access_sws in topology['access_switches'].items():
        for sw in access_sws:
            configs[sw] = generate_access_config(sw, uplink=core_sw)

    return configs