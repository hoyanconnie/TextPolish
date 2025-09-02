#!/usr/bin/env python3
"""
主窗口模块 - 应用程序的主窗口组件
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from qfluentwidgets import FluentWindow, NavigationItemPosition, FluentIcon as FIF, qconfig

from .main_interface import TextPolishInterface
from ..utils.icon import IconManager
from ..config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


class TextPolishWindow(FluentWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.initWindow()
    
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
