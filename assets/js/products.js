// 产品管理和库存显示功能
class ProductManager {
    constructor() {
        this.apiBaseUrl = window.location.port === '5001' ? '/api' : 'http://localhost:5001/api';
        this.products = [];
        this.init();
    }

    async init() {
        try {
            await this.loadProducts();
            this.updateProductDisplay();
        } catch (error) {
            console.error('初始化产品管理器失败:', error);
        }
    }

    // 从后端API加载产品数据
    async loadProducts() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/products`);
            if (response.ok) {
                this.products = await response.json();
                console.log('产品数据加载成功:', this.products);
            } else {
                console.error('加载产品数据失败:', response.status);
            }
        } catch (error) {
            console.error('API请求失败:', error);
            // 如果API不可用，使用静态数据作为后备
            this.products = this.getStaticProducts();
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
        
        productCards.forEach((card, index) => {
            const product = this.products[index];
            if (product) {
                this.addStockInfo(card, product);
                this.updateStockStatus(card, product);
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
}

// 页面加载完成后初始化产品管理器
document.addEventListener('DOMContentLoaded', function() {
    // 检查是否在首页
    if (document.querySelector('.products-grid')) {
        window.productManager = new ProductManager();
        
        // 每30秒刷新一次库存信息
        setInterval(() => {
            if (window.productManager) {
                window.productManager.refresh();
            }
        }, 30000);
    }
});

// 导出给其他页面使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductManager;
} 