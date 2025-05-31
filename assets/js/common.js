/**
 * AIStorm 通用功能模塊
 * 包含平滑滾動、目錄高亮、表單處理等通用功能
 */

class AIStormCommon {
  constructor() {
    this.init();
  }
  
  init() {
    // 等待 DOM 加載完成
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }
  
  setup() {
    this.initSmoothScroll();
    this.initTableOfContents();
    this.initLazyLoading();
    this.initFormEnhancements();
    this.initAccessibility();
    this.initPerformanceOptimizations();
  }
  
  /**
   * 平滑滾動功能
   */
  initSmoothScroll() {
    // 為所有錨點鏈接添加平滑滾動
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const targetId = anchor.getAttribute('href');
        
        // 空錨點或只有 # 的情況
        if (targetId === '#' || targetId === '') {
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
          return;
        }
        
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          
          // 計算偏移量（考慮固定導航欄）
          const offset = this.getScrollOffset();
          const targetPosition = target.offsetTop - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
          
          // 更新 URL 但不觸發跳轉
          if (history.pushState) {
            history.pushState(null, null, targetId);
          }
          
          // 可訪問性：設置焦點
          target.tabIndex = -1;
          target.focus();
        }
      });
    });
  }
  
  /**
   * 目錄高亮功能
   */
  initTableOfContents() {
    const tocLinks = document.querySelectorAll('.toc-link, .sidebar-toc a');
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    
    if (tocLinks.length === 0 || headings.length === 0) return;
    
    // 創建 Intersection Observer
    const observer = new IntersectionObserver((entries) => {
      let activeHeading = null;
      
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          activeHeading = entry.target;
        }
      });
      
      if (activeHeading) {
        this.updateActiveToC(activeHeading.id, tocLinks);
      }
    }, {
      rootMargin: '-20% 0px -80% 0px',
      threshold: 0
    });
    
    // 觀察所有標題
    headings.forEach(heading => {
      if (heading.id) {
        observer.observe(heading);
      }
    });
  }
  
  updateActiveToC(activeId, tocLinks) {
    // 移除所有活躍狀態
    tocLinks.forEach(link => {
      link.classList.remove('active');
    });
    
    // 添加當前活躍狀態
    const activeLink = document.querySelector(`a[href="#${activeId}"]`);
    if (activeLink) {
      activeLink.classList.add('active');
    }
  }
  
  /**
   * 懶加載功能
   */
  initLazyLoading() {
    // 圖片懶加載
    const images = document.querySelectorAll('img[data-src]');
    
    if (images.length === 0) return;
    
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    }, {
      rootMargin: '50px'
    });
    
    images.forEach(img => imageObserver.observe(img));
  }
  
  /**
   * 表單增強功能
   */
  initFormEnhancements() {
    // 表單驗證
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
      // 實時驗證
      const inputs = form.querySelectorAll('input, textarea, select');
      inputs.forEach(input => {
        input.addEventListener('blur', () => this.validateField(input));
        input.addEventListener('input', () => this.clearFieldError(input));
      });
      
      // 表單提交
      form.addEventListener('submit', (e) => {
        if (!this.validateForm(form)) {
          e.preventDefault();
        }
      });
    });
  }
  
  validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // 必填驗證
    if (field.hasAttribute('required') && !value) {
      isValid = false;
      errorMessage = '此欄位為必填';
    }
    
    // 電子郵件驗證
    if (field.type === 'email' && value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        isValid = false;
        errorMessage = '請輸入有效的電子郵件地址';
      }
    }
    
    // 顯示錯誤或清除錯誤
    if (!isValid) {
      this.showFieldError(field, errorMessage);
    } else {
      this.clearFieldError(field);
    }
    
    return isValid;
  }
  
  validateForm(form) {
    const inputs = form.querySelectorAll('input, textarea, select');
    let isFormValid = true;
    
    inputs.forEach(input => {
      if (!this.validateField(input)) {
        isFormValid = false;
      }
    });
    
    return isFormValid;
  }
  
  showFieldError(field, message) {
    this.clearFieldError(field);
    
    field.classList.add('error');
    
    const errorElement = document.createElement('div');
    errorElement.className = 'field-error';
    errorElement.textContent = message;
    errorElement.style.cssText = `
      color: var(--color-error, #EF4444);
      font-size: var(--font-size-sm, 14px);
      margin-top: var(--spacing-xs, 4px);
    `;
    
    field.parentNode.appendChild(errorElement);
  }
  
  clearFieldError(field) {
    field.classList.remove('error');
    
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
      errorElement.remove();
    }
  }
  
  /**
   * 可訪問性增強
   */
  initAccessibility() {
    // 跳過導航鏈接
    this.addSkipToContent();
    
    // 鍵盤導航增強
    this.enhanceKeyboardNavigation();
    
    // Focus 指示器增強
    this.enhanceFocusIndicators();
  }
  
  addSkipToContent() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = '跳到主要內容';
    skipLink.className = 'skip-to-content';
    skipLink.style.cssText = `
      position: absolute;
      top: -40px;
      left: 6px;
      background: var(--color-primary, #02B875);
      color: white;
      padding: 8px;
      text-decoration: none;
      border-radius: 4px;
      z-index: 10000;
      transition: top 0.3s;
    `;
    
    skipLink.addEventListener('focus', () => {
      skipLink.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', () => {
      skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
  }
  
  enhanceKeyboardNavigation() {
    // Tab 鍵循環導航
    const focusableElements = document.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      }
    });
  }
  
  enhanceFocusIndicators() {
    // 添加自定義 focus 樣式
    const style = document.createElement('style');
    style.textContent = `
      .focus-visible {
        outline: 2px solid var(--color-primary, #02B875) !important;
        outline-offset: 2px !important;
      }
    `;
    document.head.appendChild(style);
    
    // 添加 focus-visible 類
    document.addEventListener('focusin', (e) => {
      if (e.target.matches('button, [href], input, select, textarea')) {
        e.target.classList.add('focus-visible');
      }
    });
    
    document.addEventListener('focusout', (e) => {
      e.target.classList.remove('focus-visible');
    });
  }
  
  /**
   * 性能優化
   */
  initPerformanceOptimizations() {
    // 防抖函數
    this.debounce = (func, wait) => {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    };
    
    // 節流函數
    this.throttle = (func, limit) => {
      let inThrottle;
      return function(...args) {
        if (!inThrottle) {
          func.apply(this, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    };
  }
  
  /**
   * 工具方法
   */
  getScrollOffset() {
    const header = document.querySelector('header, nav, .nav');
    return header ? header.offsetHeight + 20 : 80;
  }
  
  // 檢測移動設備
  isMobile() {
    return window.innerWidth <= 768;
  }
  
  // 檢測觸摸設備
  isTouchDevice() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  }
  
  // 獲取當前主題
  getCurrentTheme() {
    return document.documentElement.className || 'light';
  }
}

// 初始化
window.aistormCommon = new AIStormCommon();

// 導出供其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AIStormCommon;
} 