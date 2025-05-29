#!/usr/bin/env python3
"""
OxaPay配置测试工具 - 根据官方Python示例更新
帮助诊断API密钥和连接问题
"""

import os
import requests
import json
import time
from datetime import datetime

def test_oxapay_merchant_api():
    """测试OxaPay Merchant API - 使用官方Python示例的代码风格"""
    print("🔧 OxaPay Merchant API测试工具")
    print("=" * 50)
    
    # 检查环境变量
    api_key = os.environ.get('OXAPAY_SECRET_KEY')
    
    if not api_key:
        print("❌ 环境变量 OXAPAY_SECRET_KEY 未设置")
        print("💡 请设置环境变量:")
        print("   export OXAPAY_SECRET_KEY='your-api-key'")
        return False
    
    print(f"✅ API密钥已配置: {api_key[:8]}...（已隐藏）")
    
    # 尝试不同的API endpoint和方法
    test_methods = [
        {
            'name': '方法1: Merchant API (body参数)',
            'url': 'https://api.oxapay.com/merchants/request',
            'headers': {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            'data': {
                'merchant': api_key,
                'amount': 1.0,
                'currency': 'USDT',
                'lifeTime': 15,
                'feePaidByPayer': 1,
                'callbackUrl': 'https://www.aistorm.art/oxapay-webhook',
                'description': 'API配置测试',
                'orderId': f'test_{int(time.time())}',
                'email': 'test@example.com',
            },
            'use_json_dumps': False
        },
        {
            'name': '方法2: Merchant API (header认证)',
            'url': 'https://api.oxapay.com/merchants/request',
            'headers': {
                'merchant_api_key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            'data': {
                'amount': 1.0,
                'currency': 'USDT',
                'lifeTime': 15,
                'feePaidByPayer': 1,
                'callbackUrl': 'https://www.aistorm.art/oxapay-webhook',
                'description': 'API配置测试',
                'orderId': f'test_{int(time.time())}',
                'email': 'test@example.com',
            },
            'use_json_dumps': True
        },
        {
            'name': '方法3: General API风格 (header认证)',
            'url': 'https://api.oxapay.com/v1/merchants/request',
            'headers': {
                'general_api_key': api_key,
                'Content-Type': 'application/json'
            },
            'data': {
                'amount': 1.0,
                'currency': 'USDT',
                'lifeTime': 15,
                'feePaidByPayer': 1,
                'callbackUrl': 'https://www.aistorm.art/oxapay-webhook',
                'description': 'API配置测试',
                'orderId': f'test_{int(time.time())}',
                'email': 'test@example.com',
            },
            'use_json_dumps': True
        }
    ]
    
    for method in test_methods:
        print(f"\n📤 测试 {method['name']}...")
        print(f"API URL: {method['url']}")
        print(f"Headers: {method['headers']}")
        print(f"数据: {json.dumps(method['data'], indent=2)}")
        
        try:
            if method['use_json_dumps']:
                # 使用官方示例的方式
                response = requests.post(
                    method['url'],
                    data=json.dumps(method['data']),
                    headers=method['headers'],
                    timeout=30
                )
            else:
                # 使用json参数
                response = requests.post(
                    method['url'],
                    json=method['data'],
                    headers=method['headers'],
                    timeout=30
                )
            
            print(f"\n📥 响应结果:")
            print(f"HTTP状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    result_code = result.get('result')
                    
                    if result_code == 100:
                        print(f"\n✅ {method['name']} 成功！")
                        print(f"发票ID: {result.get('trackId')}")
                        print(f"支付链接: {result.get('payLink')}")
                        return True, method
                        
                    elif result_code == 102:
                        print(f"\n❌ {method['name']} - API密钥无效")
                        
                    else:
                        print(f"\n❌ {method['name']} - 错误码: {result_code}")
                        print(f"错误信息: {result.get('message', '未知')}")
                        
                except json.JSONDecodeError:
                    print(f"\n❌ {method['name']} - 响应不是有效的JSON格式")
            else:
                print(f"\n❌ {method['name']} - HTTP请求失败: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"\n❌ {method['name']} - 请求超时")
            
        except requests.exceptions.ConnectionError:
            print(f"\n❌ {method['name']} - 连接失败")
            
        except Exception as e:
            print(f"\n❌ {method['name']} - 测试失败: {str(e)}")
    
    return False, None

def test_general_api():
    """测试OxaPay General API - 使用官方示例"""
    print("\n🔧 OxaPay General API测试 (基于官方示例)")
    print("=" * 50)
    
    api_key = os.environ.get('OXAPAY_SECRET_KEY')
    
    if not api_key:
        print("❌ 环境变量 OXAPAY_SECRET_KEY 未设置")
        return False
    
    # 使用官方示例的代码结构
    url = 'https://api.oxapay.com/v1/general/swap'
    
    data = {
       "amount": 0.5,
       "from_currency": "BTC",
       "to_currency": "USDT"
    }
    
    headers = {
       'general_api_key': api_key,
       'Content-Type': 'application/json'
    }
    
    print(f"📤 测试General API Swap功能...")
    print(f"URL: {url}")
    print(f"Headers: {headers}")
    print(f"数据: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers, timeout=30)
        result = response.json()
        
        print(f"\n📥 响应结果:")
        print(f"HTTP状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2)}")
        
        if response.status_code == 200 and result.get('success'):
            print("✅ General API测试成功 - API密钥有效")
            return True
        else:
            print("❌ General API测试失败")
            return False
            
    except Exception as e:
        print(f"❌ General API测试失败: {str(e)}")
        return False

def get_oxapay_info():
    """获取OxaPay相关信息"""
    print("\n📋 OxaPay集成信息:")
    print("=" * 50)
    print("官方文档: https://docs.oxapay.com/")
    print("Merchant API: https://api.oxapay.com/merchants/request")
    print("General API: https://api.oxapay.com/v1/general/")
    print("\n支持的错误码:")
    print("  100 - 成功")
    print("  101 - 参数错误")
    print("  102 - API密钥无效")
    print("  103 - 余额不足")
    print("  104 - 货币不支持")
    print("  105 - 金额超出限制")
    
    print("\n不同的API认证方式:")
    print("  1. Merchant API (body): merchant参数在请求体中")
    print("  2. Merchant API (header): merchant_api_key在header中")
    print("  3. General API: general_api_key在header中")
    
    print("\n环境变量设置:")
    print("  export OXAPAY_SECRET_KEY='your-api-key'")

if __name__ == '__main__':
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 显示基本信息
    get_oxapay_info()
    
    # 测试General API
    general_success = test_general_api()
    
    # 测试Merchant API
    merchant_success, working_method = test_oxapay_merchant_api()
    
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"  General API: {'✅ 成功' if general_success else '❌ 失败'}")
    print(f"  Merchant API: {'✅ 成功' if merchant_success else '❌ 失败'}")
    
    if merchant_success and working_method:
        print(f"\n🎉 找到可用的Merchant API方法: {working_method['name']}")
        print("💡 建议在实际代码中使用这种方法")
    elif general_success:
        print("\n⚠️ General API可用，但Merchant API不可用")
        print("💡 请检查API密钥权限或联系OxaPay技术支持")
    else:
        print("\n❌ 所有API测试都失败")
        print("💡 请检查API密钥是否正确或联系技术支持")
    
    print("=" * 50) 