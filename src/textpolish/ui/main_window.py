#!/usr/bin/env python3
"""
主窗口模块 - 应用程序的主窗口组件
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon as FIF, qconfig, SystemThemeListener, isDarkTheme

from .main_interface import TextPolishInterface
from ..utils.icon import IconManager
from ..config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class TextPolishWindow(FluentWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.initWindow()
        self.initThemeListener()
    
    def initWindow(self):
        """初始化窗口"""
        # 创建主界面
        self.homeInterface = TextPolishInterface(self)
        
        # 添加到导航
        self.addSubInterface(
            self.homeInterface,
            FIF.EDIT,
            "文本处理",
            position=NavigationItemPosition.TOP
        )
        
        # 添加配置界面
        self.add_config_interface()
        
        # 设置窗口属性
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 设置窗口图标
        IconManager.set_window_icon(self)
        
        # 居中显示
        self.center_window()
        
        # 设置当前界面
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
        
        # 连接信号
        self.homeInterface.status_updated.connect(self.update_status)
        self.homeInterface.set_config_interface(self.configInterface)  # 让主界面可以访问配置界面
        qconfig.themeChanged.connect(self.on_theme_changed)
        
        # 初始状态
        self.base_title = APP_TITLE
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = screen.width(), screen.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
    
    def update_status(self, message: str):
        """
        更新状态显示
        
        Args:
            message: 状态消息
        """
        if message == "正在处理...":
            self.setWindowTitle(f"{self.base_title} - {message}")
        else:
            self.setWindowTitle(self.base_title)
    
    def on_theme_changed(self, theme):
        """
        主题切换时的处理
        
        Args:
            theme: 新主题
        """
        # 通知界面更新预览
        self.homeInterface.update_preview_theme()
    
    def initThemeListener(self):
        """初始化系统主题监听器"""
        # 创建主题监听器
        self.themeListener = SystemThemeListener(self)
        # 启动监听器
        self.themeListener.start()
    
    def closeEvent(self, e):
        """窗口关闭事件处理"""
        # 停止主题监听器线程
        if hasattr(self, 'themeListener'):
            self.themeListener.terminate()
            self.themeListener.deleteLater()
        super().closeEvent(e)
    
    def _onThemeChangedFinished(self):
        """主题切换完成后的处理"""
        super()._onThemeChangedFinished()
        
        # 云母特效启用时需要增加重试机制
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))
    
    def add_config_interface(self):
        """添加配置界面"""
        # 创建配置界面
        from .config_interface import ConfigInterface
        self.configInterface = ConfigInterface(self)
        
        # 添加到导航
        self.addSubInterface(
            self.configInterface,
            FIF.SETTING,
            "配置设置",
            position=NavigationItemPosition.BOTTOM
        )
