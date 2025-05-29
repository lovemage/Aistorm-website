// 单个产品详情页面的库存管理
class ProductDetailManager {
    constructor(productSlug) {
        // 使用全局API配置
        this.apiBaseUrl = window.apiConfig ? window.apiConfig.getBaseUrl() : this.getApiBaseUrl();
        this.productSlug = productSlug;
        this.product = null;
        this.usdtToCnyRate = 8.0; // 默认汇率
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
            // 获取汇率设置
            await this.loadSiteSettings();
            
            await this.loadProduct();
            this.updateProductDisplay();
        } catch (error) {
            console.error('初始化产品详情管理器失败:', error);
            // 使用静态数据作为后备
            this.product = this.getStaticProduct();
            this.updateProductDisplay();
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
                    console.log('💱 产品详情页获取汇率设置:', this.usdtToCnyRate);
                }
            }
        } catch (error) {
            console.warn('⚠️ 获取站点设置失败，使用默认汇率:', this.usdtToCnyRate);
        }
    }

    // 从后端API加载单个产品数据
    async loadProduct() {
        try {
            if (window.apiConfig) {
                window.apiConfig.logRequest('GET', `/products/${this.productSlug}`);
            }
            
            const response = await fetch(`${this.apiBaseUrl}/products/${this.productSlug}`);
            
            if (window.apiConfig) {
                window.apiConfig.logResponse('GET', `/products/${this.productSlug}`, response);
            }
            
            if (response.ok) {
                this.product = await response.json();
                console.log('✅ 产品详情加载成功:', this.product);
            } else {
                console.error('❌ 加载产品详情失败:', response.status);
                throw new Error('API请求失败');
            }
        } catch (error) {
            console.error('❌ API请求失败:', error);
            throw error;
        }
    }

    // 静态产品数据作为后备
    getStaticProduct() {
        const staticProducts = {
            'chatgpt-pro': {
                name: 'ChatGPT Pro',
                slug: 'chatgpt-pro',
                in_stock: true,
                stock_quantity: 50,
                price_usd: 130,
                price_unit: '月'
            },
            'claude-max-5x': {
                name: 'Claude Max 5x',
                slug: 'claude-max-5x',
                in_stock: true,
                stock_quantity: 30,
                price_usd: 75,
                price_unit: '月'
            },
            'super-grok': {
                name: 'Super Grok',
                slug: 'super-grok',
                in_stock: true,
                stock_quantity: 100,
                price_usd: 20,
                price_unit: '月'
            },
            'cursor-pro': {
                name: 'Cursor Pro',
                slug: 'cursor-pro',
                in_stock: true,
                stock_quantity: 200,
                price_usd: 12,
                price_unit: '月'
            },
            'lovable-pro-200-credit': {
                name: 'Lovable Pro 200 Credit',
                slug: 'lovable-pro-200-credit',
                in_stock: true,
                stock_quantity: 80,
                price_usd: 35,
                price_unit: '200 Credit'
            }
        };

        return staticProducts[this.productSlug] || {
            name: '未知产品',
            slug: this.productSlug,
            in_stock: true,
            stock_quantity: 999,
            price_usd: 0,
            price_unit: '月'
        };
    }

    // 更新页面上的产品显示
    updateProductDisplay() {
        if (!this.product) return;

        // 更新产品价格显示
        this.updateProductPrices();
        
        // 添加库存信息到产品信息区域
        this.addStockInfoToProductInfo();
        
        // 更新购买按钮状态
        this.updatePurchaseButtons();
        
        // 添加库存状态提示
        this.addStockStatusAlert();
    }

    // 新增：更新产品价格显示
    updateProductPrices() {
        console.log('💰 更新产品详情页面价格显示');
        
        // 更新页面标题中的价格
        const titleElements = document.querySelectorAll('h1, h2, .product-title');
        titleElements.forEach(titleElement => {
            if (titleElement.textContent.includes('$') && titleElement.textContent.includes('USDT')) {
                const originalText = titleElement.textContent;
                const newText = originalText.replace(/\$[\d,]+\.?\d*\s*USDT/g, `$${this.product.price_usd} USDT`);
                if (newText !== originalText) {
                    titleElement.textContent = newText;
                    console.log(`📝 更新标题价格: ${newText}`);
                }
            }
        });
        
        // 更新主要价格显示区域的USDT价格
        const priceElements = document.querySelectorAll('.price, .price-main, .product-price');
        priceElements.forEach(priceElement => {
            if (priceElement.textContent.includes('USDT') || priceElement.textContent.includes('$')) {
                const newPriceText = `$${this.product.price_usd} USDT`;
                priceElement.textContent = newPriceText;
                console.log(`💰 更新详情页价格: ${newPriceText}`);
            }
        });

        // 更新价格单位
        const priceUnitElements = document.querySelectorAll('.price-unit, .unit');
        priceUnitElements.forEach(unitElement => {
            unitElement.textContent = `/ ${this.product.price_unit}`;
        });

        // 更新人民币价格
        const priceRmbElements = document.querySelectorAll('.price-rmb-detail, .price-rmb, .price-cny');
        priceRmbElements.forEach(rmbElement => {
            if (rmbElement.textContent.includes('¥') || rmbElement.textContent.includes('人民币')) {
                const rmbPrice = Math.round(this.product.price_usd * this.usdtToCnyRate);
                const newRmbText = `≈ ¥${rmbPrice} 人民币 / ${this.product.price_unit}`;
                rmbElement.textContent = newRmbText;
                console.log(`💱 更新详情页人民币价格: ${newRmbText}`);
            }
        });

        // 更新所有包含价格信息的文本内容
        const allTextElements = document.querySelectorAll('p, span, div');
        allTextElements.forEach(element => {
            if (element.children.length === 0) { // 只处理叶子节点
                const text = element.textContent;
                if (text.includes('$') && text.includes('USDT') && !text.includes('人民币')) {
                    const newText = text.replace(/\$[\d,]+\.?\d*\s*USDT/g, `$${this.product.price_usd} USDT`);
                    if (newText !== text) {
                        element.textContent = newText;
                        console.log(`🔄 更新文本价格: ${newText}`);
                    }
                }
            }
        });
    }

    // 在产品信息区域添加库存信息
    addStockInfoToProductInfo() {
        const productInfo = document.querySelector('.product-info');
        if (!productInfo) return;

        // 查找价格区域或产品标题区域
        const priceElement = productInfo.querySelector('.price') || 
                           productInfo.querySelector('h2') ||
                           productInfo.querySelector('h1');
        
        if (priceElement) {
            // 检查是否已经添加了库存信息
            let stockElement = productInfo.querySelector('.stock-info-detail');
            if (!stockElement) {
                stockElement = document.createElement('div');
                stockElement.className = 'stock-info-detail';
                
                // 在价格后面或标题后面插入库存信息
                priceElement.parentNode.insertBefore(stockElement, priceElement.nextSibling);
            }

            // 更新库存显示
            this.updateStockElement(stockElement);
        }
    }

    // 更新库存元素的内容
    updateStockElement(stockElement) {
        const stockStatus = this.getStockStatus();
        
        stockElement.innerHTML = `
            <div style="
                margin: 1rem 0;
                padding: 0.8rem 1.2rem;
                border-radius: 12px;
                font-size: 0.95rem;
                font-weight: 600;
                text-align: center;
                background: ${stockStatus.bgColor};
                color: ${stockStatus.textColor};
                border: 2px solid ${stockStatus.borderColor};
                box-shadow: 0 4px 12px ${stockStatus.bgColor};
            ">
                <span style="margin-right: 8px; font-size: 1.1em;">${stockStatus.icon}</span>
                ${stockStatus.text}
            </div>
        `;
    }

    // 获取库存状态信息
    getStockStatus() {
        if (!this.product.in_stock || this.product.stock_quantity <= 0) {
            return {
                text: '暂时缺货 - 请联系客服了解补货时间',
                icon: '❌',
                bgColor: 'rgba(255, 82, 82, 0.15)',
                textColor: '#FF5252',
                borderColor: '#FF5252'
            };
        } else if (this.product.stock_quantity <= 10) {
            return {
                text: `库存紧张！仅剩 ${this.product.stock_quantity} 个，欲购从速`,
                icon: '⚠️',
                bgColor: 'rgba(255, 193, 7, 0.15)',
                textColor: '#FFC107',
                borderColor: '#FFC107'
            };
        } else if (this.product.stock_quantity <= 50) {
            return {
                text: `现货充足 - 库存 ${this.product.stock_quantity} 个`,
                icon: '📦',
                bgColor: 'rgba(0, 229, 255, 0.15)',
                textColor: '#00E5FF',
                borderColor: '#00E5FF'
            };
        } else {
            return {
                text: `库存充足 - 立即可发货 (${this.product.stock_quantity}+ 现货)`,
                icon: '✅',
                bgColor: 'rgba(57, 255, 20, 0.15)',
                textColor: '#39FF14',
                borderColor: '#39FF14'
            };
        }
    }

    // 更新购买按钮状态
    updatePurchaseButtons() {
        const buttons = document.querySelectorAll('.cta-button, .purchase-button');
        
        buttons.forEach(button => {
            if (!this.product.in_stock || this.product.stock_quantity <= 0) {
                // 缺货状态
                button.style.opacity = '0.6';
                button.style.cursor = 'not-allowed';
                button.style.background = 'linear-gradient(45deg, #666, #888)';
                
                const originalText = button.textContent;
                if (!originalText.includes('缺货')) {
                    button.setAttribute('data-original-text', originalText);
                    button.textContent = '暂时缺货 - 联系客服';
                }
                
                button.onclick = (e) => {
                    e.preventDefault();
                    alert('该产品暂时缺货，请联系客服了解补货时间和预订信息。');
                };
            } else {
                // 有库存状态
                button.style.opacity = '1';
                button.style.cursor = 'pointer';
                button.style.background = '';
                
                const originalText = button.getAttribute('data-original-text');
                if (originalText) {
                    button.textContent = originalText;
                    button.removeAttribute('data-original-text');
                }
                
                button.onclick = null; // 移除点击阻止
            }
        });
    }

    // 添加库存状态提醒
    addStockStatusAlert() {
        // 如果库存很少，添加紧急提醒
        if (this.product.in_stock && this.product.stock_quantity <= 10 && this.product.stock_quantity > 0) {
            this.showUrgencyAlert();
        }
    }

    // 显示紧急库存提醒
    showUrgencyAlert() {
        // 检查是否已经显示过提醒
        if (document.querySelector('.urgency-alert')) return;

        const alertDiv = document.createElement('div');
        alertDiv.className = 'urgency-alert';
        alertDiv.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(45deg, #FF6B35, #FF8E53);
                color: white;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
                z-index: 10000;
                max-width: 300px;
                font-size: 0.9rem;
                font-weight: 600;
                animation: slideInRight 0.5s ease-out;
            ">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2em; margin-right: 8px;">🔥</span>
                    <strong>库存紧张提醒</strong>
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" 
                            style="margin-left: auto; background: none; border: none; color: white; font-size: 1.2em; cursor: pointer;">×</button>
                </div>
                <div>仅剩 ${this.product.stock_quantity} 个现货，建议尽快下单！</div>
            </div>
            <style>
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            </style>
        `;

        document.body.appendChild(alertDiv);

        // 10秒后自动消失
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 10000);
    }

    // 刷新产品数据
    async refresh() {
        try {
            await this.loadProduct();
            this.updateProductDisplay();
        } catch (error) {
            console.error('刷新产品数据失败:', error);
        }
    }

    // 获取当前产品的库存信息
    getStockInfo() {
        return this.product ? {
            in_stock: this.product.in_stock,
            stock_quantity: this.product.stock_quantity,
            status: this.getStockStatus()
        } : null;
    }
}

// 自动检测产品slug并初始化
function initProductDetail() {
    // 从URL路径或页面元素中检测产品类型
    const path = window.location.pathname;
    let productSlug = '';

    if (path.includes('chatgpt')) {
        productSlug = 'chatgpt-pro';
    } else if (path.includes('claude')) {
        productSlug = 'claude-max-5x';
    } else if (path.includes('grok')) {
        productSlug = 'super-grok';
    } else if (path.includes('cursor')) {
        productSlug = 'cursor-pro';
    } else if (path.includes('lovable')) {
        productSlug = 'lovable-pro-200-credit';
    }

    if (productSlug) {
        window.productDetailManager = new ProductDetailManager(productSlug);
        
        // 每60秒刷新一次库存信息
        setInterval(() => {
            if (window.productDetailManager) {
                window.productDetailManager.refresh();
            }
        }, 60000);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initProductDetail);

// 导出给其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductDetailManager;
} 