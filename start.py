#!/usr/bin/env python3
import os
import sys

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def main():
    try:
        print("=== AIStorm Application Startup ===")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        
        # 检查环境变量
        port = os.environ.get('PORT', '5001')
        print(f"PORT environment variable: {port}")
        
        # 导入并启动应用
        print("Importing Flask application...")
        from app import app, init_db
        
        print("Setting up application context...")
        with app.app_context():
            print("Initializing database...")
            init_db(app)
            print("Database initialization completed!")
        
        # 启动应用
        port_int = int(port)
        print(f"Starting Flask application on 0.0.0.0:{port_int}")
        
        app.run(
            host='0.0.0.0',
            port=port_int,
            debug=False  # 生产环境关闭debug
        )
        
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main() 