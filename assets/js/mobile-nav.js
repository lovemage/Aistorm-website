// 移动端导航菜单控制
document.addEventListener('DOMContentLoaded', function() {
  const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  
  if (mobileMenuToggle && mobileNav) {
    // 点击汉堡菜单按钮切换菜单
    mobileMenuToggle.addEventListener('click', function() {
      mobileMenuToggle.classList.toggle('active');
      mobileNav.classList.toggle('active');
    });
    
    // 点击菜单项后关闭菜单
    const mobileNavLinks = mobileNav.querySelectorAll('a');
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', function() {
        mobileMenuToggle.classList.remove('active');
        mobileNav.classList.remove('active');
      });
    });
    
    // 点击页面其他地方关闭菜单
    document.addEventListener('click', function(event) {
      if (!mobileMenuToggle.contains(event.target) && !mobileNav.contains(event.target)) {
        mobileMenuToggle.classList.remove('active');
        mobileNav.classList.remove('active');
      }
    });
    
    // ESC键关闭菜单
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape') {
        mobileMenuToggle.classList.remove('active');
        mobileNav.classList.remove('active');
      }
    });
  }
}); 