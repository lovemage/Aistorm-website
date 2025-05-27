// Header 导航栏统一管理
class HeaderManager {
  constructor() {
    this.isSubPage = this.detectPageType();
    this.headerRendered = false; // 标记Header是否已渲染
    // DOMContentLoaded 事件监听器只添加一次
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.init(), { once: true });
    } else {
      this.init();
    }
  }

  // 检测是否为子页面
  detectPageType() {
    return window.location.pathname.includes('/pages/');
  }

  // 获取资源路径前缀
  getPathPrefix() {
    return this.isSubPage ? '../' : '';
  }

  // 生成header HTML
  generateHeaderHTML() {
    const pathPrefix = this.getPathPrefix();
    const navPrefix = this.isSubPage ? '../pages/' : 'pages/';
    const homeLink = this.isSubPage ? '../index.html' : 'index.html';
    const contactLink = this.isSubPage ? '../index.html#contact' : '#contact';
    
    return `
      <header>
        <div class="container">
          <div class="header-content">
            <div class="logo-section">
              <img src="${pathPrefix}assets/images/logo.png" alt="AIStorm Logo">
              <div class="logo-text">AIStorm</div>
            </div>
            <nav class="desktop-nav">
              <a href="${homeLink}">首页</a>
              <a href="${navPrefix}chatgpt.html">ChatGPT Pro</a>
              <a href="${navPrefix}claude.html">Claude Max 5x</a>
              <a href="${navPrefix}grok.html">Super Grok</a>
              <a href="${navPrefix}cursor.html">Cursor Pro</a>
              <a href="${navPrefix}lovable.html">Lovable Pro</a>
              <a href="${navPrefix}about.html">关于我们</a>
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
              <a href="${navPrefix}chatgpt.html">ChatGPT Pro</a>
              <a href="${navPrefix}claude.html">Claude Max 5x</a>
              <a href="${navPrefix}grok.html">Super Grok</a>
              <a href="${navPrefix}cursor.html">Cursor Pro</a>
              <a href="${navPrefix}lovable.html">Lovable Pro</a>
              <a href="${navPrefix}about.html">关于我们</a>
              <a href="${contactLink}">联系我们</a>
            </nav>
          </div>
        </div>
      </header>
    `;
  }

  // 初始化header的入口，由 DOMContentLoaded 或直接调用
  init() {
    if (this.headerRendered) {
      console.log('Header init: Already rendered, skipping.');
      return;
    }
    this.renderHeader();
  }

  // 渲染header
  renderHeader() {
    if (this.headerRendered) {
      console.log('Header renderHeader: Already rendered, skipping.');
      return;
    }
    console.log('Header renderHeader: Rendering header...');
    console.log('Header renderHeader: Initial body innerHTML (first 500 chars):', document.body.innerHTML.substring(0, 500));

    const existingHeaders = document.querySelectorAll('header');
    existingHeaders.forEach(header => {
      console.log('Removing existing header:', header);
      header.remove();
    });
    console.log('Header renderHeader: Body innerHTML after removing <header>s (first 500 chars):', document.body.innerHTML.substring(0, 500));

    const directBodyNavs = document.querySelectorAll('body > nav');
    directBodyNavs.forEach(nav => {
      console.log('Removing direct body nav:', nav);
      nav.remove();
    });
    console.log('Header renderHeader: Body innerHTML after removing body > navs (first 500 chars):', document.body.innerHTML.substring(0, 500));
    
    // Before inserting the new header, let's check the state again
    // This is a critical point to see if any unexpected nav-like structure is present
    /*
    const navLinkTexts = ['首页', 'ChatGPT Pro', 'Claude Max 5x', 'Super Grok', 'Cursor Pro', 'Lovable Pro', '关于我们', '联系我们'];
    const bodyChildren = Array.from(document.body.children);
    if (bodyChildren.length > 0) {
        const firstFewChildren = bodyChildren.slice(0, 5); // Check first 5 children
        console.log('Header renderHeader: Checking first few children of body before inserting new header:', firstFewChildren);
        firstFewChildren.forEach((child, index) => {
            const childText = child.textContent || "";
            let matchCount = 0;
            for (const text of navLinkTexts) {
                if (childText.includes(text)) {
                    matchCount++;
                }
            }
            if (matchCount >= 2 && child.tagName !== 'SCRIPT' && child.tagName !== 'LINK' && child.tagName !== 'STYLE') {
                console.warn('Header renderHeader: Suspicious nav-like element found before new header insertion:', child);
                // Optionally, we could try to remove it here if it's consistently problematic
                // child.remove();
                // console.log('Header renderHeader: Removed suspicious element.');
                // console.log('Header renderHeader: Body innerHTML after removing suspicious element (first 500 chars):', document.body.innerHTML.substring(0, 500));
            }
        });
    }
    */

    const headerHTML = this.generateHeaderHTML();
    document.body.insertAdjacentHTML('afterbegin', headerHTML);
    console.log('Header renderHeader: Body innerHTML after inserting new header (first 500 chars):', document.body.innerHTML.substring(0, 500));
    
    this.headerRendered = true;
    console.log('Header renderHeader: Header rendered successfully.');
    
    this.initMobileNav();
  }

  // 初始化移动端导航功能
  initMobileNav() {
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');
    
    if (mobileMenuToggle && mobileNav) {
      // 移除旧的事件监听器，防止重复绑定
      const newMobileMenuToggle = mobileMenuToggle.cloneNode(true);
      mobileMenuToggle.parentNode.replaceChild(newMobileMenuToggle, mobileMenuToggle);
      
      newMobileMenuToggle.addEventListener('click', function() {
        this.classList.toggle('active');
        mobileNav.classList.toggle('active');
      });
      
      const mobileNavLinks = mobileNav.querySelectorAll('a');
      mobileNavLinks.forEach(link => {
        const newLink = link.cloneNode(true); // 移除旧监听器
        link.parentNode.replaceChild(newLink, link);
        newLink.addEventListener('click', function() {
          document.querySelector('.mobile-menu-toggle').classList.remove('active');
          mobileNav.classList.remove('active');
        });
      });
      
      document.addEventListener('click', function(event) {
        const currentMobileMenuToggle = document.querySelector('.mobile-menu-toggle'); 
        if (currentMobileMenuToggle && !currentMobileMenuToggle.contains(event.target) && !mobileNav.contains(event.target)) {
          currentMobileMenuToggle.classList.remove('active');
          mobileNav.classList.remove('active');
        }
      });
      
      document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
          const currentMobileMenuToggle = document.querySelector('.mobile-menu-toggle'); 
          if (currentMobileMenuToggle) {
            currentMobileMenuToggle.classList.remove('active');
          }
          mobileNav.classList.remove('active');
        }
      });
       console.log('Mobile nav initialized.');
    } else {
      console.log('Mobile nav elements not found.');
    }
  }
}

// 自动初始化header
// 确保 HeaderManager 实例只创建一次
if (!window.headerManagerInstance) {
  window.headerManagerInstance = new HeaderManager();
} 