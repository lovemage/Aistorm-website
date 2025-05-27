#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob

# Dictionary for Traditional Chinese to Simplified Chinese conversion
traditional_to_simplified_map = {
    '常見問題解答': '常见问题解答',
    '關於我們': '关于我们',
    '服務條款': '服务条款',
    '隐私政策': '隐私政策',
    '退款政策': '退款政策',
    '教學指南': '教学指南',
    '技術支持': '技术支持',
    '聯絡我們': '联系我们',
    '首頁': '首页',
    '產品': '产品',
    '账号': '账号', # Common case, ensure it's simplified
    '购买': '购买', # Common case
    '体验': '体验', # Common case
    '强大': '强大', # Common case
    '支持': '支持', # Common case
    '官方': '官方', # Common case
    '指定': '指定', # Common case
    '功能': '功能', # Common case
    '模型': '模型', # Common case
    '处理': '处理', # Common case
    '任务': '任务', # Common case
    '提升': '提升', # Common case
    '创造力': '创造力', # Common case
    '释放': '释放', # Common case
    '潜能': '潜能', # Common case
    '效率': '效率', # Common case
    '安全': '安全', # Common case
    '快速': '快速', # Common case
    '支付': '支付', # Common case
    '小时': '小时', # Common case
    '客服': '客服', # Common case
    '团队': '团队', # Common case
    '选择': '选择', # Common case
    '立即购买': '立即购买',
    '了解更多': '了解更多',
    'AI解决方案': 'AI解决方案',
    '专业AI服务': '专业AI服务',
    '全球用户': '全球用户',
    '人工智能': '人工智能',
    '科技创新': '科技创新',
    '企业使命': '企业使命',
    '使用教學': '使用教学',
    '您的专业AI账号服务与解决方案伙伴': '您的专业AI账号服务与解决方案伙伴',
    '释放 Claude Max 5x：Anthropic 顶尖AI的强劲动力': '释放 Claude Max 5x：Anthropic 顶尖AI的强劲动力',
    '释放 ChatGPT Pro 的力量：OpenAI 的高级 AI 服务': '释放 ChatGPT Pro 的力量：OpenAI 的高级 AI 服务',
    '释放 Cursor Pro：AI 驱动的编码体验': '释放 Cursor Pro：AI 驱动的编码体验',
    '释放 Super Grok：您的高级 AI 伙伴': '释放 Super Grok：您的高级 AI 伙伴',
    '释放 Lovable Pro：AI 驱动的客户关系管理': '释放 Lovable Pro：AI 驱动的客户关系管理',
    'Claude Max 5x 服务详情': 'Claude Max 5x 服务详情',
    'ChatGPT Pro 服务详情': 'ChatGPT Pro 服务详情',
    'Cursor Pro 服务详情': 'Cursor Pro 服务详情',
    'Super Grok 服务详情': 'Super Grok 服务详情',
    'Lovable Pro 服务详情': 'Lovable Pro 服务详情',
    '最新AI技术': '最新AI技术',
    '稳定可靠': '稳定可靠',
    '客户服务': '客户服务',
    '即时访问': '即时访问',
    '我们的客户评价': '我们的客户评价',
    '常問問題': '常见问题',
    '瞭解更多': '了解更多',
    '點擊這裡': '点击这里',
    '查看全部': '查看全部',
    '訂閱我們的新聞通訊': '订阅我们的新闻通讯',
    '獲取有關我們最新產品和特別優惠的更新。': '获取有关我们最新产品和特别优惠的更新。',
    '您的電子郵件地址': '您的电子邮件地址',
    '訂閱': '订阅',
    '引導您完成AI整合之旅的每一步。': '引导您完成AI整合之旅的每一步。',
    '我們是誰': '我们是谁',
    '我們的使命': '我们的使命',
    '我們的願景': '我们的愿景',
    '我們的價值觀': '我们的价值观',
    '創新': '创新',
    '客戶至上': '客户至上',
    '誠信': '诚信',
    '卓越': '卓越',
    '协作': '协作', # Simplified form
    '協作': '协作', # Traditional form to cover
    '為什麼選擇AIStorm？': '为什么选择AIStorm？',
    '加入我們的旅程': '加入我们的旅程',
    '聯繫我們': '联系我们',
    '有任何問題或想進一步了解我們的服務嗎？請隨時與我們聯繫。': '有任何问题或想进一步了解我们的服务吗？请随时与我们联系。',
    '發送訊息': '发送讯息', # Simplified: 发送信息 - but keeping user's likely intent
    '讯息': '讯息', # Ensure this is handled if it appears alone
    '信息': '信息', # Target for "讯息"
    '您的名字': '您的名字',
    '您的電子郵件': '您的电子邮件',
    '主旨': '主题',
    '您的訊息': '您的讯息', # Will become "您的信息"
    '购买 Claude Max 5x 账号 - Claude-3 Opus 強力支持 | AIStorm 官方': '购买 Claude Max 5x 账号 - Claude-3 Opus 强力支持 | AIStorm 官方',
    '购买 ChatGPT Pro 账号 - GPT-4 強力驅動 | AIStorm 官方指定': '购买 ChatGPT Pro 账号 - GPT-4 强力驱动 | AIStorm 官方指定',
    '购买 Super Grok 账号 - 先進AI智能助理 | AIStorm 官方': '购买 Super Grok 账号 - 先进AI智能助理 | AIStorm 官方',
    '购买 Cursor Pro 账号 - AI輔助程式設計利器 | AIStorm 官方': '购买 Cursor Pro 账号 - AI辅助程式设计利器 | AIStorm 官方',
    '购买 Lovable Pro 账号 - AI驅動客戶關係管理 | AIStorm 官方': '购买 Lovable Pro 账号 - AI驱动客户关系管理 | AIStorm 官方',
    '描述': '描述',
    '條款': '条款',
    '細節': '细节',
    '概覽': '概览',
    '其他資訊': '其他资讯', # Simplified: 其他信息
    '價格': '价格',
    '退款和換貨政策': '退款和换货政策',
    '符合條件的退款': '符合条件的退款',
    '如何申請退款': '如何申请退款',
    '處理時間': '处理时间',
    '聯繫資訊': '联系资讯',
    '政策變更': '政策变更',
    '最後更新日期': '最后更新日期',
    '一般條款': '一般条款',
    '帳戶註冊與使用': '帐户注册与使用',
    '禁止行為': '禁止行为',
    '知識產權': '知识产权',
    '終止服務': '终止服务',
    '免責聲明': '免责声明',
    '責任限制': '责任限制',
    '適用法律與管轄權': '适用法律与管辖权',
    '條款修改': '条款修改',
    '用户指南和教程': '用户指南和教程',
    '入门指南': '入门指南',
    '高级功能': '高级功能',
    '故障排除': '故障排除',
    '视频教程': '视频教程',
    '联系支持': '联系支持',
    '提交支持请求': '提交支持请求',
    '我们的支持渠道': '我们的支持渠道',
    '服务时间': '服务时间',
    '预计响应时间': '预计响应时间',
    '浏览我们的教程': '浏览我们的教程',
    '获取实时帮助': '获取实时帮助',
    '查看我们的FAQ': '查看我们的FAQ',
    # Add more specific translations as identified from files
}

def t2s(text, mapping_dict):
    for traditional, simplified in mapping_dict.items():
        text = text.replace(traditional, simplified)
    # Specific fix for "讯息" to "信息" after general replacements
    text = text.replace('讯息', '信息')
    text = text.replace('軟體', '软件')
    text = text.replace('硬體', '硬件')
    text = text.replace('數位', '数字')
    text = text.replace('網路', '网络')
    text = text.replace('鏈接', '链接')
    text = text.replace('下載', '下载')
    text = text.replace('游戲', '游戏')
    text = text.replace('計畫', '计划')
    text = text.replace('項目', '项目')
    return text

def clean_css_in_html(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return

    style_block_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    if not style_block_match:
        # print(f"No <style> block found in {filepath}")
        return

    original_style_content = style_block_match.group(1)
    cleaned_style_content = original_style_content

    patterns_to_remove = [
        r'\.header-content\s*\{[^\}]*\}\s*',
        r'\.logo-section\s*\{[^\}]*\}\s*',
        r'\.logo-text\s*\{[^\}]*\}\s*',
        r'(?<!\.some-class-)nav\s*\{[^\}]*\}\s*', # Avoid matching things like .mobile-nav if specific
        r'(?<!\.some-class-)nav\s+a\s*\{[^\}]*\}\s*',
        r'\.desktop-nav\s*\{[^\}]*\}\s*',
        r'\.desktop-nav\s+a\s*\{[^\}]*\}\s*',
        # More specific mobile nav elements if they are distinct from header.css or mobile-nav.css
        # r'\.mobile-menu-toggle\s*\{[^\}]*\}\s*', # Keep if mobile-nav.css doesn't cover all states
        # r'\.hamburger-line\s*\{[^\}]*\}\s*',  # Keep if mobile-nav.css doesn't cover all states
        # r'\.mobile-nav\s*\{[^\}]*\}\s*', # Keep if this is the main container styled by mobile-nav.css
        # r'\.mobile-nav\s+a\s*\{[^\}]*\}\s*',
        # Catch variations like "nav a:hover, nav a.active"
        r'(?<!\.some-class-)nav\s+a:hover\s*,\s*(?<!\.some-class-)nav\s+a\.active\s*\{[^\}]*\}\s*',
        r'\.desktop-nav\s+a:hover\s*,\s*\.desktop-nav\s+a\.active\s*\{[^\}]*\}\s*',
        # r'\.mobile-nav\s+a:hover\s*,\s*\.mobile-nav\s+a\.active\s*\{[^\}]*\}\s*', # Covered by mobile-nav.css
        # Remove comments that might be associated with these rules
        r'/\*\s*Header样式已移至统一CSS文件\s*\*/\s*',
        r'/\*\s*桌面端导航\s*\*/\s*',
        # r'/\*\s*移动端汉堡菜单按钮\s*\*/\s*', # Keep if specific styling remains for it
        # r'/\*\s*移动端下拉菜单\s*\*/\s*',   # Keep if specific styling remains for it
        r'/\*\s*重复的header-content样式已移除\s*\*/\s*',
    ]

    for pattern in patterns_to_remove:
        cleaned_style_content = re.sub(pattern, '', cleaned_style_content, flags=re.IGNORECASE | re.DOTALL)

    # Remove media query blocks ONLY if they become completely empty or just whitespace/comments
    # This regex looks for @media blocks that contain only whitespace or comments.
    cleaned_style_content = re.sub(r'@media\s*\([^\)]*\)\s*\{\s*(\/\*.*?\*\/\s*)*\s*\}\s*', '', cleaned_style_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remove multiple empty lines from the cleaned style content but ensure one newline before non-empty lines.
    cleaned_style_content = re.sub(r'(\n\s*){2,}', '\n', cleaned_style_content)
    cleaned_style_content = cleaned_style_content.strip()


    if cleaned_style_content.strip() != original_style_content.strip():
        if not cleaned_style_content.strip(): 
            # If style content is empty, put a comment placeholder
            new_style_block = '<style>\n    /* All redundant inline styles removed. Global CSS files should handle styling. */\n  </style>'
            content = content.replace(style_block_match.group(0), new_style_block)
            print(f"Cleaned (all rules removed) CSS in {filepath}")
        else:
            # Otherwise, replace with the cleaned content
            new_style_block = '<style>\n' + cleaned_style_content + '\n  </style>'
            content = content.replace(style_block_match.group(0), new_style_block)
            print(f"Cleaned CSS in {filepath}")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    # else:
        # print(f"No CSS changes made to {filepath}")

def process_html_file(filepath, lang_map):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return

    original_content = content

    # 1. Language Conversion (繁体 to 简体)
    content = t2s(content, lang_map)
    if content != original_content:
        print(f"Performed language conversion for {filepath}")
    
    # 2. Clean inline CSS
    # Temporarily store content after lang conversion to pass to clean_css_in_html
    # This is a bit tricky as clean_css_in_html reads the file itself.
    # For simplicity here, we'll write the lang-converted content first, then clean CSS.
    # This means clean_css_in_html will operate on the language-converted version.
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    clean_css_in_html(filepath) # This function now reads and writes the file

    # Read the content again after clean_css_in_html might have modified it
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 3. Ensure correct asset links and script tags
    # header.css
    header_css_link = '<link rel="stylesheet" href="../assets/css/header.css">'
    if header_css_link not in content and '<link rel="stylesheet" href="assets/css/header.css">' not in content : # check if not already correct
        # Ensure it's not the incorrect root path for subpages
        incorrect_header_css_link = '<link rel="stylesheet" href="assets/css/header.css">'
        if incorrect_header_css_link in content and "/pages/" in filepath:
             content = content.replace(incorrect_header_css_link, header_css_link, 1)
             print(f"Corrected header.css link in {filepath}")
        elif '<title>' in content:
            content = content.replace('</title>', '</title>\n  ' + header_css_link, 1)
            print(f"Added header.css link to {filepath}")
        else: # Fallback
            content = content.replace('<head>', '<head>\n  ' + header_css_link, 1)
            print(f"Added header.css link (fallback) to {filepath}")


    # mobile-nav.css
    mobile_nav_css_link = '<link rel="stylesheet" href="../assets/css/mobile-nav.css">'
    incorrect_mobile_nav_css_pattern = r'<link rel="stylesheet" href="assets/css/mobile-nav.css">'
    if "/pages/" in filepath: # Only for files in /pages/ directory
        if re.search(incorrect_mobile_nav_css_pattern, content):
            content = re.sub(incorrect_mobile_nav_css_pattern, mobile_nav_css_link, content, 1)
            print(f"Corrected mobile-nav.css link in {filepath}")
        elif mobile_nav_css_link not in content:
            if header_css_link in content: # Insert after header.css
                content = content.replace(header_css_link, header_css_link + '\n  ' + mobile_nav_css_link, 1)
            elif '<title>' in content: # Fallback to after title
                content = content.replace('</title>', '</title>\n  ' + mobile_nav_css_link, 1)
            else: # Absolute fallback
                content = content.replace('<head>', '<head>\n  ' + mobile_nav_css_link, 1)
            print(f"Added mobile-nav.css link to {filepath}")
    else: # For root files like index.html
        correct_root_mobile_nav_css = '<link rel="stylesheet" href="assets/css/mobile-nav.css">'
        if correct_root_mobile_nav_css not in content:
            if '<link rel="stylesheet" href="assets/css/header.css">' in content:
                 content = content.replace('<link rel="stylesheet" href="assets/css/header.css">', '<link rel="stylesheet" href="assets/css/header.css">' + '\n  ' + correct_root_mobile_nav_css, 1)
            elif '<title>' in content:
                 content = content.replace('</title>', '</title>\n  ' + correct_root_mobile_nav_css, 1)
            else:
                 content = content.replace('<head>', '<head>\n  ' + correct_root_mobile_nav_css, 1)
            print(f"Added mobile-nav.css link to {filepath} (root)")


    # Favicon
    favicon_link_sub = '<link rel="icon" href="../assets/images/logo.png">'
    favicon_link_root = '<link rel="icon" href="assets/images/logo.png">'
    correct_favicon_link = favicon_link_sub if "/pages/" in filepath else favicon_link_root
    
    incorrect_favicon_pattern_sub = r'<link rel="icon" href="assets/images/logo.png">' # if in pages/
    incorrect_favicon_pattern_root = r'<link rel="icon" href="../assets/images/logo.png">' # if in root and wrongly ../

    if "/pages/" in filepath:
        if re.search(incorrect_favicon_pattern_sub, content):
            content = re.sub(incorrect_favicon_pattern_sub, correct_favicon_link, content, 1)
            print(f"Corrected favicon link in {filepath}")
        elif correct_favicon_link not in content:
            if '<title>' in content: content = content.replace('</title>', '</title>\n  ' + correct_favicon_link, 1)
            else: content = content.replace('<head>', '<head>\n  ' + correct_favicon_link, 1)
            print(f"Added favicon link to {filepath}")
    else: # Root file
        if re.search(incorrect_favicon_pattern_root, content):
            content = re.sub(incorrect_favicon_pattern_root, correct_favicon_link, content, 1)
            print(f"Corrected favicon link in {filepath} (root)")
        elif correct_favicon_link not in content:
            if '<title>' in content: content = content.replace('</title>', '</title>\n  ' + correct_favicon_link, 1)
            else: content = content.replace('<head>', '<head>\n  ' + correct_favicon_link, 1)
            print(f"Added favicon link to {filepath} (root)")


    # Scripts: header.js, footer.js
    header_script_sub = '<script src="../assets/js/header.js"></script>'
    footer_script_sub = '<script src="../assets/js/footer.js"></script>'
    header_script_root = '<script src="assets/js/header.js"></script>'
    footer_script_root = '<script src="assets/js/footer.js"></script>'

    correct_header_script = header_script_sub if "/pages/" in filepath else header_script_root
    correct_footer_script = footer_script_sub if "/pages/" in filepath else footer_script_root

    # Remove any existing versions (correct or incorrect paths, multiple times)
    # Regex to match script tags for header.js or footer.js with any path starting with assets/ or ../assets/
    content = re.sub(r'<script\s+src=["'](?:\.\./)?assets/js/(?:header|footer)\.js["']></script>\s*', '', content)

    # Add them back correctly before </body>
    scripts_to_add = f"\n  {correct_header_script}\n  {correct_footer_script}\n</body>"
    if '</body>' in content:
        content = content.replace('</body>', scripts_to_add, 1)
        # print(f"Ensured header.js and footer.js scripts in {filepath}")
    else:
        content += f"\n{correct_header_script}\n{correct_footer_script}" # Fallback
        # print(f"Appended header.js and footer.js scripts to {filepath} (no body tag found)")

    # mobile-nav.js (only correct path if exists, don't add if missing)
    mobile_nav_js_sub = '<script src="../assets/js/mobile-nav.js"></script>'
    mobile_nav_js_root = '<script src="assets/js/mobile-nav.js"></script>'
    correct_mobile_nav_js = mobile_nav_js_sub if "/pages/" in filepath else mobile_nav_js_root
    
    incorrect_mobile_nav_js_pattern_sub = r'<script src="assets/js/mobile-nav.js"></script>'
    incorrect_mobile_nav_js_pattern_root = r'<script src="../assets/js/mobile-nav.js"></script>'

    if "/pages/" in filepath:
        if re.search(incorrect_mobile_nav_js_pattern_sub, content):
            content = re.sub(incorrect_mobile_nav_js_pattern_sub, correct_mobile_nav_js, content, 1)
            print(f"Corrected mobile-nav.js script link in {filepath}")
    else: # Root file
         if re.search(incorrect_mobile_nav_js_pattern_root, content):
            content = re.sub(incorrect_mobile_nav_js_pattern_root, correct_mobile_nav_js, content, 1)
            print(f"Corrected mobile-nav.js script link in {filepath} (root)")


    if content != original_content: # Check if any changes (lang, css, links, scripts) were made
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"File {filepath} updated with various fixes.")
    # else:
    #     print(f"No changes needed for {filepath} after all checks.")


def main():
    print("Starting website issue fixing script...")
    
    # Process pages in /pages/ directory
    pages_dir = 'pages'
    if os.path.isdir(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(pages_dir, filename)
                print(f"--- Processing sub-page: {filepath} ---")
                process_html_file(filepath, traditional_to_simplified_map)
    else:
        print(f"Directory '{pages_dir}' not found.")

    # Process index.html in the root directory
    index_file_path = 'index.html'
    if os.path.exists(index_file_path):
        print(f"--- Processing root page: {index_file_path} ---")
        process_html_file(index_file_path, traditional_to_simplified_map)
    else:
        print(f"File '{index_file_path}' not found in root directory.")
    
    print("\nScript finished. Please review the changes and test the website.")

if __name__ == '__main__':
    main() 