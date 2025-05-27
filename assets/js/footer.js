// Footer 统一管理
class FooterManager {
  constructor() {
    this.isSubPage = this.detectPageType();
  }

  // 检测当前页面类型（主页还是子页面）
  detectPageType() {
    const currentPath = window.location.pathname;
    return currentPath.includes('/pages/') || currentPath.includes('pages/');
  }

  // 获取正确的路径前缀
  getPathPrefix() {
    return this.isSubPage ? '../' : 'pages/';
  }

  // 生成footer HTML
  generateFooterHTML() {
    const pathPrefix = this.getPathPrefix();
    const indexPath = this.isSubPage ? '../index.html#products' : '#products';
    
    return `
      <footer>
        <div class="container">
          <div class="footer-content">
            <div class="footer-section">
              <h4>AIStorm 产品</h4>
              <a href="${pathPrefix}chatgpt.html">ChatGPT Pro 账号</a>
              <a href="${pathPrefix}claude.html">Claude Max 5x 账号</a>
              <a href="${pathPrefix}grok.html">Super Grok 账号</a>
              <a href="${pathPrefix}cursor.html">Cursor Pro 账号</a>
              <a href="${pathPrefix}lovable.html">Lovable Pro 账号</a>
              <a href="${indexPath}">查看所有AI解决方案</a>
            </div>
            <div class="footer-section">
              <h4>客户支持</h4>
              <a href="https://t.me/aistorm2025" target="_blank" rel="noopener noreferrer">联系客服团队</a>
              <a href="${pathPrefix}faq.html">常见问题解答</a>
              <a href="${pathPrefix}tutorials.html">使用教学指南</a>
              <a href="${pathPrefix}support.html">售后技术支持</a>
            </div>
          </div>
          <div style="border-top: 1px solid rgba(0, 229, 255, 0.15); padding-top: 1.5rem; margin-top: 2rem;">
            <p class="footer-bottom-text">© 2025 AIStorm. All Rights Reserved. | 您的专业AI账号服务与解决方案伙伴。</p>
          </div>
        </div>
      </footer>
    `;
  }

  // 初始化footer
  init() {
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.renderFooter());
    } else {
      this.renderFooter();
    }
  }

  // 渲染footer
  renderFooter() {
    // 查找现有的footer元素
    const existingFooter = document.querySelector('footer');
    
    if (existingFooter) {
      // 如果存在footer，替换其内容
      existingFooter.outerHTML = this.generateFooterHTML();
    } else {
      // 如果不存在footer，在body末尾添加
      document.body.insertAdjacentHTML('beforeend', this.generateFooterHTML());
    }
  }
}

// 自动初始化footer
const footerManager = new FooterManager();
footerManager.init(); 