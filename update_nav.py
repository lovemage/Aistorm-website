#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

# 需要更新的页面列表
pages_to_update = [
    'index.html',  # 确保 index.html 在列表中
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

# 新的导航HTML模板 - 使用更全面的动态占位符
nav_template = '''    <!-- 导航栏 -->
    <nav class="nav">
        <div class="container nav-container">
            <a href="{logo_href}" class="nav-logo">
                <img src="{logo_img_src}" alt="AIStorm Logo" style="width: 32px; height: 32px; border-radius: 50%;">
                AIStorm
            </a>
            
            <div class="nav-links desktop-nav">
                <a href="{home_href_desktop}" class="nav-link{active_home}">home</a>
                <a href="{chatgpt_href_desktop}" class="nav-link{active_chatgpt}">ChatGPT Pro</a>
                <a href="{claude_href_desktop}" class="nav-link{active_claude}">Claude Max</a>
                <a href="{cursor_href_desktop}" class="nav-link{active_cursor}">Cursor Pro</a>
                <a href="{grok_href_desktop}" class="nav-link{active_grok}">SuperGrok</a>
                <a href="{lovable_href_desktop}" class="nav-link{active_lovable}">Lovable Pro</a>
                <a href="{news_href_desktop}" class="nav-link{active_news}">AI News</a>
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
    elif filename == 'index.html' or filename == '' or filename == 'shop.html' or filename in ['about.html', 'faq.html', 'privacy.html', 'refund.html', 'support.html', 'terms.html', 'tutorials.html'] : # shop.html now activates 'home'
        return 'home'
    # Default for any other unhandled page
    else:
        return 'home'

def update_navigation(file_path):
    """更新单个文件的导航"""
    print(f"正在更新: {file_path}")
    
    is_root_index = (file_path == 'index.html')
    
    # Determine link prefixes based on current file_path
    logo_href_val = './' if is_root_index else '../' # Corrected: './' or '/' for root, '../' for subpages
    if is_root_index and file_path == 'index.html': # Specifically for the root index.html
        logo_href_val = './' # Or can be simply "/" if served from root
        
    logo_img_src_val = 'assets/images/logo.jpeg' if is_root_index else '../assets/images/logo.jpeg'
    link_prefix_for_subpages = 'pages/' if is_root_index else ''

    # Define all href values for formatting
    home_href_desktop_val = logo_href_val
    chatgpt_href_desktop_val = f"{link_prefix_for_subpages}chatgpt.html"
    claude_href_desktop_val = f"{link_prefix_for_subpages}claude.html"
    cursor_href_desktop_val = f"{link_prefix_for_subpages}cursor.html"
    grok_href_desktop_val = f"{link_prefix_for_subpages}grok.html"
    lovable_href_desktop_val = f"{link_prefix_for_subpages}lovable.html"
    news_href_desktop_val = f"{link_prefix_for_subpages}ai_news.html"

    home_href_mobile_val = logo_href_val
    chatgpt_href_mobile_val = f"{link_prefix_for_subpages}chatgpt.html"
    claude_href_mobile_val = f"{link_prefix_for_subpages}claude.html"
    cursor_href_mobile_val = f"{link_prefix_for_subpages}cursor.html"
    grok_href_mobile_val = f"{link_prefix_for_subpages}grok.html"
    lovable_href_mobile_val = f"{link_prefix_for_subpages}lovable.html"
    news_href_mobile_val = f"{link_prefix_for_subpages}ai_news.html"
    shop_href_mobile_val = f"{link_prefix_for_subpages}shop.html"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(file_path)
        active_page_category = determine_active_page(filename)
        
        active_home = ' active' if active_page_category == 'home' else ''
        active_chatgpt = ' active' if active_page_category == 'chatgpt' else ''
        active_claude = ' active' if active_page_category == 'claude' else ''
        active_cursor = ' active' if active_page_category == 'cursor' else ''
        active_grok = ' active' if active_page_category == 'grok' else ''
        active_lovable = ' active' if active_page_category == 'lovable' else ''
        active_news = ' active' if active_page_category == 'news' else ''
        
        new_nav = nav_template.format(
            logo_href=logo_href_val,
            logo_img_src=logo_img_src_val,
            
            home_href_desktop=home_href_desktop_val,
            chatgpt_href_desktop=chatgpt_href_desktop_val,
            claude_href_desktop=claude_href_desktop_val,
            cursor_href_desktop=cursor_href_desktop_val,
            grok_href_desktop=grok_href_desktop_val,
            lovable_href_desktop=lovable_href_desktop_val,
            news_href_desktop=news_href_desktop_val,
            
            home_href_mobile=home_href_mobile_val,
            chatgpt_href_mobile=chatgpt_href_mobile_val,
            claude_href_mobile=claude_href_mobile_val,
            cursor_href_mobile=cursor_href_mobile_val,
            grok_href_mobile=grok_href_mobile_val,
            lovable_href_mobile=lovable_href_mobile_val,
            news_href_mobile=news_href_mobile_val,
            shop_href_mobile=shop_href_mobile_val,

            active_home=active_home,
            active_chatgpt=active_chatgpt,
            active_claude=active_claude,
            active_cursor=active_cursor,
            active_grok=active_grok,
            active_lovable=active_lovable,
            active_news=active_news
        )
        
        nav_pattern = r'<!-- 导航栏 -->.*?<!-- 移动端导航菜单 -->\s*</nav>'
        # A more robust pattern to match the entire nav structure including the mobile nav
        nav_pattern_full = r'<!-- 导航栏 -->.*?<nav class="mobile-nav">.*?</nav>'
        
        if re.search(nav_pattern_full, content, re.DOTALL):
            content = re.sub(nav_pattern_full, new_nav.strip(), content, flags=re.DOTALL)
        else:
            # Fallback to simpler pattern if the full one isn't found (e.g., if mobile nav was missing)
            nav_pattern_simple_desktop = r'<nav class="nav">.*?</nav>'
            if re.search(nav_pattern_simple_desktop, content, re.DOTALL):
                 # This might leave mobile nav if it exists and isn't part of the new_nav block
                 # For safety, we should ensure new_nav contains both desktop and mobile.
                 # The new_nav template already includes both.
                content = re.sub(nav_pattern_simple_desktop, new_nav.strip(), content, flags=re.DOTALL, count=1) # Replace only the first main nav
            else:
                print(f"  警告: 在 {file_path} 中找不到导航结构")
                return False
        
        if 'mobile-nav.js' not in content:
            if 'common.js' in content:
                content = content.replace(
                    '<script src="../assets/js/common.js"></script>',
                    '<script src="../assets/js/common.js"></script>\n  <script src="../assets/js/mobile-nav.js"></script>'
                )
            elif 'theme-toggle.js' in content:
                content = content.replace(
                    '<script src="../assets/js/theme-toggle.js"></script>',
                    '<script src="../assets/js/theme-toggle.js"></script>\n  <script src="../assets/js/mobile-nav.js"></script>'
                )
            else:
                # Attempt to add before </body> if other scripts not found
                if '</body>' in content:
                    js_script_path = 'assets/js/mobile-nav.js' if is_root_index else '../assets/js/mobile-nav.js'
                    content = content.replace('</body>', f'  <script src="{js_script_path}"></script>\n</body>')
            else:
                print(f"  警告: 在 {file_path} 中找不到合适的位置添加mobile-nav.js")
        
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
        print() # Add a newline for better readability between page updates
    
    print(f"\n更新完成！成功: {success_count}/{len(pages_to_update)}")

if __name__ == "__main__":
    main() 