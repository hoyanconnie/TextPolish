#!/usr/bin/env python3
"""
剪贴板管理模块 - 负责处理剪贴板操作
"""

import pyperclip
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMimeData
from bs4 import BeautifulSoup


class ClipboardManager:
    """剪贴板管理器 - 负责处理各种剪贴板操作"""
    
    @staticmethod
    def copy_plain_text(text: str) -> None:
        """
        复制纯文本到剪贴板
        
        Args:
            text: 要复制的文本
        """
        pyperclip.copy(text)
    
    @staticmethod
    def copy_rich_text(html_content: str) -> None:
        """
        复制富文本（HTML）到剪贴板
        
        Args:
            html_content: HTML内容
        """
        app = QApplication.instance()
        if not app:
            raise RuntimeError("QApplication instance not found")
        
        clipboard = app.clipboard()
        
        # 从HTML中提取纯文本，作为备用格式
        plain_text = BeautifulSoup(html_content, 'html.parser').get_text(
            separator='\n', strip=True
        )
        
        mime_data = QMimeData()
        # 关键：同时设置HTML格式和纯文本格式
        mime_data.setHtml(html_content)
        mime_data.setText(plain_text)
        
        clipboard.setMimeData(mime_data)
    
    @staticmethod
    def get_plain_text() -> str:
        """
        从剪贴板获取纯文本
        
        Returns:
            剪贴板中的纯文本
        """
        return pyperclip.paste()
    
    @staticmethod
    def get_html_text() -> str:
        """
        从剪贴板获取HTML文本
        
        Returns:
            剪贴板中的HTML文本
        """
        app = QApplication.instance()
        if not app:
            return ""
        
        clipboard = app.clipboard()
        mime_data = clipboard.mimeData()
        
        if mime_data.hasHtml():
            return mime_data.html()
        
        return ""
