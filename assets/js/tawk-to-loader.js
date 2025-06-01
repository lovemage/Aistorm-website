/**
 * Tawk.to 动态加载器
 * 根据后台配置动态加载Tawk.to在线客服脚本
 */

// 全局Tawk.to配置
window.TawkToConfig = {
    enabled: false,
    propertyId: '',
    widgetId: '',
    loaded: false
};

/**
 * 加载Tawk.to配置
 */
async function loadTawkToConfig() {
    try {
        const apiBaseUrl = window.apiConfig ? window.apiConfig.getBaseUrl() : '/api';
        const response = await fetch(`${apiBaseUrl.replace('/api', '')}/api/settings`);
        
        if (response.ok) {
            const settings = await response.json();
            
            window.TawkToConfig = {
                enabled: settings.tawk_to_enabled || false,
                propertyId: settings.tawk_to_property_id || '',
                widgetId: settings.tawk_to_widget_id || '',
                loaded: false
            };
            
            console.log('✅ Tawk.to配置加载成功:', window.TawkToConfig);
            
            // 如果启用了Tawk.to，则加载脚本
            if (window.TawkToConfig.enabled && window.TawkToConfig.propertyId && window.TawkToConfig.widgetId) {
                loadTawkToScript();
            } else {
                console.log('ℹ️ Tawk.to未启用或配置不完整');
            }
        } else {
            console.warn('⚠️ 无法获取Tawk.to配置，使用默认设置');
            // 使用默认配置
            window.TawkToConfig = {
                enabled: true,
                propertyId: '683c81902022f41910633ceb',
                widgetId: '1ism5k77i',
                loaded: false
            };
            loadTawkToScript();
        }
    } catch (error) {
        console.warn('⚠️ Tawk.to配置加载失败，使用默认设置:', error.message);
        // 使用默认配置
        window.TawkToConfig = {
            enabled: true,
            propertyId: '683c81902022f41910633ceb',
            widgetId: '1ism5k77i',
            loaded: false
        };
        loadTawkToScript();
    }
}

/**
 * 动态加载Tawk.to脚本
 */
function loadTawkToScript() {
    if (window.TawkToConfig.loaded) {
        console.log('ℹ️ Tawk.to脚本已加载');
        return;
    }
    
    if (!window.TawkToConfig.enabled) {
        console.log('ℹ️ Tawk.to已禁用');
        return;
    }
    
    if (!window.TawkToConfig.propertyId || !window.TawkToConfig.widgetId) {
        console.warn('⚠️ Tawk.to配置不完整，无法加载');
        return;
    }
    
    try {
        // 初始化Tawk_API
        window.Tawk_API = window.Tawk_API || {};
        window.Tawk_LoadStart = new Date();
        
        // 创建脚本元素
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://embed.tawk.to/${window.TawkToConfig.propertyId}/${window.TawkToConfig.widgetId}`;
        script.charset = 'UTF-8';
        script.setAttribute('crossorigin', '*');
        
        // 添加加载成功回调
        script.onload = function() {
            window.TawkToConfig.loaded = true;
            console.log('✅ Tawk.to脚本加载成功');
            
            // 可以在这里添加自定义配置
            if (window.Tawk_API) {
                // 设置访客信息（如果需要）
                window.Tawk_API.onLoad = function() {
                    console.log('✅ Tawk.to聊天窗口已加载');
                };
                
                // 设置聊天开始回调
                window.Tawk_API.onChatStarted = function() {
                    console.log('💬 用户开始聊天');
                };
            }
        };
        
        // 添加加载失败回调
        script.onerror = function() {
            console.error('❌ Tawk.to脚本加载失败');
        };
        
        // 插入脚本到页面
        const firstScript = document.getElementsByTagName('script')[0];
        firstScript.parentNode.insertBefore(script, firstScript);
        
        console.log('🚀 开始加载Tawk.to脚本:', script.src);
        
    } catch (error) {
        console.error('❌ Tawk.to脚本加载异常:', error);
    }
}

/**
 * 手动启用Tawk.to（用于测试）
 */
function enableTawkTo(propertyId, widgetId) {
    window.TawkToConfig = {
        enabled: true,
        propertyId: propertyId || '683c81902022f41910633ceb',
        widgetId: widgetId || '1ism5k77i',
        loaded: false
    };
    loadTawkToScript();
}

/**
 * 禁用Tawk.to
 */
function disableTawkTo() {
    window.TawkToConfig.enabled = false;
    
    // 如果已经加载，尝试隐藏聊天窗口
    if (window.Tawk_API && window.Tawk_API.hideWidget) {
        window.Tawk_API.hideWidget();
        console.log('🔒 Tawk.to聊天窗口已隐藏');
    }
}

/**
 * 显示Tawk.to聊天窗口
 */
function showTawkTo() {
    if (window.Tawk_API && window.Tawk_API.showWidget) {
        window.Tawk_API.showWidget();
        console.log('👁️ Tawk.to聊天窗口已显示');
    }
}

/**
 * 隐藏Tawk.to聊天窗口
 */
function hideTawkTo() {
    if (window.Tawk_API && window.Tawk_API.hideWidget) {
        window.Tawk_API.hideWidget();
        console.log('🔒 Tawk.to聊天窗口已隐藏');
    }
}

/**
 * 获取Tawk.to状态
 */
function getTawkToStatus() {
    return {
        config: window.TawkToConfig,
        apiLoaded: !!window.Tawk_API,
        widgetVisible: window.Tawk_API && window.Tawk_API.getWindowType ? window.Tawk_API.getWindowType() !== null : false
    };
}

// 页面加载完成后自动加载配置
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTawkToConfig);
} else {
    loadTawkToConfig();
}

// 导出函数供全局使用
window.TawkToLoader = {
    loadConfig: loadTawkToConfig,
    loadScript: loadTawkToScript,
    enable: enableTawkTo,
    disable: disableTawkTo,
    show: showTawkTo,
    hide: hideTawkTo,
    getStatus: getTawkToStatus
}; 