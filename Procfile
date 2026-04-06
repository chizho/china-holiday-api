# Render 部署配置文件
# 启动命令：使用 uvicorn 加载 FastAPI 应用，监听 0.0.0.0 和环境变量 PORT
web: uvicorn app.main:create_app --factory --host 0.0.0.0 --port $PORT --log-level info
