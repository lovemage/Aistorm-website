#!/usr/bin/env python3
"""
AIStorm 应用启动脚本
用于Railway等部署平台的简化启动
"""

import os
import sys
import traceback

def main():
    try:
        print("🚀 AIStorm 应用启动中...")
        print(f"🐍 Python版本: {sys.version}")
        print(f"📁 当前工作目录: {os.getcwd()}")
        print(f"📁 脚本目录: {os.path.dirname(os.path.abspath(__file__))}")
        
        # 检查环境变量
        required_env_vars = ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'OXAPAY_SECRET_KEY']
        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ 缺少环境变量: {', '.join(missing_vars)}")
        else:
            print("✅ 所有必需的环境变量都已设置")
        
        # 获取项目根目录和backend目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.join(script_dir, 'backend')
        
        print(f"📁 Script目录: {script_dir}")
        print(f"📁 Backend目录: {backend_dir}")
        print(f"📁 Backend目录存在: {os.path.exists(backend_dir)}")
        
        if not os.path.exists(backend_dir):
            print("❌ Backend目录不存在")
            # 尝试查找backend目录
            possible_paths = [
                os.path.join(script_dir, 'backend'),
                os.path.join(script_dir, '..', 'backend'),
                os.path.join(os.getcwd(), 'backend')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    backend_dir = path
                    print(f"✅ 找到Backend目录: {backend_dir}")
                    break
            else:
                print("❌ 无法找到Backend目录")
                sys.exit(1)
        
        # 检查app.py文件是否存在
        app_file = os.path.join(backend_dir, 'app.py')
        print(f"📄 App文件路径: {app_file}")
        print(f"📄 App文件存在: {os.path.exists(app_file)}")
        
        if not os.path.exists(app_file):
            print("❌ app.py文件不存在")
            sys.exit(1)
        
        # 添加backend目录到Python路径
        sys.path.insert(0, backend_dir)
        print(f"📋 Python路径已更新，前3项: {sys.path[:3]}")
        
        # 尝试导入模块
        print("📦 正在导入Flask应用模块...")
        try:
            from app import app, init_db
            print("✅ 成功导入Flask应用")
        except ImportError as e:
            print(f"❌ 导入失败: {str(e)}")
            print("尝试的路径:")
            for path in sys.path[:5]:
                print(f"  - {path}")
            traceback.print_exc()
            sys.exit(1)
        
        # 检查Flask应用是否正确创建
        print("🔍 检查Flask应用配置...")
        print(f"App名称: {app.name}")
        print(f"Debug模式: {app.debug}")
        print(f"Secret Key设置: {'是' if app.secret_key else '否'}")
        
        # 初始化数据库
        print("🗄️ 正在初始化数据库...")
        try:
            with app.app_context():
                init_db(app)
            print("✅ 数据库初始化成功")
        except Exception as e:
            print(f"❌ 数据库初始化失败: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
        
        # 获取端口号，支持环境变量
        port = int(os.environ.get('PORT', 5001))
        
        # 在生产环境中禁用调试模式
        flask_env = os.environ.get('FLASK_ENV', 'development')
        is_production = flask_env == 'production'
        debug = not is_production
        
        print(f"🌐 准备启动服务器...")
        print(f"📍 端口: {port}")
        print(f"🔧 调试模式: {debug}")
        print(f"🏭 环境: {flask_env}")
        print(f"🌍 主机: 0.0.0.0")
        
        # 启动应用
        print("🚀 启动Flask应用...")
        app.run(debug=debug, host='0.0.0.0', port=port)
        
    except KeyboardInterrupt:
        print("\n👋 应用被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"💥 启动失败: {str(e)}")
        print("详细错误信息:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 