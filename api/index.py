"""
Vercel Serverless Function 入口
"""
import sys
import os

# 将项目根目录添加到 Python 路径，确保能导入 app/ 包
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from app.main import create_app

app = create_app()
