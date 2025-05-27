// Footer 统一管理
class FooterManager {
  constructor() {
    this.isSubPage = this.detectPageType();
  }

  // 检测是否为子页面
  detectPageType() {
    return window.location.pathname.includes('/pages/');
  }

  // 获取资源路径前缀
  getPathPrefix() {
    return this.isSubPage ? '../' : '';
  }

  // 生成footer HTML
  generateFooterHTML() {
    const pathPrefix = this.getPathPrefix();
    const pageLinkPrefix = this.isSubPage ? '../pages/' : 'pages/';
    const homeLinkPrefix = this.isSubPage ? '../' : '';

    return `
      <footer>
        <div class="container">
          <div class="footer-content">
            <div class="footer-section">
              <h4>AIStorm 产品</h4>
              <a href="${pageLinkPrefix}chatgpt.html">ChatGPT Pro 账号</a>
              <a href="${pageLinkPrefix}claude.html">Claude Max 5x 账号</a>
              <a href="${pageLinkPrefix}grok.html">Super Grok 账号</a>
              <a href="${pageLinkPrefix}cursor.html">Cursor Pro 账号</a>
              <a href="${pageLinkPrefix}lovable.html">Lovable Pro 账号</a>
            </div>
            <div class="footer-section">
              <h4>客户支持</h4>
              <a href="https://t.me/aistorm2025" target="_blank" rel="noopener noreferrer">联系客服团队</a>
              <a href="${pageLinkPrefix}faq.html">常见问题解答</a>
              <a href="${pageLinkPrefix}tutorials.html">使用教学指南</a>
              <a href="${pageLinkPrefix}support.html">售后技术支持</a>
            </div>
            <div class="footer-section">
              <h4>法律条款</h4>
              <a href="${pageLinkPrefix}privacy.html">隐私政策</a>
              <a href="${pageLinkPrefix}terms.html">服务条款</a>
              <a href="${pageLinkPrefix}refund.html">退款政策</a>
              <a href="${pageLinkPrefix}about.html">关于我们</a>
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