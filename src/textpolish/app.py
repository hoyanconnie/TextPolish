#!/usr/bin/env python3
"""
应用程序入口模块 - 负责初始化和启动应用程序
"""

import sys


class TextPolishApp:
    """TextPolish应用程序类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.app = None
        self.window = None
    
    def create_application(self):
        """
        创建QApplication实例
        
        Returns:
            QApplication实例
        """
        from PyQt6.QtWidgets import QApplication
        from qfluentwidgets import Theme, setTheme
        from .utils.icon import IconManager
        from .config import APP_NAME, APP_VERSION, APP_ORGANIZATION
        
        app = QApplication(sys.argv)
        
        # 设置应用信息
        app.setApplicationName(APP_NAME)
        app.setApplicationVersion(APP_VERSION)
        app.setOrganizationName(APP_ORGANIZATION)
        
        # 设置应用程序图标
        IconManager.set_app_icon(app)
        
        # 设置主题
        setTheme(Theme.AUTO)
        
        return app
    
    def create_main_window(self):
        """
        创建主窗口
        
        Returns:
            TextPolishWindow实例
        """
        from .ui.main_window import TextPolishWindow
        return TextPolishWindow()
    
    def run(self) -> int:
        """
        运行应用程序
        
        Returns:
            应用程序退出代码
        """
        try:
            # 创建应用实例
            self.app = self.create_application()
            
            # 创建主窗口
            self.window = self.create_main_window()
            self.window.show()
            
            # 启动事件循环
            return self.app.exec()
            
        except Exception as e:
            print(f"程序启动失败: {e}")
            return 1


def main() -> int:
    """
    主函数入口
    
    Returns:
        应用程序退出代码
    """
    app = TextPolishApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
