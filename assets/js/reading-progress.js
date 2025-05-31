/**
 * AIStorm 閱讀進度條管理器
 * 顯示文章閱讀進度，提升閱讀體驗
 */

class ReadingProgressManager {
  constructor(options = {}) {
    this.options = {
      // 進度條選擇器
      progressBarSelector: '.reading-progress',
      // 內容容器選擇器
      contentSelector: 'article, main, .article-content',
      // 偏移量調整
      offsetTop: 100,
      offsetBottom: 100,
      // 是否顯示估計閱讀時間
      showReadingTime: true,
      // 平均閱讀速度（字/分鐘）
      readingSpeed: 200,
      // 動畫持續時間
      animationDuration: 100,
      ...options
    };
    
    this.progressBar = null;
    this.content = null;
    this.isInitialized = false;
    
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
    this.createProgressBar();
    this.findContent();
    
    if (this.content) {
      this.bindEvents();
      this.calculateReadingTime();
      this.updateProgress();
      this.isInitialized = true;
    }
  }
  
  createProgressBar() {
    // 檢查是否已存在進度條
    this.progressBar = document.querySelector(this.options.progressBarSelector);
    
    if (!this.progressBar) {
      // 創建進度條元素
      this.progressBar = document.createElement('div');
      this.progressBar.className = 'reading-progress';
      this.progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: var(--color-primary, #02B875);
        z-index: var(--z-fixed, 1030);
        transition: width ${this.options.animationDuration}ms ease;
        opacity: 0;
        transform: scaleX(0);
        transform-origin: left;
      `;
      
      document.body.appendChild(this.progressBar);
      
      // 添加入場動畫
      requestAnimationFrame(() => {
        this.progressBar.style.opacity = '1';
        this.progressBar.style.transform = 'scaleX(1)';
      });
    }
  }
  
  findContent() {
    // 尋找主要內容容器
    this.content = document.querySelector(this.options.contentSelector);
    
    if (!this.content) {
      console.warn('ReadingProgressManager: 找不到內容容器');
    }
  }
  
  bindEvents() {
    // 節流函數
    let ticking = false;
    
    const handleScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          this.updateProgress();
          ticking = false;
        });
        ticking = true;
      }
    };
    
    // 監聽滾動事件
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    
    // 監聽主題變更事件
    window.addEventListener('themeChanged', () => {
      this.updateProgressBarColor();
    });
  }
  
  updateProgress() {
    if (!this.content || !this.progressBar) return;
    
    const contentRect = this.content.getBoundingClientRect();
    const contentHeight = this.content.offsetHeight;
    const contentTop = contentRect.top + window.pageYOffset;
    const windowHeight = window.innerHeight;
    const scrollY = window.pageYOffset;
    
    // 計算閱讀進度
    const startReading = contentTop - this.options.offsetTop;
    const finishReading = contentTop + contentHeight - windowHeight + this.options.offsetBottom;
    const totalDistance = finishReading - startReading;
    const currentDistance = scrollY - startReading;
    
    let progress = 0;
    
    if (totalDistance > 0) {
      progress = Math.max(0, Math.min(100, (currentDistance / totalDistance) * 100));
    }
    
    // 更新進度條寬度
    this.progressBar.style.width = `${progress}%`;
    
    // 觸發進度更新事件
    window.dispatchEvent(new CustomEvent('readingProgressUpdate', {
      detail: { progress, isComplete: progress >= 100 }
    }));
    
    // 當閱讀完成時的特效
    if (progress >= 100) {
      this.onReadingComplete();
    }
  }
  
  onReadingComplete() {
    // 添加完成特效
    this.progressBar.style.boxShadow = '0 0 10px var(--color-primary, #02B875)';
    
    setTimeout(() => {
      this.progressBar.style.boxShadow = 'none';
    }, 1000);
  }
  
  calculateReadingTime() {
    if (!this.content || !this.options.showReadingTime) return;
    
    // 計算文字數量
    const text = this.content.textContent || this.content.innerText || '';
    const wordCount = text.length;
    const readingTimeMinutes = Math.ceil(wordCount / this.options.readingSpeed);
    
    // 尋找或創建閱讀時間顯示元素
    let readingTimeElement = document.querySelector('.reading-time');
    
    if (!readingTimeElement) {
      // 在文章開頭添加閱讀時間
      const articleMeta = document.querySelector('.article-meta, .post-meta');
      if (articleMeta) {
        readingTimeElement = document.createElement('span');
        readingTimeElement.className = 'reading-time';
        readingTimeElement.textContent = `閱讀時間：${readingTimeMinutes} 分鐘`;
        articleMeta.appendChild(readingTimeElement);
      }
    }
    
    // 觸發閱讀時間計算完成事件
    window.dispatchEvent(new CustomEvent('readingTimeCalculated', {
      detail: { 
        wordCount, 
        readingTimeMinutes,
        readingTimeText: `${readingTimeMinutes} 分鐘`
      }
    }));
  }
  
  updateProgressBarColor() {
    if (!this.progressBar) return;
    
    // 根據當前主題更新進度條顏色
    const currentTheme = document.documentElement.className;
    const primaryColor = getComputedStyle(document.documentElement)
      .getPropertyValue('--color-primary').trim() || '#02B875';
    
    this.progressBar.style.background = primaryColor;
  }
  
  // 手動設置進度（用於測試或特殊需求）
  setProgress(percentage) {
    if (this.progressBar) {
      this.progressBar.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
    }
  }
  
  // 顯示進度條
  show() {
    if (this.progressBar) {
      this.progressBar.style.opacity = '1';
      this.progressBar.style.transform = 'scaleX(1)';
    }
  }
  
  // 隱藏進度條
  hide() {
    if (this.progressBar) {
      this.progressBar.style.opacity = '0';
      this.progressBar.style.transform = 'scaleX(0)';
    }
  }
  
  // 銷毀進度條
  destroy() {
    if (this.progressBar && this.progressBar.parentNode) {
      this.progressBar.parentNode.removeChild(this.progressBar);
    }
    this.isInitialized = false;
  }
}

// 自動初始化（僅在文章頁面）
document.addEventListener('DOMContentLoaded', () => {
  // 檢查是否為文章頁面
  if (document.querySelector('article, .article-content, .post-content')) {
    window.readingProgressManager = new ReadingProgressManager();
  }
});

// 導出供其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ReadingProgressManager;
} 