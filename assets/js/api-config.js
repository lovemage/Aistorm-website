// API配置和环境检测
class APIConfig {
    constructor() {
        this.baseUrl = this.detectApiBaseUrl();
        this.debug = this.isDebugMode();
        this.isProduction = this.isProductionEnvironment();
        
        if (this.debug) {
            console.log('🔧 API配置初始化:', {
                baseUrl: this.baseUrl,
                currentHost: window.location.hostname,
                currentPort: window.location.port,
                currentProtocol: window.location.protocol,
                isProduction: this.isProduction
            });
        }
    }

    // 检测是否为生产环境
    isProductionEnvironment() {
        const hostname = window.location.hostname;
        // 检测常见的生产环境域名模式
        return !['localhost', '127.0.0.1', '0.0.0.0'].includes(hostname) &&
               !hostname.includes('.local') &&
               !hostname.includes('192.168.') &&
               !hostname.includes('10.0.') &&
               !hostname.includes('172.');
    }

    // 智能检测API基础URL
    detectApiBaseUrl() {
        const currentHost = window.location.hostname;
        const currentPort = window.location.port;
        const currentProtocol = window.location.protocol;
        
        // 生产环境检测
        if (this.isProductionEnvironment()) {
            // 在生产环境中，前端和后端通常在同一个服务器上
            // 使用相对路径，让浏览器自动使用当前域名和端口
            return '/api';
        }
        
        // 本地开发环境检测
        if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
            // 如果当前页面就在5001端口（后端端口），使用相对路径
            if (currentPort === '5001') {
                return '/api';
            }
            
            // 如果在8000端口（前端端口），连接到5001端口的后端
            if (currentPort === '8000') {
                return 'http://localhost:5001/api';
            }
            
            // 其他本地端口，默认尝试5001
            return 'http://localhost:5001/api';
        }
        
        // 默认回退到相对路径（适用于大多数部署场景）
        return '/api';
    }

    // 检测是否为调试模式
    isDebugMode() {
        return window.location.hostname === 'localhost' || 
               window.location.hostname === '127.0.0.1' ||
               window.location.search.includes('debug=true') ||
               window.location.search.includes('dev=true');
    }

    // 获取API基础URL
    getBaseUrl() {
        return this.baseUrl;
    }

    // 测试API连接
    async testConnection() {
        const urlsToTry = [];
        
        // 根据环境添加不同的URL尝试顺序
        if (this.isProductionEnvironment()) {
            // 生产环境：优先尝试相对路径
            urlsToTry.push('/api');
            urlsToTry.push(`${window.location.protocol}//${window.location.host}/api`);
        } else {
            // 开发环境：按原有逻辑
            urlsToTry.push(this.baseUrl);
            if (this.baseUrl !== '/api') {
                urlsToTry.push('/api');
            }
            urlsToTry.push(`${window.location.protocol}//${window.location.hostname}/api`);
        }
        
        for (const baseUrl of urlsToTry) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 8000); // 8秒超时
                
                const response = await fetch(`${baseUrl}/products`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                const isConnected = response.ok;
                
                if (this.debug) {
                    console.log('🌐 API连接测试:', {
                        url: `${baseUrl}/products`,
                        status: response.status,
                        ok: response.ok,
                        connected: isConnected
                    });
                }
                
                if (isConnected) {
                    // 如果连接成功但不是原始URL，更新baseUrl
                    if (baseUrl !== this.baseUrl) {
                        console.log(`🔄 API URL自动切换: ${this.baseUrl} -> ${baseUrl}`);
                        this.baseUrl = baseUrl;
                    }
                    return true;
                }
                
            } catch (error) {
                if (this.debug) {
                    console.warn(`❌ API连接失败 (${baseUrl}):`, error.message);
                }
                continue; // 尝试下一个URL
            }
        }
        
        if (this.debug) {
            console.error('❌ 所有API URL都连接失败');
        }
        return false;
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

    // 获取环境信息（用于调试）
    getEnvironmentInfo() {
        return {
            hostname: window.location.hostname,
            port: window.location.port,
            protocol: window.location.protocol,
            isProduction: this.isProductionEnvironment(),
            isDebug: this.isDebugMode(),
            apiBaseUrl: this.baseUrl,
            userAgent: navigator.userAgent
        };
    }
}

// 创建全局API配置实例
window.apiConfig = new APIConfig();

// 导出配置（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIConfig;
}

// 页面加载时输出调试信息
document.addEventListener('DOMContentLoaded', function() {
    if (window.apiConfig.getEnvironmentInfo().isDevelopment) {
        window.apiConfig.debug();
    }
}); 