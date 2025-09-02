#!/usr/bin/env python3
"""
图标管理模块 - 负责处理应用程序图标
"""

import sys
import os
from typing import Optional
from PyQt6.QtGui import QIcon

from ..config import ICON_PATHS


class IconManager:
    """图标管理器 - 负责加载和管理应用程序图标"""
    
    @staticmethod
    def get_icon_path() -> Optional[str]:
        """
        获取图标文件路径
        
        Returns:
            图标文件路径，如果不存在则返回None
        """
        # 检测是否为打包后的程序
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.getcwd()
        
        # 使用ICO文件
        ico_path = os.path.join(base_path, ICON_PATHS['ico'])
        if os.path.exists(ico_path):
            return ico_path
        
        return None
    
    @staticmethod
    def load_icon() -> Optional[QIcon]:
        """
        加载应用程序图标
        
        Returns:
            QIcon对象，如果加载失败则返回None
        """
        icon_path = IconManager.get_icon_path()
        if icon_path:
            try:
                return QIcon(icon_path)
            except Exception as e:
                print(f"加载图标失败: {e}")
        
        return None
    
    @staticmethod
    def set_app_icon(app) -> bool:
        """
        为应用程序设置图标
        
        Args:
            app: QApplication实例
            
        Returns:
            是否设置成功
        """
        icon = IconManager.load_icon()
        if icon:
            try:
                app.setWindowIcon(icon)
                return True
            except Exception as e:
                print(f"设置应用程序图标失败: {e}")
        
        return False
    
    @staticmethod
    def set_window_icon(window) -> bool:
        """
        为窗口设置图标
        
        Args:
            window: 窗口对象
            
        Returns:
            是否设置成功
        """
        icon = IconManager.load_icon()
        if icon:
            try:
                window.setWindowIcon(icon)
                return True
            except Exception as e:
                print(f"设置窗口图标失败: {e}")
        
        return False
