#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 需要更新的页面列表
pages_to_update = [
    'pages/ai_news.html',
    'pages/ai_prompt_guide.html',
    'pages/ai_settings_guide.html',
    'pages/about.html',
    'pages/chatgpt.html',
    'pages/chatgpt_news.html',
    'pages/claude.html',
    'pages/claude_news.html',
    'pages/cursor.html',
    'pages/faq.html',
    'pages/grok.html',
    'pages/grok_news.html',
    'pages/lovable.html',
    'pages/lovable_news.html',
    'pages/lovable_breakout_guide.html',
    'pages/privacy.html',
    'pages/refund.html',
    'pages/students_ai_guide.html',
    'pages/support.html',
    'pages/terms.html',
    'pages/tutorials.html'
]

# 新的导航HTML模板
nav_template = '''    <!-- 导航栏 -->
    <nav class="nav">
        <div class="container nav-container">
            <a href="/" class="nav-logo">
                <img src="../assets/images/logo.jpeg" alt="AIStorm Logo" style="width: 32px; height: 32px; border-radius: 50%;">
                AIStorm
            </a>
            
            <div class="nav-links desktop-nav">
                <a href="/" class="nav-link{active_home}">首页</a>
                <a href="shop.html" class="nav-link{active_shop}">商店</a>
                <a href="ai_news.html" class="nav-link{active_news}">AI新闻</a>
                <a href="/#contact" class="nav-link">联系</a>
            </div>
            
            <div class="nav-actions">
                <button class="theme-toggle" aria-label="切换主题">🌙</button>
                <a href="shop.html" class="btn btn-primary">购买服务</a>
                
                <!-- 汉堡菜单按钮 -->
                <button class="mobile-menu-toggle" aria-label="菜单">
                    <span class="hamburger-line"></span>
                    <span class="hamburger-line"></span>
                    <span class="hamburger-line"></span>
                </button>
            </div>
        </div>
    </nav>
    
    <!-- 移动端导航菜单 -->
    <nav class="mobile-nav">
        <a href="/" class="nav-link{active_home}">首页</a>
        <a href="shop.html" class="nav-link{active_shop}">商店</a>
        <a href="ai_news.html" class="nav-link{active_news}">AI新闻</a>
        <a href="/#contact" class="nav-link">联系</a>
        <a href="shop.html" class="nav-link btn btn-primary" style="margin-top: var(--spacing-xl);">购买服务</a>
    </nav>'''

def determine_active_page(filename):
    """根据文件名确定哪个导航链接应该是active的"""
    if 'ai_news' in filename or '_news' in filename or 'ai_prompt' in filename or 'ai_settings' in filename or 'students_ai' in filename or 'lovable_breakout' in filename:
        return 'news'
    elif filename in ['chatgpt.html', 'claude.html', 'grok.html', 'cursor.html', 'lovable.html']:
        return 'shop'
    else:
        return ''

def update_navigation(file_path):
    """更新单个文件的导航"""
    print(f"正在更新: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取当前页面的active状态
        filename = os.path.basename(file_path)
        active_page = determine_active_page(filename)
        
        # 设置active类
        active_home = ' active' if active_page == '' else ''
        active_shop = ' active' if active_page == 'shop' else ''
        active_news = ' active' if active_page == 'news' else ''
        
        # 生成新的导航HTML
        new_nav = nav_template.format(
            active_home=active_home,
            active_shop=active_shop,
            active_news=active_news
        )
        
        # 查找并替换导航部分
        # 匹配从 <!-- 导航栏 --> 到下一个主要section的内容
        nav_pattern = r'<!-- 导航栏 -->.*?(?=<!-- (?:面包屑导航|页面头部|主要内容|Hero))'
        
        if re.search(nav_pattern, content, re.DOTALL):
            content = re.sub(nav_pattern, new_nav + '\n\n  ', content, flags=re.DOTALL)
        else:
            # 如果没找到标准模式，尝试其他模式
            nav_pattern2 = r'<nav class="nav">.*?</nav>(?:\s*<nav class="mobile-nav">.*?</nav>)?'
            if re.search(nav_pattern2, content, re.DOTALL):
                content = re.sub(nav_pattern2, new_nav.strip(), content, flags=re.DOTALL)
            else:
                print(f"  警告: 在 {file_path} 中找不到导航结构")
                return False
        
        # 添加mobile-nav.js引用（如果不存在）
        if 'mobile-nav.js' not in content:
            # 在common.js后面添加
            if 'common.js' in content:
                content = content.replace(
                    '<script src="../assets/js/common.js"></script>',
                    '<script src="../assets/js/common.js"></script>\n  <script src="../assets/js/mobile-nav.js"></script>'
                )
            # 或者在theme-toggle.js后面添加
            elif 'theme-toggle.js' in content:
                content = content.replace(
                    '<script src="../assets/js/theme-toggle.js"></script>',
                    '<script src="../assets/js/theme-toggle.js"></script>\n  <script src="../assets/js/mobile-nav.js"></script>'
                )
            else:
                print(f"  警告: 在 {file_path} 中找不到合适的位置添加mobile-nav.js")
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✓ 成功更新 {file_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ 更新 {file_path} 时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始批量更新导航结构...")
    print(f"将更新 {len(pages_to_update)} 个页面\n")
    
    success_count = 0
    for page in pages_to_update:
        if update_navigation(page):
            success_count += 1
        print()
    
    print(f"\n更新完成！成功: {success_count}/{len(pages_to_update)}")

if __name__ == "__main__":
    main() 