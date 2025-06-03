# AI-powered-switches Backend

这是 AI-powered-switches 的后端服务，基于 `Flask` 构建，提供 `REST API` 接口，用于解析自然语言生成网络交换机配置并下发到设备

### 项目结构

```bash
src/backend/
├── app/
│   ├── __init__.py             # 创建 Flask 应用实例
│   ├── api/                    # API 路由模块
│   │   ├── __init__.py         # 注册 API 蓝图
│   │   ├── command_parser.py   # /api/parse_command 接口
│   │   └── network_config.py   # /api/apply_config 接口
│   └── services/               # 核心服务逻辑
│       └── ai_services.py      # 调用外部 AI 服务生成配置
├── config.py                   # 配置加载与环境变量管理
├── exceptions.py               # 自定义异常定义
├── run.py                      # 程序入口
├── requirements.txt            # Python 依赖列表
└── Dockerfile/Dockerfile       # 后端 Docker 镜像构建文件
```

### 本地运行

``` bash
pip install -r requirements.txt
```

创建`.env`并参照`.envExample`写入环境变量

```bash
python run.py
```

### Docker构建

```bash
docker build -t ai-switch-backend -f Dockerfile/Dockerfile .
```

```bash
docker run -p 5000:5000 \
  -e AI_API_KEY=your_api_key \
  -e SWITCH_USER=admin \
  -e SWITCH_PASS=your_password \
  ai-switch-backend
```
