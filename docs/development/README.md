# 🛠️ AIStorm 开发指南

## 📋 目录
- [前端开发](#前端开发)
- [主题系统](#主题系统)
- [图标系统](#图标系统)
- [API集成](#api集成)
- [本地开发环境](#本地开发环境)

---

## 🎨 前端开发

### 技术栈
- **HTML5**: 语义化标记
- **CSS3**: Flexbox/Grid布局，CSS变量
- **JavaScript ES6+**: 模块化开发
- **响应式设计**: 移动优先设计原则

### 项目结构
```
assets/
├── css/
│   ├── main.css          # 主样式文件
│   ├── theme.css         # 主题变量
│   └── responsive.css    # 响应式样式
├── images/
│   ├── products/         # 产品图片
│   ├── icons/           # 图标文件
│   └── backgrounds/     # 背景图片
└── js/
    ├── main.js          # 主脚本
    ├── api-config.js    # API配置
    └── footer.js        # Footer管理
```

### 开发规范
- 使用 CSS 变量进行主题管理
- 遵循 BEM 命名规范
- 保持组件化开发思路
- 优化图片格式和大小

---

## 🎨 主题系统

### 颜色变量
```css
:root {
    /* 主要颜色 */
    --primary-color: #00E5FF;      /* 荧光青 */
    --secondary-color: #D400FF;    /* 洋红色 */
    --accent-color: #39FF14;       /* 荧光绿 */
    
    /* 背景颜色 */
    --bg-primary: #0D0F12;         /* 深邃背景 */
    --bg-secondary: #1A1D24;       /* 卡片背景 */
    
    /* 文字颜色 */
    --text-primary: #EAEAEA;       /* 主要文字 */
    --text-secondary: #B0B0B0;     /* 次要文字 */
    --text-accent: #00E5FF;        /* 强调文字 */
}
```

### 动态主题切换
```javascript
// 主题管理器
class ThemeManager {
    constructor() {
        this.themes = {
            default: {
                primary: '#00E5FF',
                secondary: '#D400FF',
                accent: '#39FF14'
            },
            // 可扩展其他主题
        };
    }
    
    applyTheme(themeName) {
        const theme = this.themes[themeName];
        if (theme) {
            Object.entries(theme).forEach(([key, value]) => {
                document.documentElement.style.setProperty(`--${key}-color`, value);
            });
        }
    }
}
```

### 响应式断点
```css
/* 移动设备 */
@media (max-width: 768px) {
    .container {
        padding: 15px;
    }
}

/* 平板设备 */
@media (min-width: 769px) and (max-width: 1024px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* 桌面设备 */
@media (min-width: 1025px) {
    .grid {
        grid-template-columns: repeat(3, 1fr);
    }
}
```

---

## 🔧 图标系统

### 图标规范
- **格式**: SVG (推荐) 或 PNG
- **尺寸**: 24x24px (小图标), 48x48px (中等), 64x64px (大图标)
- **颜色**: 使用 CSS 变量，支持主题切换

### 图标组件
```html
<!-- SVG 图标组件 -->
<svg class="icon icon--payment" viewBox="0 0 24 24">
    <path d="..." fill="currentColor"/>
</svg>
```

```css
.icon {
    width: 24px;
    height: 24px;
    color: var(--primary-color);
    transition: color 0.3s ease;
}

.icon--payment {
    color: var(--accent-color);
}
```

### 图标库
- 支付相关：USDT、支付宝、微信支付
- 产品相关：ChatGPT、Claude、Grok、Cursor、Lovable
- 功能相关：购物车、用户、设置、通知

---

## 🔌 API集成

### API配置
```javascript
// api-config.js
const API_CONFIG = {
    BASE_URL: window.location.origin,
    ENDPOINTS: {
        PRODUCTS: '/api/products',
        SETTINGS: '/api/settings',
        CREATE_ORDER: '/api/create-order',
        OXAPAY_PAYMENT: '/api/oxapay-payment',
        ORDER_STATUS: '/api/order-status'
    }
};
```

### API调用示例
```javascript
// 获取产品列表
async function fetchProducts() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.PRODUCTS}`);
        const products = await response.json();
        return products;
    } catch (error) {
        console.error('获取产品失败:', error);
        return [];
    }
}

// 创建订单
async function createOrder(orderData) {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.CREATE_ORDER}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('创建订单失败:', error);
        throw error;
    }
}
```

### 错误处理
```javascript
// 统一错误处理
function handleApiError(error, userMessage = '操作失败，请重试') {
    console.error('API错误:', error);
    
    // 显示用户友好的错误消息
    showNotification(userMessage, 'error');
    
    // 记录详细错误信息用于调试
    if (window.console && typeof error === 'object') {
        console.table(error);
    }
}
```

---

## 💻 本地开发环境

### 环境搭建
```bash
# 1. 克隆项目
git clone <repository-url>
cd AIStorm_Static_Website

# 2. 安装Python依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的配置

# 4. 启动后端服务
python3 start.py

# 5. 启动前端静态服务 (另一个终端)
python3 -m http.server 8080
```

### 开发工具推荐
- **代码编辑器**: VS Code, Cursor
- **浏览器**: Chrome DevTools
- **调试工具**: Vue DevTools, React DevTools
- **版本控制**: Git

### 调试技巧
```javascript
// 开发环境调试
if (window.location.hostname === 'localhost') {
    // 启用详细日志
    console.log('开发模式：详细日志已启用');
    
    // 暴露调试接口到全局
    window.DEBUG = {
        api: API_CONFIG,
        state: applicationState,
        utils: debugUtils
    };
}
```

### 热重载配置
```javascript
// 开发环境热重载
if (process.env.NODE_ENV === 'development') {
    // 监听文件变化
    const ws = new WebSocket('ws://localhost:8080/ws');
    ws.onmessage = (event) => {
        if (event.data === 'reload') {
            window.location.reload();
        }
    };
}
```

---

## 🧪 测试

### 前端测试
```javascript
// 简单的单元测试示例
function testApiConfig() {
    console.assert(API_CONFIG.BASE_URL, 'API Base URL should be defined');
    console.assert(API_CONFIG.ENDPOINTS.PRODUCTS, 'Products endpoint should be defined');
    console.log('✅ API配置测试通过');
}

// 测试主题系统
function testThemeSystem() {
    const root = document.documentElement;
    const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color');
    console.assert(primaryColor, 'Primary color should be defined');
    console.log('✅ 主题系统测试通过');
}
```

### 浏览器兼容性测试
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 性能优化
- 图片懒加载
- CSS/JS 压缩
- CDN 使用
- 缓存策略

---

## 📦 构建部署

### 生产环境构建
```bash
# 压缩CSS
npm run build:css

# 压缩JavaScript
npm run build:js

# 优化图片
npm run optimize:images

# 生成sitemap
npm run generate:sitemap
```

### 部署检查清单
- [ ] 所有静态资源已优化
- [ ] API端点配置正确
- [ ] 响应式设计测试通过
- [ ] 跨浏览器兼容性测试
- [ ] 性能测试通过
- [ ] SEO优化完成

---

**更新时间**: 2025-05-29  
**维护者**: AIStorm开发团队 