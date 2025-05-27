# AIStorm 主题系统

## 🎨 概述

AIStorm 主题系统是一个完整的前端主题管理解决方案，支持多种配色方案的动态切换，包含完整的设计令牌系统和组件库。主题管理功能已从前台迁移至后台管理系统，提供更专业的管理体验。

## 📁 文件结构

```
assets/
├── css/
│   └── theme-variables.css    # 主题变量和组件样式
└── js/
    └── theme-manager.js       # 主题管理器（仅用于演示）
theme-demo.html               # 主题系统演示页面
```

## 🎯 内置主题

| 主题名称 | 标识符 | 主色调 | 适用场景 |
|---------|--------|--------|----------|
| 荧光青色 | `default` | #00E5FF | 科技感、现代化网站 |
| 经典灰色 | `gray` | #656565 | 专业商务、企业网站 |
| 自然绿色 | `green` | #C0FF6B | 环保、自然主题网站 |
| 经典黑白 | `monochrome` | #FFFFFF | 简约、极简主义网站 |

## 🎨 颜色变量系统

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
--font-primary       /* 主要字体: 'Roboto', sans-serif */
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

## 🔧 后台主题管理

### 管理界面
主题配置功能位于后台管理系统的"站点配置"页面：
- 预设主题选择下拉菜单
- 12个颜色配置输入框
- 实时主题预览
- 自动填充和验证

### 预设主题配置

#### 1. 荧光青色主题 (default)
```javascript
{
  primary_color: '#00E5FF',
  secondary_color: '#00A2FF',
  accent_color: '#D400FF',
  success_color: '#39FF14',
  warning_color: '#FF6B35',
  background_color: '#0D0F12',
  surface_color: '#1A1D24',
  text_color: '#EAEAEA',
  text_secondary_color: '#B0B0B0',
  text_muted_color: '#888888',
  border_color: '#00E5FF',
  shadow_color: '#00E5FF'
}
```

#### 2. 经典灰色主题 (gray)
```javascript
{
  primary_color: '#656565',
  secondary_color: '#4A4A4A',
  accent_color: '#8B8B8B',
  success_color: '#6B8E23',
  warning_color: '#CD853F',
  background_color: '#2F2F2F',
  surface_color: '#404040',
  text_color: '#F5F5F5',
  text_secondary_color: '#D5D5D5',
  text_muted_color: '#A0A0A0',
  border_color: '#656565',
  shadow_color: '#656565'
}
```

#### 3. 自然绿色主题 (green)
```javascript
{
  primary_color: '#C0FF6B',
  secondary_color: '#8FBC8F',
  accent_color: '#32CD32',
  success_color: '#90EE90',
  warning_color: '#FFD700',
  background_color: '#1C2E1C',
  surface_color: '#2F4F2F',
  text_color: '#F0FFF0',
  text_secondary_color: '#D3D3D3',
  text_muted_color: '#A9A9A9',
  border_color: '#C0FF6B',
  shadow_color: '#C0FF6B'
}
```

#### 4. 经典黑白主题 (monochrome)
```javascript
{
  primary_color: '#FFFFFF',
  secondary_color: '#E0E0E0',
  accent_color: '#808080',
  success_color: '#D3D3D3',
  warning_color: '#A9A9A9',
  background_color: '#000000',
  surface_color: '#1A1A1A',
  text_color: '#FFFFFF',
  text_secondary_color: '#CCCCCC',
  text_muted_color: '#888888',
  border_color: '#FFFFFF',
  shadow_color: '#FFFFFF'
}
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

## 🔄 主题迁移说明

### 前台页面变更
**移除的功能：**
- ❌ 前台主题切换器（右上角调色板图标）
- ❌ 用户端主题选择功能
- ❌ 前台主题管理脚本引用

**保留的功能：**
- ✅ 主题变量系统 (`assets/css/theme-variables.css`)
- ✅ 主题感知的组件样式
- ✅ CSS变量动态应用

**修改的文件：**
- `index.html` - 移除主题管理器脚本引用
- `icons-demo.html` - 移除主题管理器脚本引用

### 后台管理增强
**新增功能：**
- ✅ 预设主题选择（4种主题）
- ✅ 完整的颜色配置管理（12个配置项）
- ✅ 实时主题预览
- ✅ 主题配置验证和自动填充

## 🔍 调试和测试

访问 `theme-demo.html` 查看完整的主题系统演示，包括：
- 所有颜色变量的可视化
- 组件样式展示
- 交互效果演示
- 使用方法说明

## 🎨 自定义主题

### 创建新主题配置

管理员可以在后台管理系统中：
1. 选择"自定义主题"
2. 配置12个颜色变量
3. 实时预览效果
4. 保存并应用到前台

### 主题配色建议

1. **确保对比度**: 文字和背景之间要有足够的对比度
2. **保持一致性**: 同一主题内的颜色要协调统一
3. **考虑可访问性**: 支持色盲用户和低视力用户
4. **测试多场景**: 在不同组件和页面中测试主题效果

## 📞 技术支持

如有问题或建议，请联系 AIStorm 技术团队。

---

**AIStorm 主题系统** - 让您的网站拥有专业、统一、可定制的视觉体验！ 