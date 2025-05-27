# AIStorm 主题系统使用指南

## 🎨 概述

AIStorm 主题系统是一个完整的前端主题管理解决方案，支持多种配色方案的动态切换，包含完整的设计令牌系统和组件库。

## 📁 文件结构

```
assets/
├── css/
│   └── theme-variables.css    # 主题变量和组件样式
└── js/
    └── theme-manager.js       # 主题管理器
theme-demo.html               # 主题系统演示页面
```

## 🚀 快速开始

### 1. 引入文件

在HTML头部引入主题CSS：
```html
<link rel="stylesheet" href="assets/css/theme-variables.css">
```

在页面底部引入主题管理器：
```html
<script src="assets/js/theme-manager.js"></script>
```

### 2. 基本使用

主题系统会自动初始化并在页面右上角显示主题切换器。用户可以点击调色板图标切换主题。

## 🎯 内置主题

| 主题名称 | 标识符 | 描述 |
|---------|--------|------|
| 荧光青色 | `default` | 默认主题，科技感荧光青色 |
| 经典灰色 | `gray` | 专业商务灰色主题 |
| 自然绿色 | `green` | 清新自然绿色主题 |
| 经典黑白 | `monochrome` | 简约黑白主题 |

## 🎨 颜色变量

### 主要颜色
```css
--color-primary      /* 主色调 */
--color-secondary    /* 次要色 */
--color-accent       /* 强调色 */
--color-success      /* 成功色 */
--color-warning      /* 警告色 */
```

### 背景颜色
```css
--color-background   /* 页面背景 */
--color-surface      /* 卡片/组件背景 */
```

### 文字颜色
```css
--color-text         /* 主要文字 */
--color-text-secondary /* 次要文字 */
--color-text-muted   /* 静音文字 */
```

### 边框和阴影
```css
--color-border       /* 边框颜色 */
--color-shadow       /* 阴影颜色 */
```

## 📝 字体系统

### 字体族
```css
--font-primary       /* 主要字体 */
```

### 字体大小
```css
--font-size-xs       /* 0.75rem */
--font-size-sm       /* 0.875rem */
--font-size-base     /* 1rem */
--font-size-lg       /* 1.125rem */
--font-size-xl       /* 1.25rem */
--font-size-2xl      /* 1.5rem */
--font-size-3xl      /* 1.875rem */
--font-size-4xl      /* 2.25rem */
```

## 📏 间距系统

```css
--spacing-xs         /* 0.25rem */
--spacing-sm         /* 0.5rem */
--spacing-md         /* 1rem */
--spacing-lg         /* 1.5rem */
--spacing-xl         /* 2rem */
--spacing-2xl        /* 3rem */
--spacing-3xl        /* 4rem */
```

## 🔘 预定义组件类

### 按钮
```html
<button class="theme-btn-primary">主要按钮</button>
<button class="theme-btn-outline">轮廓按钮</button>
```

### 卡片
```html
<div class="theme-card">
  <h3 class="theme-heading-primary">卡片标题</h3>
  <p>卡片内容</p>
</div>
```

### 表单
```html
<input type="text" class="theme-input" placeholder="输入框">
```

### 徽章
```html
<span class="theme-badge">默认徽章</span>
<span class="theme-badge-accent">强调徽章</span>
<span class="theme-badge-success">成功徽章</span>
<span class="theme-badge-warning">警告徽章</span>
```

### 文字样式
```html
<h1 class="theme-heading-primary">主要标题</h1>
<h2 class="theme-heading-accent">强调标题</h2>
<a href="#" class="theme-link">主题链接</a>
```

### 背景和文字颜色
```html
<div class="theme-bg-primary theme-text-default">主色背景</div>
<div class="theme-bg-surface theme-text-primary">表面背景，主色文字</div>
```

## 🔧 JavaScript API

### 基本方法

```javascript
// 切换主题
themeManager.applyTheme('gray');

// 获取当前主题
const currentTheme = themeManager.getCurrentTheme();

// 获取主题颜色
const colors = themeManager.getThemeColors();
```

### 添加自定义主题

```javascript
themeManager.addTheme('custom', {
  name: '自定义主题',
  colors: {
    primary: '#FF5722',
    secondary: '#FF9800',
    accent: '#FFC107',
    success: '#4CAF50',
    warning: '#FF9800',
    background: '#121212',
    surface: '#1E1E1E',
    text: '#FFFFFF',
    textSecondary: '#CCCCCC',
    textMuted: '#999999',
    border: 'rgba(255, 87, 34, 0.2)',
    shadow: 'rgba(255, 87, 34, 0.1)'
  },
  fonts: {
    primary: "'Arial', sans-serif",
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
});
```

### 监听主题变更

```javascript
document.addEventListener('themeChanged', function(event) {
  const { theme, colors } = event.detail;
  console.log(`主题已切换到: ${theme}`, colors);
});
```

## 📱 响应式设计

主题系统包含响应式断点：

- **平板**: `@media (max-width: 768px)`
- **手机**: `@media (max-width: 480px)`

字体大小和间距会在小屏幕上自动调整。

## 🎯 最佳实践

### 1. 使用CSS变量
```css
.my-component {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: var(--spacing-md);
  border-radius: var(--radius-lg);
}
```

### 2. 使用预定义类
```html
<div class="theme-card">
  <h3 class="theme-heading-primary">标题</h3>
  <p class="theme-text-secondary">描述文字</p>
  <button class="theme-btn-primary">操作按钮</button>
</div>
```

### 3. 组合使用
```html
<div class="theme-bg-surface" style="padding: var(--spacing-lg);">
  <h2 style="color: var(--color-primary); margin-bottom: var(--spacing-md);">
    组合使用示例
  </h2>
</div>
```

## 🔍 调试和测试

访问 `theme-demo.html` 查看完整的主题系统演示，包括：
- 所有颜色变量的可视化
- 组件样式展示
- 交互效果演示
- 使用方法说明

## 🎨 自定义主题

### 创建新主题配置

```javascript
const myTheme = {
  name: '我的主题',
  colors: {
    primary: '#your-color',
    secondary: '#your-color',
    // ... 其他颜色
  },
  fonts: {
    primary: "'Your Font', sans-serif",
    size: {
      // ... 字体大小配置
    }
  }
};

themeManager.addTheme('my-theme', myTheme);
```

### 主题配色建议

1. **确保对比度**: 文字和背景之间要有足够的对比度
2. **保持一致性**: 同一主题内的颜色要协调统一
3. **考虑可访问性**: 支持色盲用户和低视力用户
4. **测试多场景**: 在不同组件和页面中测试主题效果

## 📞 技术支持

如有问题或建议，请联系 AIStorm 技术团队。

---

**AIStorm 主题系统** - 让您的网站拥有专业、统一、可定制的视觉体验！ 