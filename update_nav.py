#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 需要更新的页面列表
pages_to_update = [
    'index.html',
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
    'pages/shop.html',
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
                <a href="/" class="nav-link{active_home}">home</a>
                <a href="chatgpt.html" class="nav-link{active_chatgpt}">ChatGPT Pro</a>
                <a href="claude.html" class="nav-link{active_claude}">Claude Max</a>
                <a href="cursor.html" class="nav-link{active_cursor}">Cursor Pro</a>
                <a href="grok.html" class="nav-link{active_grok}">SuperGrok</a>
                <a href="lovable.html" class="nav-link{active_lovable}">Lovable Pro</a>
                <a href="ai_news.html" class="nav-link{active_news}">AI News</a>
            </div>
            
            <div class="nav-actions">
                <button class="theme-toggle" aria-label="切换主题">🌙</button>
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
        <a href="{home_href_mobile}" class="nav-link{active_home}">home</a>
        <a href="{chatgpt_href_mobile}" class="nav-link{active_chatgpt}">ChatGPT Pro</a>
        <a href="{claude_href_mobile}" class="nav-link{active_claude}">Claude Max</a>
        <a href="{cursor_href_mobile}" class="nav-link{active_cursor}">Cursor Pro</a>
        <a href="{grok_href_mobile}" class="nav-link{active_grok}">SuperGrok</a>
        <a href="{lovable_href_mobile}" class="nav-link{active_lovable}">Lovable Pro</a>
        <a href="{news_href_mobile}" class="nav-link{active_news}">AI News</a>
        <a href="{shop_href_mobile}" class="nav-link btn btn-primary" style="margin-top: var(--spacing-xl);">购买服务</a>
    </nav>'''

def determine_active_page(filename):
    """根据文件名确定哪个导航链接应该是active的"""
    # Specific product pages
    if filename == 'chatgpt.html':
        return 'chatgpt'
    elif filename == 'claude.html':
        return 'claude'
    elif filename == 'cursor.html':
        return 'cursor'
    elif filename == 'grok.html':
        return 'grok'
    elif filename == 'lovable.html':
        return 'lovable'
    # AI News and related content pages
    elif filename == 'ai_news.html' or \
         filename == 'chatgpt_news.html' or \
         filename == 'claude_news.html' or \
         filename == 'grok_news.html' or \
         filename == 'lovable_news.html' or \
         filename == 'ai_prompt_guide.html' or \
         filename == 'ai_settings_guide.html' or \
         filename == 'students_ai_guide.html' or \
         filename == 'lovable_breakout_guide.html':
        return 'news'
    # Home page and other pages default to 'home' active state
    elif filename == 'index.html' or filename == '' or filename in ['about.html', 'faq.html', 'privacy.html', 'refund.html', 'support.html', 'terms.html', 'tutorials.html'] :
        return 'home'
    # Default for any other unhandled page, can also be 'home' or specific logic
    else: 
        return 'home' # Or consider a different default if necessary

def update_navigation(file_path):
    """更新单个文件的导航"""
    print(f"正在更新: {file_path}")
    
    is_root_index = (file_path == 'index.html')
    link_prefix = 'pages/' if is_root_index else ''
    home_link = '/' if is_root_index else '../' # Adjusted for root vs subpage

    # 产品页面链接
    chatgpt_page = f"{link_prefix}chatgpt.html"
    claude_page = f"{link_prefix}claude.html"
    cursor_page = f"{link_prefix}cursor.html"
    grok_page = f"{link_prefix}grok.html"
    lovable_page = f"{link_prefix}lovable.html"
    news_page = f"{link_prefix}ai_news.html"
    shop_page = f"{link_prefix}shop.html"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 获取当前页面的active状态
        filename = os.path.basename(file_path)
        active_page_category = determine_active_page(filename)
        
        # 设置active类
        active_home = ' active' if active_page_category == 'home' else ''
        active_chatgpt = ' active' if active_page_category == 'chatgpt' else ''
        active_claude = ' active' if active_page_category == 'claude' else ''
        active_cursor = ' active' if active_page_category == 'cursor' else ''
        active_grok = ' active' if active_page_category == 'grok' else ''
        active_lovable = ' active' if active_page_category == 'lovable' else ''
        active_news = ' active' if active_page_category == 'news' else ''
        
        # 根据是否为根目录的index.html调整模板中的链接
        # 桌面导航链接
        home_href_desktop = home_link
        chatgpt_href_desktop = chatgpt_page
        claude_href_desktop = claude_page
        cursor_href_desktop = cursor_page
        grok_href_desktop = grok_page
        lovable_href_desktop = lovable_page
        news_href_desktop = news_page

        # 移动导航链接 (通常与桌面版相同，但也需要前缀处理)
        home_href_mobile = home_link
        chatgpt_href_mobile = chatgpt_page
        claude_href_mobile = claude_page
        cursor_href_mobile = cursor_page
        grok_href_mobile = grok_page
        lovable_href_mobile = lovable_page
        news_href_mobile = news_page
        shop_href_mobile = shop_page

        # 生成新的导航HTML
        # 注意：模板中占位符已更新，以接受动态链接
        current_nav_template = nav_template.replace('<a href="/" class="nav-logo">', f'<a href="{home_link}" class="nav-logo">')

        new_nav = current_nav_template.format(
            home_href_desktop=home_href_desktop,
            chatgpt_href_desktop=chatgpt_href_desktop,
            claude_href_desktop=claude_href_desktop,
            cursor_href_desktop=cursor_href_desktop,
            grok_href_desktop=grok_href_desktop,
            lovable_href_desktop=lovable_href_desktop,
            news_href_desktop=news_href_desktop,
            
            home_href_mobile=home_href_mobile,
            chatgpt_href_mobile=chatgpt_href_mobile,
            claude_href_mobile=claude_href_mobile,
            cursor_href_mobile=cursor_href_mobile,
            grok_href_mobile=grok_href_mobile,
            lovable_href_mobile=lovable_href_mobile,
            news_href_mobile=news_href_mobile,
            shop_href_mobile=shop_href_mobile,

            active_home=active_home,
            active_chatgpt=active_chatgpt,
            active_claude=active_claude,
            active_cursor=active_cursor,
            active_grok=active_grok,
            active_lovable=active_lovable,
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