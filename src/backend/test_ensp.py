import asyncio
import logging
from src.backend.app.api.network_config import SwitchConfigurator
#该文件用于测试

# 设置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_ensp():
    """eNSP测试函数"""
    # 1. 初始化配置器（对应eNSP设备设置）
    configurator = SwitchConfigurator(
        ensp_mode=True,     # 启用eNSP模式
        ensp_port=2000,     # 必须与eNSP中设备设置的Telnet端口一致
        username="admin",   # 默认账号
        password="admin",   # 默认密码
        timeout=15          # 建议超时设长些
    )

    # 2. 执行配置（示例：创建VLAN100）
    try:
        result = await configurator.safe_apply(
            ip="127.0.0.1",  # 本地连接固定用这个地址
            config={
                "type": "vlan",
                "vlan_id": 100,
                "name": "测试VLAN"
            }
        )
        print("✅ 配置结果:", result)
    except Exception as e:
        print("❌ 配置失败:", str(e))

# 运行测试
if __name__ == "__main__":
    asyncio.run(test_ensp())