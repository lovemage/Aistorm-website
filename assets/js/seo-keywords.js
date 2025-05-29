// SEO关键字配置文件
// 统一管理所有产品的SEO关键字，便于维护和更新

const SEO_KEYWORDS = {
  // 通用关键字
  common: [
    'AIStorm',
    'AI账号购买',
    '人工智能账号',
    'AI账号充值',
    'AI账号代购',
    'USDT支付',
    '加密货币支付',
    '科技AI',
    'AI解决方案',
    'AI工具购买',
    'AI服务购买',
    'AI账号代理',
    'AI账号批发',
    'AI账号零售',
    '人工智能服务'
  ],

  // ChatGPT相关关键字
  chatgpt: [
    'ChatGPT Pro',
    'ChatGPT账号',
    'ChatGPT账号购买',
    'ChatGPT账号充值',
    'ChatGPT Pro购买',
    'ChatGPT Pro账号',
    'ChatGPT代购',
    'ChatGPT账号代理',
    'GPT-4',
    'GPT-4账号',
    'OpenAI账号',
    'OpenAI账号购买',
    'OpenAI Pro',
    'ChatGPT Plus',
    'ChatGPT订阅',
    'AI写作助手',
    'AI代码助手',
    '智能对话',
    'ChatGPT官方账号',
    'ChatGPT正版账号',
    'ChatGPT安全购买'
  ],

  // Claude相关关键字
  claude: [
    'Claude Max 5x',
    'Claude账号',
    'Claude账号购买',
    'Claude账号充值',
    'Claude Max账号',
    'Claude代购',
    'Claude账号代理',
    'Claude-3 Opus',
    'Claude-3账号',
    'Anthropic账号',
    'Anthropic账号购买',
    'Claude Pro',
    'Claude订阅',
    'Claude Plus',
    'AI写作助手',
    'AI分析助手',
    'Claude官方账号',
    'Claude正版账号',
    'Claude安全购买',
    'AI文本生成',
    'AI创作助手'
  ],

  // Grok相关关键字
  grok: [
    'Super Grok',
    'Grok账号',
    'Grok账号购买',
    'Grok账号充值',
    'Grok Pro',
    'Grok代购',
    'Grok账号代理',
    'X AI',
    'Twitter AI',
    'Grok AI',
    'X平台AI',
    '实时资讯',
    '社交媒體AI',
    'Elon Musk AI',
    'Grok订阅',
    'Grok Plus',
    'AI新闻助手',
    '实时AI',
    '社交AI',
    'Grok官方账号',
    'Grok正版账号',
    'Grok安全购买',
    'X Premium',
    'Twitter Premium'
  ],

  // Cursor相关关键字
  cursor: [
    'Cursor Pro',
    'Cursor账号',
    'Cursor账号购买',
    'Cursor账号充值',
    'Cursor Pro购买',
    'Cursor代购',
    'Cursor账号代理',
    'AI IDE',
    'AI编程助手',
    'GPT-4 Turbo',
    '代码生成',
    '智能开发工具',
    'AI辅助编程',
    'Cursor編輯器',
    'Cursor订阅',
    'AI代码助手',
    '编程AI工具',
    '开发者AI',
    '智能IDE',
    '代码补全',
    'AI编程环境',
    'Cursor官方账号',
    'Cursor正版账号',
    'Cursor安全购买'
  ],

  // Lovable相关关键字
  lovable: [
    'Lovable Pro',
    'Lovable账号',
    'Lovable账号购买',
    'Lovable账号充值',
    'Lovable Pro购买',
    'Lovable代购',
    'Lovable账号代理',
    '200 Credit',
    'Lovable Credit',
    'AI全棧开发',
    'AI Web开发',
    'AI应用生成',
    '无代码AI',
    '低代码AI',
    'AI网站建設',
    'AI开发平台',
    '全栈AI工具',
    'AI应用构建',
    'Lovable订阅',
    'AI自动化开发',
    '智能开发工具',
    'Lovable官方账号',
    'Lovable正版账号',
    'Lovable安全购买'
  ],

  // 行业相关关键字
  industry: [
    'AI聊天机器人',
    'AI内容生成',
    '長文本处理',
    '专业AI服务',
    'GPT-4 API',
    '企业級AI',
    'AI新闻助手',
    '编程AI工具',
    '开发者AI',
    'AI代码助手',
    'AI写作助手',
    'AI分析助手',
    '智能对话',
    'AI创作助手',
    'AI自动化开发'
  ]
};

// 生成特定产品的关键字字符串
function generateKeywords(productType) {
  const keywords = [
    ...SEO_KEYWORDS.common,
    ...SEO_KEYWORDS[productType] || [],
    ...SEO_KEYWORDS.industry
  ];
  return keywords.join(', ');
}

// 生成首页关键字（包含所有产品）
function generateHomeKeywords() {
  const allKeywords = [
    ...SEO_KEYWORDS.common,
    ...SEO_KEYWORDS.chatgpt.slice(0, 10), // 取前10个主要关键字
    ...SEO_KEYWORDS.claude.slice(0, 8),
    ...SEO_KEYWORDS.grok.slice(0, 8),
    ...SEO_KEYWORDS.cursor.slice(0, 8),
    ...SEO_KEYWORDS.lovable.slice(0, 8),
    ...SEO_KEYWORDS.industry
  ];
  return allKeywords.join(', ');
}

// 导出配置
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SEO_KEYWORDS, generateKeywords, generateHomeKeywords };
} 