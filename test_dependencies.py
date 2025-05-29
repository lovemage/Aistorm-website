#!/usr/bin/env python3
"""
AIStorm 依赖测试脚本
验证所有必需的Python模块都能正确导入
"""

import sys

def test_imports():
    """测试所有必需的模块导入"""
    print("🔍 测试Python依赖模块...")
    
    success_count = 0
    total_count = 0
    
    # 必需的核心模块
    required_modules = [
        ('flask', 'Flask'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('flask_cors', 'Flask-CORS'),
        ('requests', 'Requests'),
        ('werkzeug', 'Werkzeug'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('datetime', 'Datetime (内置)'),
        ('os', 'OS (内置)'),
        ('json', 'JSON (内置)'),
        ('hashlib', 'Hashlib (内置)'),
        ('hmac', 'HMAC (内置)'),
        ('time', 'Time (内置)'),
        ('functools', 'Functools (内置)')
    ]
    
    # 可选模块
    optional_modules = [
        ('python_dotenv', 'Python-dotenv'),
        ('cryptography', 'Cryptography'),
        ('dateutil', 'Python-dateutil')
    ]
    
    print("\n📦 核心模块测试:")
    for module_name, display_name in required_modules:
        total_count += 1
        try:
            __import__(module_name)
            print(f"  ✅ {display_name}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {display_name} - {str(e)}")
    
    print("\n📦 可选模块测试:")
    for module_name, display_name in optional_modules:
        try:
            __import__(module_name)
            print(f"  ✅ {display_name}")
        except ImportError:
            print(f"  ⚠️ {display_name} - 可选模块，未安装")
    
    print(f"\n📊 测试结果: {success_count}/{total_count} 核心模块成功导入")
    
    if success_count == total_count:
        print("🎉 所有核心依赖都已正确安装！")
        return True
    else:
        print("❌ 部分核心依赖缺失，请检查requirements.txt并重新安装")
        return False

def test_flask_app():
    """测试Flask应用能否正常创建"""
    print("\n🌐 测试Flask应用...")
    
    try:
        import sys
        import os
        
        # 添加backend目录到Python路径
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        
        # 导入应用
        from app import app
        
        print("  ✅ Flask应用创建成功")
        print(f"  ✅ 应用名称: {app.name}")
        print(f"  ✅ 调试模式: {app.debug}")
        
        return True
    except Exception as e:
        print(f"  ❌ Flask应用创建失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 AIStorm 依赖检查开始")
    print("=" * 50)
    
    # 测试Python版本
    print(f"🐍 Python版本: {sys.version}")
    
    # 测试模块导入
    imports_ok = test_imports()
    
    # 测试Flask应用
    app_ok = test_flask_app()
    
    print("\n" + "=" * 50)
    if imports_ok and app_ok:
        print("🎉 所有测试通过！应用准备就绪")
        sys.exit(0)
    else:
        print("❌ 测试失败！请修复问题后重试")
        sys.exit(1)

if __name__ == '__main__':
    main() 