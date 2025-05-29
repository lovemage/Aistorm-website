#!/usr/bin/env python3
"""
AIStorm 支付流程测试脚本
用于本地测试支付API的完整流程
"""

import requests
import json
import time

def test_payment_flow():
    """测试完整的支付流程"""
    
    # 配置
    BASE_URL = "http://localhost:5001"
    TEST_EMAIL = "test@example.com"
    TEST_PRODUCT = "chatgpt-pro"
    TEST_QUANTITY = 1
    
    print("🚀 开始测试支付流程...")
    print(f"🌐 测试服务器: {BASE_URL}")
    print(f"📧 测试邮箱: {TEST_EMAIL}")
    print(f"📦 测试产品: {TEST_PRODUCT}")
    print("-" * 50)
    
    try:
        # 步骤1: 测试获取产品列表
        print("📋 步骤1: 获取产品列表")
        response = requests.get(f"{BASE_URL}/api/products")
        
        if response.status_code == 200:
            products = response.json()
            print(f"✅ 成功获取 {len(products)} 个产品")
            
            # 查找测试产品
            test_product = None
            for product in products:
                if product['slug'] == TEST_PRODUCT:
                    test_product = product
                    break
            
            if test_product:
                print(f"✅ 找到测试产品: {test_product['name']} - ${test_product['price_usd']}")
            else:
                print(f"❌ 未找到测试产品: {TEST_PRODUCT}")
                return False
        else:
            print(f"❌ 获取产品列表失败: {response.status_code}")
            return False
        
        # 步骤2: 创建订单
        print("\n📝 步骤2: 创建订单")
        order_data = {
            "customer_email": TEST_EMAIL,
            "product_slug": TEST_PRODUCT,
            "quantity": TEST_QUANTITY
        }
        
        print(f"📤 发送订单数据: {json.dumps(order_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/create-order",
            json=order_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 响应状态: {response.status_code}")
        print(f"📥 响应内容: {response.text}")
        
        if response.status_code == 200:
            order_result = response.json()
            if order_result.get('success'):
                order_id = order_result['order_id']
                total_amount = order_result['total_amount']
                print(f"✅ 订单创建成功!")
                print(f"🆔 订单ID: {order_id}")
                print(f"💰 订单金额: ${total_amount}")
            else:
                print(f"❌ 订单创建失败: {order_result.get('error')}")
                return False
        else:
            print(f"❌ 订单创建请求失败: {response.status_code}")
            return False
        
        # 步骤3: 生成支付链接
        print("\n💳 步骤3: 生成支付链接")
        payment_data = {
            "orderId": order_id
        }
        
        print(f"📤 发送支付数据: {json.dumps(payment_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/oxapay-payment",
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 响应状态: {response.status_code}")
        print(f"📥 响应内容: {response.text}")
        
        if response.status_code == 200:
            payment_result = response.json()
            if payment_result.get('success'):
                pay_link = payment_result['payLink']
                track_id = payment_result.get('trackId')
                print(f"✅ 支付链接生成成功!")
                print(f"🔗 支付链接: {pay_link}")
                print(f"🔍 追踪ID: {track_id}")
                
                # 测试模式提示
                if payment_result.get('testMode'):
                    print("🧪 注意: 当前运行在测试模式")
            else:
                print(f"❌ 支付链接生成失败: {payment_result.get('error')}")
                return False
        else:
            print(f"❌ 支付链接生成请求失败: {response.status_code}")
            return False
        
        # 步骤4: 检查订单状态
        print("\n📊 步骤4: 检查订单状态")
        response = requests.get(f"{BASE_URL}/api/order-status/{order_id}")
        
        if response.status_code == 200:
            status_result = response.json()
            if status_result.get('success'):
                order_info = status_result['order']
                print(f"✅ 订单状态查询成功!")
                print(f"📊 支付状态: {order_info['payment_status']}")
                print(f"📊 订单状态: {order_info['order_status']}")
            else:
                print(f"❌ 订单状态查询失败: {status_result.get('error')}")
                return False
        else:
            print(f"❌ 订单状态查询请求失败: {response.status_code}")
            return False
        
        # 步骤5: 模拟Webhook回调（测试模式）
        print("\n🔔 步骤5: 测试Webhook回调")
        webhook_data = {
            "orderId": order_id,
            "status": "Paid",
            "amount": str(total_amount),
            "currency": "USDT",
            "trackId": track_id or "test_track_id"
        }
        
        print(f"📤 发送Webhook数据: {json.dumps(webhook_data, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/oxapay-webhook",
            json=webhook_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📥 响应状态: {response.status_code}")
        print(f"📥 响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook处理成功!")
        else:
            print(f"❌ Webhook处理失败: {response.status_code}")
            return False
        
        # 步骤6: 再次检查订单状态
        print("\n🔍 步骤6: 确认最终订单状态")
        time.sleep(1)  # 等待1秒确保数据库更新
        
        response = requests.get(f"{BASE_URL}/api/order-status/{order_id}")
        
        if response.status_code == 200:
            status_result = response.json()
            if status_result.get('success'):
                order_info = status_result['order']
                print(f"✅ 最终订单状态:")
                print(f"📊 支付状态: {order_info['payment_status']}")
                print(f"📊 订单状态: {order_info['order_status']}")
                print(f"⏰ 支付时间: {order_info.get('paid_at', 'N/A')}")
                
                if order_info['payment_status'] == 'completed':
                    print("🎉 支付流程测试完全成功!")
                    return True
                else:
                    print("⚠️ 支付状态未更新为completed")
                    return False
            else:
                print(f"❌ 最终状态查询失败: {status_result.get('error')}")
                return False
        else:
            print(f"❌ 最终状态查询请求失败: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 请确保后端服务器正在运行 (python3 backend/app.py)")
        return False
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")
        return False

def test_telegram_notification():
    """测试Telegram通知功能"""
    print("\n🤖 测试Telegram通知功能...")
    
    try:
        response = requests.post(
            "http://localhost:5001/api/test-telegram",
            json={"type": "test"},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Telegram通知测试成功!")
            else:
                print(f"❌ Telegram通知测试失败: {result.get('message')}")
        else:
            print(f"❌ Telegram通知请求失败: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Telegram通知测试错误: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 AIStorm 支付流程完整测试")
    print("=" * 60)
    
    # 测试Telegram通知
    test_telegram_notification()
    
    # 测试支付流程
    success = test_payment_flow()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 所有测试通过! 支付流程工作正常")
    else:
        print("❌ 测试失败! 请检查上述错误信息")
    print("=" * 60) 