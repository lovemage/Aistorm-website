// 主题管理系统
class ThemeManager {
  constructor() {
    this.currentTheme = 'default';
    this.themes = {
      // 默认主题 (现有的荧光青色主题)
      default: {
        name: '荧光青色',
        colors: {
          primary: '#00E5FF',      // 主色调
          secondary: '#00A2FF',    // 次要色
          accent: '#D400FF',       // 强调色
          success: '#39FF14',      // 成功色
          warning: '#FF6B35',      // 警告色
          background: '#0D0F12',   // 背景色
          surface: '#1A1D24',      // 表面色
          text: '#EAEAEA',         // 主文字色
          textSecondary: '#B0B0B0', // 次要文字色
          textMuted: '#888888',    // 静音文字色
          border: 'rgba(0, 229, 255, 0.2)', // 边框色
          shadow: 'rgba(0, 229, 255, 0.1)'  // 阴影色
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem', 
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 灰色主题
      gray: {
        name: '经典灰色',
        colors: {
          primary: '#656565',      // 中性灰
          secondary: '#4A4A4A',    // 深灰
          accent: '#8B8B8B',       // 浅灰强调
          success: '#6B8E23',      // 橄榄绿
          warning: '#CD853F',      // 秘鲁色
          background: '#2F2F2F',   // 深灰背景
          surface: '#404040',      // 灰色表面
          text: '#F5F5F5',         // 浅色文字
          textSecondary: '#D5D5D5', // 次要文字
          textMuted: '#A0A0A0',    // 静音文字
          border: 'rgba(101, 101, 101, 0.3)', // 灰色边框
          shadow: 'rgba(101, 101, 101, 0.2)'  // 灰色阴影
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 绿色主题
      green: {
        name: '自然绿色',
        colors: {
          primary: '#C0FF6B',      // 亮绿色
          secondary: '#8FBC8F',    // 深海绿
          accent: '#32CD32',       // 酸橙绿
          success: '#90EE90',      // 浅绿色
          warning: '#FFD700',      // 金色
          background: '#1C2E1C',   // 深绿背景
          surface: '#2F4F2F',      // 深橄榄绿表面
          text: '#F0FFF0',         // 蜜瓜色文字
          textSecondary: '#D3D3D3', // 浅灰文字
          textMuted: '#A9A9A9',    // 深灰文字
          border: 'rgba(192, 255, 107, 0.3)', // 绿色边框
          shadow: 'rgba(192, 255, 107, 0.2)'  // 绿色阴影
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 黑白主题
      monochrome: {
        name: '经典黑白',
        colors: {
          primary: '#FFFFFF',      // 纯白
          secondary: '#E0E0E0',    // 浅灰
          accent: '#808080',       // 中灰
          success: '#D3D3D3',      // 浅灰成功色
          warning: '#A9A9A9',      // 深灰警告色
          background: '#000000',   // 纯黑背景
          surface: '#1A1A1A',      // 深灰表面
          text: '#FFFFFF',         // 白色文字
          textSecondary: '#CCCCCC', // 浅灰文字
          textMuted: '#888888',    // 中灰文字
          border: 'rgba(255, 255, 255, 0.2)', // 白色边框
          shadow: 'rgba(255, 255, 255, 0.1)'  // 白色阴影
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 新增主题：Blue Candy
      blueCandy: {
        name: 'Blue Candy',
        colors: {
          primary: '#4F76F6', // 主色调
          secondary: '#1F2B37', // 次要色
          accent: '#8553F4', // 强调色
          success: '#77F2A1', // 成功色
          warning: '#FB81BE', // 警告色
          background: '#F9F9F9', // 背景色
          surface: '#192442', // 表面色
          text: '#1F2B37', // 主文字色
          textSecondary: '#4F76F6', // 次要文字色
          textMuted: '#8553F4', // 静音文字色
          border: 'rgba(79, 118, 246, 0.2)', // 边框色
          shadow: 'rgba(79, 118, 246, 0.08)' // 阴影色
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 新增主题：Mint Candy
      mintCandy: {
        name: 'Mint Candy',
        colors: {
          primary: '#45D3A1',
          secondary: '#ADEDc2',
          accent: '#E949DB',
          success: '#77F2A1',
          warning: '#FB81BE',
          background: '#F9F9F9',
          surface: '#C4F4F9',
          text: '#192442',
          textSecondary: '#45D3A1',
          textMuted: '#E949DB',
          border: 'rgba(69, 211, 161, 0.2)',
          shadow: 'rgba(69, 211, 161, 0.08)'
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      },
      
      // 新增主题：Pastel Candy
      pastelCandy: {
        name: 'Pastel Candy',
        colors: {
          primary: '#63BFF4',
          secondary: '#C4F4F9',
          accent: '#E949DB',
          success: '#ADEDc2',
          warning: '#FB81BE',
          background: '#F9F9F9',
          surface: '#E949DB',
          text: '#192442',
          textSecondary: '#63BFF4',
          textMuted: '#E949DB',
          border: 'rgba(99, 191, 244, 0.2)',
          shadow: 'rgba(99, 191, 244, 0.08)'
        },
        fonts: {
          primary: "'Roboto', sans-serif",
          size: {
            xs: '0.75rem',
            sm: '0.875rem',
            base: '1rem',
            lg: '1.125rem',
            xl: '1.25rem',
            '2xl': '1.5rem',
            '3xl': '1.875rem',
            '4xl': '2.25rem'
          }
        }
      }
    };
    
    this.init();
  }

  // 初始化主题系统
  init() {
    // 从本地存储加载主题设置
    const savedTheme = localStorage.getItem('aistorm-theme');
    if (savedTheme && this.themes[savedTheme]) {
      this.currentTheme = savedTheme;
    }
    
    // 应用当前主题
    this.applyTheme(this.currentTheme);
    
    // 创建主题切换器UI
    this.createThemeSwitcher();
  }

  // 应用主题
  applyTheme(themeName) {
    if (!this.themes[themeName]) {
      console.warn(`主题 "${themeName}" 不存在`);
      return;
    }

    const theme = this.themes[themeName];
    const root = document.documentElement;

    // 应用颜色变量
    Object.entries(theme.colors).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key}`, value);
    });

    // 应用字体变量
    root.style.setProperty('--font-primary', theme.fonts.primary);
    Object.entries(theme.fonts.size).forEach(([key, value]) => {
      root.style.setProperty(`--font-size-${key}`, value);
    });

    // 更新当前主题
    this.currentTheme = themeName;
    
    // 保存到本地存储
    localStorage.setItem('aistorm-theme', themeName);
    
    // 触发主题变更事件
    document.dispatchEvent(new CustomEvent('themeChanged', {
      detail: { theme: themeName, colors: theme.colors }
    }));

    console.log(`已切换到主题: ${theme.name}`);
  }

  // 创建主题切换器UI
  createThemeSwitcher() {
    // 创建主题切换器容器
    const switcher = document.createElement('div');
    switcher.className = 'theme-switcher';
    switcher.innerHTML = `
      <button class="theme-toggle-btn" aria-label="切换主题">
        <span class="icon icon-palette icon-lg"></span>
      </button>
      <div class="theme-menu">
        <h4>选择主题</h4>
        <div class="theme-options">
          ${Object.entries(this.themes).map(([key, theme]) => `
            <button class="theme-option ${key === this.currentTheme ? 'active' : ''}" 
                    data-theme="${key}">
              <div class="theme-preview">
                <div class="color-preview" style="background: ${theme.colors.primary}"></div>
                <div class="color-preview" style="background: ${theme.colors.secondary}"></div>
                <div class="color-preview" style="background: ${theme.colors.accent}"></div>
              </div>
              <span class="theme-name">${theme.name}</span>
            </button>
          `).join('')}
        </div>
      </div>
    `;

    // 添加样式
    this.addThemeSwitcherStyles();
    
    // 添加到页面
    document.body.appendChild(switcher);
    
    // 绑定事件
    this.bindThemeSwitcherEvents(switcher);
  }

  // 添加主题切换器样式
  addThemeSwitcherStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .theme-switcher {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
      }
      
      .theme-toggle-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--color-surface, #1A1D24);
        border: 2px solid var(--color-primary, #00E5FF);
        color: var(--color-primary, #00E5FF);
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px var(--color-shadow, rgba(0, 229, 255, 0.2));
      }
      
      .theme-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px var(--color-shadow, rgba(0, 229, 255, 0.3));
      }
      
      .theme-menu {
        position: absolute;
        top: 60px;
        right: 0;
        background: var(--color-surface, #1A1D24);
        border: 1px solid var(--color-border, rgba(0, 229, 255, 0.2));
        border-radius: 10px;
        padding: 1rem;
        min-width: 200px;
        opacity: 0;
        visibility: hidden;
        transform: translateY(-10px);
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
      }
      
      .theme-switcher.active .theme-menu {
        opacity: 1;
        visibility: visible;
        transform: translateY(0);
      }
      
      .theme-menu h4 {
        color: var(--color-text, #EAEAEA);
        margin: 0 0 1rem 0;
        font-size: 1rem;
        text-align: center;
      }
      
      .theme-options {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
      }
      
      .theme-option {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.75rem;
        background: transparent;
        border: 1px solid var(--color-border, rgba(0, 229, 255, 0.2));
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
        color: var(--color-text, #EAEAEA);
      }
      
      .theme-option:hover {
        background: var(--color-border, rgba(0, 229, 255, 0.1));
        transform: translateX(3px);
      }
      
      .theme-option.active {
        border-color: var(--color-primary, #00E5FF);
        background: var(--color-border, rgba(0, 229, 255, 0.1));
      }
      
      .theme-preview {
        display: flex;
        gap: 2px;
      }
      
      .color-preview {
        width: 12px;
        height: 12px;
        border-radius: 2px;
      }
      
      .theme-name {
        font-size: 0.9rem;
        font-weight: 500;
      }
      
      @media (max-width: 768px) {
        .theme-switcher {
          top: 10px;
          right: 10px;
        }
        
        .theme-toggle-btn {
          width: 40px;
          height: 40px;
          font-size: 1.2rem;
        }
        
        .theme-menu {
          right: -50px;
          min-width: 180px;
        }
      }
    `;
    
    document.head.appendChild(style);
  }

  // 绑定主题切换器事件
  bindThemeSwitcherEvents(switcher) {
    const toggleBtn = switcher.querySelector('.theme-toggle-btn');
    const themeOptions = switcher.querySelectorAll('.theme-option');
    
    // 切换菜单显示
    toggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      switcher.classList.toggle('active');
    });
    
    // 点击主题选项
    themeOptions.forEach(option => {
      option.addEventListener('click', (e) => {
        e.stopPropagation();
        const themeName = option.dataset.theme;
        this.applyTheme(themeName);
        
        // 更新活跃状态
        themeOptions.forEach(opt => opt.classList.remove('active'));
        option.classList.add('active');
        
        // 关闭菜单
        switcher.classList.remove('active');
      });
    });
    
    // 点击外部关闭菜单
    document.addEventListener('click', () => {
      switcher.classList.remove('active');
    });
    
    // ESC键关闭菜单
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        switcher.classList.remove('active');
      }
    });
  }

  // 获取当前主题
  getCurrentTheme() {
    return this.currentTheme;
  }

  // 获取主题颜色
  getThemeColors(themeName = this.currentTheme) {
    return this.themes[themeName]?.colors || {};
  }

  // 添加新主题
  addTheme(name, themeConfig) {
    this.themes[name] = themeConfig;
    console.log(`已添加新主题: ${themeConfig.name}`);
  }

  // 移除主题
  removeTheme(name) {
    if (name === 'default') {
      console.warn('无法移除默认主题');
      return;
    }
    
    delete this.themes[name];
    
    if (this.currentTheme === name) {
      this.applyTheme('default');
    }
    
    console.log(`已移除主题: ${name}`);
  }
}

// 自动初始化主题管理器
const themeManager = new ThemeManager();

// 导出到全局作用域
window.themeManager = themeManager; 