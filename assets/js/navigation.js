/**
 * 响应式导航菜单控制器
 * 处理汉堡菜单的显示/隐藏和相关交互
 */

class NavigationController {
  constructor() {
    this.navToggle = document.querySelector('.nav-toggle');
    this.navDropdown = document.querySelector('.nav-dropdown');
    this.navDropdownLinks = document.querySelectorAll('.nav-dropdown-link');
    this.isOpen = false;
    
    // 调试信息
    console.log('NavigationController 初始化', {
      navToggle: this.navToggle,
      navDropdown: this.navDropdown,
      navDropdownLinks: this.navDropdownLinks
    });
    
    this.init();
  }
  
  init() {
    // 绑定汉堡菜单点击事件
    if (this.navToggle) {
      this.navToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        this.toggleMenu();
      });
    } else {
      console.error('导航切换按钮未找到');
    }
    
    // 绑定下拉菜单链接点击事件（移动端点击后关闭菜单）
    this.navDropdownLinks.forEach(link => {
      link.addEventListener('click', () => {
        // 延迟关闭，让页面导航先发生
        setTimeout(() => {
          this.closeMenu();
        }, 100);
      });
    });
    
    // 点击外部区域关闭菜单
    document.addEventListener('click', this.handleOutsideClick.bind(this));
    
    // 监听窗口大小变化
    window.addEventListener('resize', this.handleResize.bind(this));
    
    // ESC键关闭菜单
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.isOpen) {
        this.closeMenu();
      }
    });
  }
  
  toggleMenu() {
    console.log('切换菜单状态', this.isOpen);
    if (this.isOpen) {
      this.closeMenu();
    } else {
      this.openMenu();
    }
  }
  
  openMenu() {
    if (!this.navDropdown) {
      console.error('下拉菜单元素未找到');
      return;
    }
    
    this.isOpen = true;
    this.navToggle.classList.add('active');
    this.navDropdown.classList.add('active');
    
    // 禁止页面滚动
    document.body.style.overflow = 'hidden';
    
    console.log('菜单已打开');
  }
  
  closeMenu() {
    if (!this.navDropdown) {
      console.error('下拉菜单元素未找到');
      return;
    }
    
    this.isOpen = false;
    this.navToggle.classList.remove('active');
    this.navDropdown.classList.remove('active');
    
    // 恢复页面滚动
    document.body.style.overflow = '';
    
    console.log('菜单已关闭');
  }
  
  handleOutsideClick(e) {
    // 如果点击的不是导航区域，则关闭菜单
    if (this.isOpen && 
        this.navToggle && 
        this.navDropdown &&
        !this.navToggle.contains(e.target) && 
        !this.navDropdown.contains(e.target)) {
      this.closeMenu();
    }
  }
  
  handleResize() {
    // 当窗口大小变化到桌面端时，自动关闭移动端菜单
    if (window.innerWidth > 768 && this.isOpen) {
      this.closeMenu();
    }
  }
}

// 页面加载完成后初始化导航控制器
document.addEventListener('DOMContentLoaded', () => {
  // 确保DOM完全加载
  setTimeout(() => {
    const controller = new NavigationController();
    window.navigationController = controller; // 暴露给全局便于调试
  }, 100);
});

// 导出供其他脚本使用
if (typeof module !== 'undefined' && module.exports) {
  module.exports = NavigationController;
} 