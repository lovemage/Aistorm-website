// 产品管理和库存显示功能
class ProductManager {
    constructor() {
        // 使用全局API配置
        this.apiBaseUrl = window.apiConfig ? window.apiConfig.getBaseUrl() : this.getApiBaseUrl();
        this.products = [];
        this.init();
    }

    // 备用API URL检测方法（如果全局配置不可用）
    getApiBaseUrl() {
        const currentHost = window.location.hostname;
        const currentPort = window.location.port;
        
        // 如果当前页面就在5001端口，使用相对路径
        if (currentPort === '5001') {
            return '/api';
        }
        
        // 如果是本地开发环境
        if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
            return 'http://localhost:5001/api';
        }
        
        // 如果是远程部署，尝试使用相同域名的5001端口
        if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
            return `${window.location.protocol}//${currentHost}:5001/api`;
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
            
            await this.loadProducts();
            this.updateProductDisplay();
            
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

    // 从后端API加载产品数据
    async loadProducts() {
        try {
            if (window.apiConfig) {
                window.apiConfig.logRequest('GET', '/products');
            }
            
            const response = await fetch(`${this.apiBaseUrl}/products`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                timeout: 10000 // 10秒超时
            });
            
            if (window.apiConfig) {
                window.apiConfig.logResponse('GET', '/products', response);
            }
            
            if (response.ok) {
                this.products = await response.json();
                this.isUsingStaticData = false;
                console.log('✅ 产品数据加载成功:', this.products);
            } else {
                console.error('❌ 加载产品数据失败:', response.status);
                throw new Error(`API响应错误: ${response.status}`);
            }
        } catch (error) {
            console.error('❌ API请求失败:', error);
            // 如果API不可用，使用静态数据作为后备
            console.log('🔄 使用静态数据作为后备');
            this.products = this.getStaticProducts();
            this.isUsingStaticData = true;
        }
    }

    // 静态产品数据作为后备
    getStaticProducts() {
        return [
            {
                name: 'AI風暴組合套餐',
                slug: 'ai-storm-combo',
                in_stock: true,
                stock_quantity: 25
            },
            {
                name: 'ChatGPT Pro',
                slug: 'chatgpt-pro',
                in_stock: true,
                stock_quantity: 50
            },
            {
                name: 'Claude Max 5x',
                slug: 'claude-max-5x',
                in_stock: true,
                stock_quantity: 30
            },
            {
                name: 'Super Grok',
                slug: 'super-grok',
                in_stock: true,
                stock_quantity: 100
            },
            {
                name: 'Cursor Pro',
                slug: 'cursor-pro',
                in_stock: true,
                stock_quantity: 200
            },
            {
                name: 'Lovable Pro 200 Credit',
                slug: 'lovable-pro-200-credit',
                in_stock: true,
                stock_quantity: 80
            }
        ];
    }

    // 更新页面上的产品显示
    updateProductDisplay() {
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach((card) => {
            // 尝试从产品卡片中提取产品标识信息
            const productTitle = card.querySelector('h3')?.textContent.trim();
            const productLink = card.querySelector('a[href*="pages/"]')?.getAttribute('href');
            
            // 根据标题或链接匹配产品
            let product = null;
            
            if (productTitle) {
                // 首先尝试按名称匹配
                product = this.products.find(p => p.name === productTitle);
                
                // 如果没找到，尝试特殊情况
                if (!product && productTitle === 'AI風暴組合套餐') {
                    product = this.products.find(p => p.slug === 'ai-storm-combo' || p.name.includes('AI風暴'));
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
            
            if (product) {
                this.addStockInfo(card, product);
                this.updateStockStatus(card, product);
            } else {
                console.warn('无法匹配产品卡片:', productTitle || '未知产品');
            }
        });
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
        await this.loadProducts();
        this.updateProductDisplay();
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
}

// 页面加载完成后初始化产品管理器
document.addEventListener('DOMContentLoaded', function() {
    // 检查是否在首页
    if (document.querySelector('.products-grid')) {
        window.productManager = new ProductManager();
        
        // 注意：定期刷新现在在ProductManager的init()方法中处理
        // 不需要在这里重复设置定时器
    }
});

// 导出给其他页面使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductManager;
} 