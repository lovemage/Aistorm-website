#!/usr/bin/env python3
"""
直接测试OxaPay API调用
"""

import requests
import json

def test_oxapay_direct():
    """直接测试OxaPay API"""
    
    # 测试数据
    data = {
        'merchant': 'URXMY9-VHVPGK-DA4HEC-2EXI3S',
        'amount': 130.0,
        'currency': 'USDT',
        'lifeTime': 15,
        'feePaidByPayer': 1,
        'callbackUrl': 'http://localhost:5001/oxapay-webhook',
        'description': '购买 ChatGPT Pro x1',
        'orderId': 'test_order_123',
        'email': 'test@example.com',
    }

    print('🧪 直接测试OxaPay API调用')
    print('=' * 50)
    print('发送到OxaPay的数据:')
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print('=' * 50)

    try:
        response = requests.post(
            'https://api.oxapay.com/merchants/request', 
            json=data, 
            timeout=15,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f'响应状态码: {response.status_code}')
        print(f'响应头: {dict(response.headers)}')
        print(f'响应内容: {response.text}')
        
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                response_json = response.json()
                print(f'JSON响应: {json.dumps(response_json, indent=2, ensure_ascii=False)}')
                
                # 分析响应
                if response_json.get('result') == 102:
                    print('❌ API密钥无效')
                elif response_json.get('result') == 100:
                    print('✅ 请求成功')
                else:
                    print(f'⚠️ 未知结果码: {response_json.get("result")}')
                    if 'error' in response_json:
                        print(f'错误信息: {response_json["error"]}')
                    if 'message' in response_json:
                        print(f'消息: {response_json["message"]}')
                        
            except json.JSONDecodeError:
                print('❌ 响应不是有效的JSON格式')
        
    except requests.exceptions.Timeout:
        print('❌ 请求超时')
    except requests.exceptions.RequestException as e:
        print(f'❌ 请求异常: {e}')
    except Exception as e:
        print(f'❌ 其他错误: {e}')

if __name__ == "__main__":
    test_oxapay_direct() 