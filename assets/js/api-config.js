// API配置和环境检测
class APIConfig {
    constructor() {
        this.baseUrl = this.detectApiBaseUrl();
        this.debug = this.isDebugMode();
        
        if (this.debug) {
            console.log('🔧 API配置初始化:', {
                baseUrl: this.baseUrl,
                currentHost: window.location.hostname,
                currentPort: window.location.port,
                currentProtocol: window.location.protocol
            });
        }
    }

    // 智能检测API基础URL
    detectApiBaseUrl() {
        const currentHost = window.location.hostname;
        const currentPort = window.location.port;
        const currentProtocol = window.location.protocol;
        
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
            return `${currentProtocol}//${currentHost}:5001/api`;
        }
        
        // 默认回退到相对路径
        return '/api';
    }

    // 检测是否为调试模式
    isDebugMode() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.search.includes('debug=true');
    }

    // 获取API基础URL
    getBaseUrl() {
        return this.baseUrl;
    }

    // 测试API连接
    async testConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/products`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const isConnected = response.ok;
            
            if (this.debug) {
                console.log('🌐 API连接测试:', {
                    url: `${this.baseUrl}/products`,
                    status: response.status,
                    ok: response.ok,
                    connected: isConnected
                });
            }
            
            return isConnected;
        } catch (error) {
            if (this.debug) {
                console.error('❌ API连接失败:', error);
            }
            return false;
        }
    }

    // 记录API请求
    logRequest(method, endpoint, data = null) {
        if (this.debug) {
            console.log(`📡 API请求: ${method} ${this.baseUrl}${endpoint}`, data ? { data } : '');
        }
    }

    // 记录API响应
    logResponse(method, endpoint, response, data = null) {
        if (this.debug) {
            console.log(`📨 API响应: ${method} ${this.baseUrl}${endpoint}`, {
                status: response.status,
                ok: response.ok,
                data: data
            });
        }
    }
}

// 创建全局API配置实例
window.apiConfig = new APIConfig();

// 导出配置（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIConfig;
} 