#!/usr/bin/env python3
"""
AIStorm 应用启动脚本
用于Railway等部署平台的简化启动
"""

import os
import sys

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# 设置工作目录为backend
os.chdir(backend_dir)

# 导入并运行Flask应用
if __name__ == '__main__':
    from app import app, init_db
    
    # 初始化数据库
    with app.app_context():
        init_db(app)
    
    # 获取端口号，支持环境变量
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🚀 启动 AIStorm 应用在端口 {port}")
    app.run(debug=debug, host='0.0.0.0', port=port) 