// 产品管理和库存显示功能
class ProductManager {
    constructor() {
        // 使用全局API配置
        this.apiBaseUrl = window.apiConfig ? window.apiConfig.getBaseUrl() : this.getApiBaseUrl();
        this.products = [];
        this.retryCount = 0;
        this.maxRetries = 3;
        this.retryDelay = 2000; // 2秒
        this.usdtToCnyRate = 8.0; // 默认汇率
        this.init();
    }

    // 备用API URL检测方法（如果全局配置不可用）
    getApiBaseUrl() {
        const currentHost = window.location.hostname;
        const currentPort = window.location.port;
        
        // 生产环境检测
        if (!['localhost', '127.0.0.1', '0.0.0.0'].includes(currentHost)) {
            return '/api';
        }
        
        // 如果当前页面就在5001端口，使用相对路径
        if (currentPort === '5001') {
            return '/api';
        }
        
        // 如果是本地开发环境
        if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
            return 'http://localhost:5001/api';
        }
        
        // 默认回退到相对路径
        return '/api';
    }

    async init() {
        try {
            // 测试API连接并自动选择最佳URL
            if (window.apiConfig) {
                const isConnected = await window.apiConfig.testConnection();
                if (isConnected) {
                    // 更新API基础URL（可能已经自动切换）
                    this.apiBaseUrl = window.apiConfig.getBaseUrl();
                    console.log('✅ API连接成功，使用URL:', this.apiBaseUrl);
                } else {
                    console.warn('⚠️ API连接失败，将使用静态数据');
                }
            }
            
            // 获取汇率设置
            await this.loadSiteSettings();
            
            await this.loadProductsWithRetry();
            this.updateProductDisplay();
            this.updateProductPrices();
            
            // 设置定期刷新（仅在API可用时）
            if (this.products.length > 0 && !this.isUsingStaticData) {
                this.startPeriodicRefresh();
            }
        } catch (error) {
            console.error('初始化产品管理器失败:', error);
            // 确保使用静态数据作为最后的回退
            this.products = this.getStaticProducts();
            this.isUsingStaticData = true;
            this.updateProductDisplay();
        }
    }

    // 带重试机制的产品加载
    async loadProductsWithRetry() {
        for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
            try {
                await this.loadProducts();
                if (!this.isUsingStaticData) {
                    console.log(`✅ 产品数据加载成功 (尝试 ${attempt + 1}/${this.maxRetries + 1})`);
                    return;
                }
            } catch (error) {
                console.warn(`❌ 产品数据加载失败 (尝试 ${attempt + 1}/${this.maxRetries + 1}):`, error.message);
                
                if (attempt < this.maxRetries) {
                    console.log(`⏳ ${this.retryDelay / 1000}秒后重试...`);
                    await new Promise(resolve => setTimeout(resolve, this.retryDelay));
                    // 指数退避：每次重试延迟时间翻倍
                    this.retryDelay *= 1.5;
                } else {
                    console.log('🔄 所有重试失败，使用静态数据');
                    this.products = this.getStaticProducts();
                    this.isUsingStaticData = true;
                }
            }
        }
    }

    // 加载站点设置（主要获取汇率）
    async loadSiteSettings() {
        try {
            const response = await fetch(`${this.apiBaseUrl.replace('/api', '')}/api/settings`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const settings = await response.json();
                if (settings.usdt_to_cny_rate) {
                    this.usdtToCnyRate = parseFloat(settings.usdt_to_cny_rate);
                    console.log('💱 获取汇率设置:', this.usdtToCnyRate);
                }
            }
        } catch (error) {
            console.warn('⚠️ 获取站点设置失败，使用默认汇率:', this.usdtToCnyRate);
        }
    }

    // 从后端API加载产品数据
    async loadProducts() {
        try {
            if (window.apiConfig) {
                window.apiConfig.logRequest('GET', '/products');
            }
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000); // 15秒超时
            
            const response = await fetch(`${this.apiBaseUrl}/products`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (window.apiConfig) {
                window.apiConfig.logResponse('GET', '/products', response);
            }
            
            if (response.ok) {
                const data = await response.json();
                if (Array.isArray(data) && data.length > 0) {
                    this.products = data;
                    this.isUsingStaticData = false;
                    console.log('✅ 产品数据加载成功:', this.products);
                } else {
                    throw new Error('API返回空数据或格式错误');
                }
            } else {
                throw new Error(`API响应错误: ${response.status} ${response.statusText}`);
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                throw new Error('请求超时');
            }
            console.error('❌ API请求失败:', error);
            throw error;
        }
    }

    // 静态产品数据作为后备
    getStaticProducts() {
        return [
            {
                name: 'AI風暴組合套餐',
                slug: 'ai-storm-combo',
                price_usd: 200,
                price_unit: '月',
                in_stock: true,
                stock_quantity: 25
            },
            {
                name: 'ChatGPT Pro',
                slug: 'chatgpt-pro',
                price_usd: 130,
                price_unit: '月',
                in_stock: true,
                stock_quantity: 50
            },
            {
                name: 'Claude Max 5x',
                slug: 'claude-max-5x',
                price_usd: 75,
                price_unit: '月',
                in_stock: true,
                stock_quantity: 30
            },
            {
                name: 'Super Grok',
                slug: 'super-grok',
                price_usd: 20,
                price_unit: '月',
                in_stock: true,
                stock_quantity: 100
            },
            {
                name: 'Cursor Pro',
                slug: 'cursor-pro',
                price_usd: 12,
                price_unit: '月',
                in_stock: true,
                stock_quantity: 200
            },
            {
                name: 'Lovable Pro 200 Credit',
                slug: 'lovable-pro-200-credit',
                price_usd: 35,
                price_unit: '200 Credit',
                in_stock: true,
                stock_quantity: 80
            }
        ];
    }

    // 新增：更新产品价格显示
    updateProductPrices() {
        console.log('💰 开始更新产品价格显示');
        
        this.products.forEach(product => {
            this.updateProductCardPrice(product);
        });
        
        // 如果使用静态数据，添加警告日志
        if (this.isUsingStaticData) {
            console.log('⚠️ 使用静态数据更新价格');
        }
    }

    // 新增：更新单个产品卡片的价格显示
    updateProductCardPrice(product) {
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            const productTitle = card.querySelector('h3')?.textContent.trim();
            
            // 匹配产品名称
            if (this.matchProductName(productTitle, product.name)) {
                this.updateCardPriceElements(card, product);
            }
        });
    }

    // 新增：更新卡片内的价格元素
    updateCardPriceElements(card, product) {
        const priceElement = card.querySelector('.price');
        const priceRmbElement = card.querySelector('.price-rmb, .price-rmb-detail');
        
        if (priceElement) {
            // 更新USDT价格
            const newPriceText = `$${product.price_usd} USDT/${product.price_unit}`;
            priceElement.textContent = newPriceText;
            console.log(`💰 更新价格: ${product.name} -> ${newPriceText}`);
        }
        
        if (priceRmbElement) {
            // 计算人民币价格 (使用动态汇率)
            const rmbPrice = Math.round(product.price_usd * this.usdtToCnyRate);
            const newRmbText = `≈ ¥${rmbPrice}/${product.price_unit}`;
            priceRmbElement.textContent = newRmbText;
            console.log(`💱 更新人民币价格: ${product.name} -> ${newRmbText} (汇率: ${this.usdtToCnyRate})`);
        }
    }

    // 改进的产品名称匹配函数
    matchProductName(titleText, productName) {
        if (!titleText || !productName) return false;
        
        // 精确匹配
        if (titleText === productName) return true;
        
        // 常见的名称变换匹配
        const nameMap = {
            'AI風暴組合套餐': ['AI風暴組合套餐', 'AI风暴组合套餐'],
            'ChatGPT Pro': ['ChatGPT Pro'],
            'Claude Max 5x': ['Claude Max 5x'],
            'Super Grok': ['Super Grok'],
            'Cursor Pro': ['Cursor Pro'],
            'Lovable Pro 200 Credit': ['Lovable Pro 200 Credit', 'Lovable Pro']
        };
        
        for (const [key, variations] of Object.entries(nameMap)) {
            if (variations.includes(titleText) && (key === productName || variations.includes(productName))) {
                return true;
            }
        }
        
        return false;
    }

    // 更新页面上的产品显示
    updateProductDisplay() {
        const productCards = document.querySelectorAll('.product-card');
        
        if (productCards.length === 0) {
            console.warn('⚠️ 页面上没有找到产品卡片');
            return;
        }
        
        console.log(`🔄 更新 ${productCards.length} 个产品卡片的显示`);
        
        productCards.forEach((card, index) => {
            // 尝试从产品卡片中提取产品标识信息
            const productTitle = card.querySelector('h3')?.textContent.trim();
            const productLink = card.querySelector('a[href*="pages/"]')?.getAttribute('href');
            
            // 根据标题或链接匹配产品
            let product = null;
            
            if (productTitle) {
                // 首先尝试按名称精确匹配
                product = this.products.find(p => p.name === productTitle);
                
                // 如果没找到，尝试模糊匹配
                if (!product) {
                    product = this.products.find(p => 
                        p.name.includes(productTitle) || 
                        productTitle.includes(p.name)
                    );
                }
                
                // 特殊情况处理
                if (!product && productTitle === 'AI風暴組合套餐') {
                    product = this.products.find(p => 
                        p.slug === 'ai-storm-combo' || 
                        p.name.includes('AI風暴') ||
                        p.name.includes('组合') ||
                        p.name.includes('套餐')
                    );
                }
            }
            
            // 如果还是没找到，尝试从链接中提取slug
            if (!product && productLink) {
                const slugMatch = productLink.match(/pages\/([^.]+)\.html/);
                if (slugMatch) {
                    const pageSlug = slugMatch[1];
                    // 映射页面名称到产品slug
                    const slugMap = {
                        'chatgpt': 'chatgpt-pro',
                        'claude': 'claude-max-5x',
                        'grok': 'super-grok',
                        'cursor': 'cursor-pro',
                        'lovable': 'lovable-pro-200-credit'
                    };
                    const productSlug = slugMap[pageSlug];
                    if (productSlug) {
                        product = this.products.find(p => p.slug === productSlug);
                    }
                }
            }
            
            // 如果仍然没找到，尝试按索引匹配（最后的回退方案）
            if (!product && index < this.products.length) {
                product = this.products[index];
                console.warn(`⚠️ 使用索引匹配产品: ${productTitle} -> ${product.name}`);
            }
            
            if (product) {
                console.log(`✅ 匹配产品: ${productTitle} -> ${product.name} (库存: ${product.stock_quantity})`);
                this.addStockInfo(card, product);
                this.updateStockStatus(card, product);
            } else {
                console.warn('❌ 无法匹配产品卡片:', productTitle || '未知产品', '索引:', index);
            }
        });
        
        // 添加数据源指示器
        this.addDataSourceIndicator();
    }

    // 添加数据源指示器
    addDataSourceIndicator() {
        // 移除现有指示器
        const existingIndicator = document.querySelector('.data-source-indicator');
        if (existingIndicator) {
            existingIndicator.remove();
        }
        
        // 创建新指示器
        const indicator = document.createElement('div');
        indicator.className = 'data-source-indicator';
        indicator.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: ${this.isUsingStaticData ? '#ff9800' : '#4caf50'};
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        `;
        indicator.textContent = this.isUsingStaticData ? '📦 静态数据' : '🌐 实时数据';
        indicator.title = this.isUsingStaticData ? 
            '当前使用静态数据，API连接失败' : 
            '当前使用实时API数据';
        
        document.body.appendChild(indicator);
        
        // 5秒后自动隐藏
        setTimeout(() => {
            if (indicator.parentNode) {
                indicator.style.opacity = '0';
                indicator.style.transition = 'opacity 0.5s';
                setTimeout(() => indicator.remove(), 500);
            }
        }, 5000);
    }

    // 添加库存信息到产品卡片
    addStockInfo(card, product) {
        // 查找价格区域
        const priceElement = card.querySelector('.price');
        if (priceElement) {
            // 检查是否已经添加了库存信息
            let stockElement = card.querySelector('.stock-info');
            if (!stockElement) {
                stockElement = document.createElement('div');
                stockElement.className = 'stock-info';
                
                // 在价格后面插入库存信息
                const priceRmbElement = card.querySelector('.price-rmb');
                if (priceRmbElement) {
                    priceRmbElement.parentNode.insertBefore(stockElement, priceRmbElement.nextSibling);
                } else {
                    priceElement.parentNode.insertBefore(stockElement, priceElement.nextSibling);
                }
            }

            // 更新库存显示
            this.updateStockElement(stockElement, product);
        }
    }

    // 更新库存元素的内容
    updateStockElement(stockElement, product) {
        const stockStatus = this.getStockStatus(product);
        
        stockElement.innerHTML = `
            <div style="
                margin: 0.5rem 0;
                padding: 0.3rem 0.8rem;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: 500;
                text-align: center;
                background: ${stockStatus.bgColor};
                color: ${stockStatus.textColor};
                border: 1px solid ${stockStatus.borderColor};
            ">
                <span style="margin-right: 5px;">${stockStatus.icon}</span>
                ${stockStatus.text}
            </div>
        `;
    }

    // 获取库存状态信息
    getStockStatus(product) {
        if (!product.in_stock || product.stock_quantity <= 0) {
            return {
                text: '暂时缺货',
                icon: '❌',
                bgColor: 'rgba(255, 82, 82, 0.1)',
                textColor: '#FF5252',
                borderColor: '#FF5252'
            };
        } else if (product.stock_quantity <= 10) {
            return {
                text: `仅剩 ${product.stock_quantity} 个`,
                icon: '⚠️',
                bgColor: 'rgba(255, 193, 7, 0.1)',
                textColor: '#FFC107',
                borderColor: '#FFC107'
            };
        } else if (product.stock_quantity <= 50) {
            return {
                text: `库存 ${product.stock_quantity} 个`,
                icon: '📦',
                bgColor: 'rgba(0, 229, 255, 0.1)',
                textColor: '#00E5FF',
                borderColor: '#00E5FF'
            };
        } else {
            return {
                text: `充足库存 (${product.stock_quantity}+)`,
                icon: '✅',
                bgColor: 'rgba(57, 255, 20, 0.1)',
                textColor: '#39FF14',
                borderColor: '#39FF14'
            };
        }
    }

    // 更新产品卡片的整体状态
    updateStockStatus(card, product) {
        const button = card.querySelector('.cta-button');
        
        if (!product.in_stock || product.stock_quantity <= 0) {
            // 缺货状态
            if (button) {
                button.style.opacity = '0.5';
                button.style.cursor = 'not-allowed';
                button.textContent = '暂时缺货';
                button.onclick = (e) => {
                    e.preventDefault();
                    alert('该产品暂时缺货，请联系客服了解补货时间。');
                };
            }
            card.style.opacity = '0.8';
        } else {
            // 有库存状态
            if (button) {
                button.style.opacity = '1';
                button.style.cursor = 'pointer';
                button.onclick = null; // 移除点击阻止
            }
            card.style.opacity = '1';
        }
    }

    // 刷新产品数据
    async refresh() {
        try {
            await this.loadProductsWithRetry();
            this.updateProductDisplay();
            this.updateProductPrices();
        } catch (error) {
            console.warn('刷新产品数据失败:', error);
        }
    }

    // 获取特定产品的库存信息
    getProductStock(slug) {
        const product = this.products.find(p => p.slug === slug);
        return product ? {
            in_stock: product.in_stock,
            stock_quantity: product.stock_quantity,
            status: this.getStockStatus(product)
        } : null;
    }

    // 启动定期刷新
    startPeriodicRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        
        // 每30秒刷新一次库存信息（仅在使用API数据时）
        this.refreshInterval = setInterval(async () => {
            if (!this.isUsingStaticData) {
                try {
                    await this.refresh();
                } catch (error) {
                    console.warn('定期刷新失败:', error);
                }
            }
        }, 30000);
    }

    // 获取调试信息
    getDebugInfo() {
        return {
            apiBaseUrl: this.apiBaseUrl,
            isUsingStaticData: this.isUsingStaticData,
            productsCount: this.products.length,
            retryCount: this.retryCount,
            hasRefreshInterval: !!this.refreshInterval
        };
    }
}

// 页面加载完成后初始化产品管理器
document.addEventListener('DOMContentLoaded', function() {
    // 检查是否在首页
    if (document.querySelector('.products-grid')) {
        window.productManager = new ProductManager();
        
        // 添加调试信息到控制台
        setTimeout(() => {
            if (window.productManager) {
                console.log('🔍 产品管理器调试信息:', window.productManager.getDebugInfo());
            }
        }, 2000);
    }
});

// 导出给其他页面使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductManager;
} 