// Header 导航栏统一管理
class HeaderManager {
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
    return this.isSubPage ? '../' : '';
  }

  // 获取页面路径前缀（用于导航链接）
  getNavPathPrefix() {
    return this.isSubPage ? '../' : 'pages/';
  }

  // 生成header HTML
  generateHeaderHTML() {
    const pathPrefix = this.getPathPrefix();
    const navPathPrefix = this.getNavPathPrefix();
    const homeLink = this.isSubPage ? '../index.html' : '/';
    const contactLink = this.isSubPage ? '../index.html#contact' : '#contact';
    
    return `
      <header>
        <div class="container">
          <div class="header-content">
            <div class="logo-section">
              <a href="${homeLink}" style="display: flex; align-items: center; gap: 15px; text-decoration: none;">
                <img src="${pathPrefix}assets/images/logo.png" alt="AIStorm Logo">
                <div class="logo-text">AIStorm</div>
              </a>
            </div>
            <nav class="desktop-nav">
              <a href="${homeLink}">首页</a>
              <a href="${navPathPrefix}chatgpt.html">ChatGPT Pro</a>
              <a href="${navPathPrefix}claude.html">Claude Max 5x</a>
              <a href="${navPathPrefix}grok.html">Super Grok</a>
              <a href="${navPathPrefix}cursor.html">Cursor Pro</a>
              <a href="${navPathPrefix}lovable.html">Lovable Pro</a>
              <a href="${navPathPrefix}about.html">关于我们</a>
              <a href="${contactLink}">联系我们</a>
            </nav>
            
            <!-- 移动端汉堡菜单按钮 -->
            <button class="mobile-menu-toggle" aria-label="切换菜单">
              <span class="hamburger-line"></span>
              <span class="hamburger-line"></span>
              <span class="hamburger-line"></span>
            </button>
            
            <!-- 移动端下拉菜单 -->
            <nav class="mobile-nav">
              <a href="${homeLink}">首页</a>
              <a href="${navPathPrefix}chatgpt.html">ChatGPT Pro</a>
              <a href="${navPathPrefix}claude.html">Claude Max 5x</a>
              <a href="${navPathPrefix}grok.html">Super Grok</a>
              <a href="${navPathPrefix}cursor.html">Cursor Pro</a>
              <a href="${navPathPrefix}lovable.html">Lovable Pro</a>
              <a href="${navPathPrefix}about.html">关于我们</a>
              <a href="${contactLink}">联系我们</a>
            </nav>
          </div>
        </div>
      </header>
    `;
  }

  // 初始化header
  init() {
    // 等待DOM加载完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.renderHeader());
    } else {
      this.renderHeader();
    }
  }

  // 渲染header
  renderHeader() {
    // 查找现有的header元素
    const existingHeader = document.querySelector('header');
    
    if (existingHeader) {
      // 如果存在header，替换其内容
      existingHeader.outerHTML = this.generateHeaderHTML();
    } else {
      // 如果不存在header，在body开头添加
      document.body.insertAdjacentHTML('afterbegin', this.generateHeaderHTML());
    }
    
    // 重新初始化移动端导航功能
    this.initMobileNav();
  }

  // 初始化移动端导航功能
  initMobileNav() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    
    if (mobileMenuToggle && mobileNav) {
      // 点击汉堡菜单按钮切换菜单
      mobileMenuToggle.addEventListener('click', function() {
        mobileMenuToggle.classList.toggle('active');
        mobileNav.classList.toggle('active');
      });
      
      // 点击菜单项后关闭菜单
      const mobileNavLinks = mobileNav.querySelectorAll('a');
      mobileNavLinks.forEach(link => {
        link.addEventListener('click', function() {
          mobileMenuToggle.classList.remove('active');
          mobileNav.classList.remove('active');
        });
      });
      
      // 点击页面其他地方关闭菜单
      document.addEventListener('click', function(event) {
        if (!mobileMenuToggle.contains(event.target) && !mobileNav.contains(event.target)) {
          mobileMenuToggle.classList.remove('active');
          mobileNav.classList.remove('active');
        }
      });
      
      // ESC键关闭菜单
      document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
          mobileMenuToggle.classList.remove('active');
          mobileNav.classList.remove('active');
        }
      });
    }
  }
}

// 自动初始化header
const headerManager = new HeaderManager();
headerManager.init(); 