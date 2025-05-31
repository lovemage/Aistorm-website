/**
 * AIStorm 主題切換管理器
 * 支持亮色/暗色模式切換，並記住用戶偏好
 */

class ThemeManager {
  constructor() {
    this.init();
  }
  
  init() {
    // 獲取保存的主題或檢測系統偏好
    const saved = localStorage.getItem('aistorm-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = saved || (prefersDark ? 'dark' : 'light');
    
    this.setTheme(theme);
    this.bindEvents();
    this.addSystemThemeListener();
  }
  
  setTheme(theme) {
    // 應用主題到 HTML 元素
    document.documentElement.className = theme;
    localStorage.setItem('aistorm-theme', theme);
    this.updateToggleButtons(theme);
    
    // 觸發主題變更事件
    window.dispatchEvent(new CustomEvent('themeChanged', { 
      detail: { theme } 
    }));
  }
  
  toggle() {
    const current = document.documentElement.className;
    const newTheme = current === 'dark' ? 'light' : 'dark';
    this.setTheme(newTheme);
  }
  
  updateToggleButtons(theme) {
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      // 更新按鈕圖標
      const isDark = theme === 'dark';
      
      // 如果按鈕包含SVG圖標
      const lightIcon = btn.querySelector('.light-icon');
      const darkIcon = btn.querySelector('.dark-icon');
      
      if (lightIcon && darkIcon) {
        lightIcon.style.display = isDark ? 'none' : 'block';
        darkIcon.style.display = isDark ? 'block' : 'none';
      } else {
        // 如果是文字按鈕
        btn.textContent = isDark ? '☀️' : '🌙';
      }
      
      // 更新 aria 標籤
      btn.setAttribute('aria-label', isDark ? '切換到亮色模式' : '切換到暗色模式');
    });
  }
  
  bindEvents() {
    // 綁定所有主題切換按鈕
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggle();
      });
    });
    
    // 鍵盤快捷鍵 (Ctrl/Cmd + Shift + T)
    document.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'T') {
        e.preventDefault();
        this.toggle();
      }
    });
  }
  
  addSystemThemeListener() {
    // 監聽系統主題變化
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      // 只在用戶沒有手動設置主題時自動跟隨系統
      if (!localStorage.getItem('aistorm-theme')) {
        this.setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
  
  getCurrentTheme() {
    return document.documentElement.className || 'light';
  }
  
  // 重置到系統偏好
  resetToSystemPreference() {
    localStorage.removeItem('aistorm-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    this.setTheme(prefersDark ? 'dark' : 'light');
  }
}

// 等待 DOM 加載完成後初始化
document.addEventListener('DOMContentLoaded', () => {
  window.themeManager = new ThemeManager();
});

// 如果 DOM 已經加載完成，立即初始化
if (document.readyState === 'loading') {
  // DOM 還在加載中，等待 DOMContentLoaded 事件
} else {
  // DOM 已經加載完成
  window.themeManager = new ThemeManager();
}

// 導出供其他模塊使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ThemeManager;
} 