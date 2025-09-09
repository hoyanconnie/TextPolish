#!/usr/bin/env python3
"""
主界面组件 - 包含文本处理的主要UI组件
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from qfluentwidgets import (
    BodyLabel, PlainTextEdit, PrimaryPushButton, PushButton, 
    TransparentPushButton, InfoBar, InfoBarPosition, Theme, setTheme, 
    CardWidget, setFont, FluentIcon as FIF, isDarkTheme, CheckBox, TextBrowser
)

from ..core.text_processor import TextProcessor
from ..core.html_generator import HTMLGenerator
from ..utils.clipboard import ClipboardManager
from ..config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT, 
    PRIMARY_BUTTON_HEIGHT, SPLITTER_SIZES, SPLITTER_HANDLE_WIDTH,
    FONTS, MESSAGES
)


class TextPolishInterface(QWidget):
    """主界面组件"""
    
    # 定义状态更新信号
    status_updated = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TextPolishInterface")
        
        # 初始化核心组件
        self.text_processor = TextProcessor()
        self.html_generator = HTMLGenerator()
        self.clipboard_manager = ClipboardManager()
        
        # 状态变量
        self.processed_text = ""
        self.config_interface = None  # 配置界面引用
        
        # 初始化UI
        self.initUI()
    
    def initUI(self):
        """初始化用户界面"""
        # 创建主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(SPLITTER_HANDLE_WIDTH)
        self.update_splitter_style(splitter)
        main_layout.addWidget(splitter)
        
        # 添加各个区域
        input_card = self.create_input_card()
        button_widget = self.create_button_widget()
        output_card = self.create_output_card()
        
        splitter.addWidget(input_card)
        splitter.addWidget(button_widget)
        splitter.addWidget(output_card)
        
        # 设置分割器比例
        splitter.setSizes(SPLITTER_SIZES)
        splitter.setChildrenCollapsible(False)
        
        # 保存分割器引用
        self.splitter = splitter
    
    def update_splitter_style(self, splitter):
        """更新分割器样式以适应当前主题"""
        if isDarkTheme():
            splitter.setStyleSheet("""
                QSplitter::handle {
                    background-color: transparent;
                    border: none;
                }
                QSplitter::handle:horizontal {
                    width: 1px;
                    background-color: rgba(255, 255, 255, 0.2);
                }
            """)
        else:
            splitter.setStyleSheet("""
                QSplitter::handle {
                    background-color: transparent;
                    border: none;
                }
                QSplitter::handle:horizontal {
                    width: 1px;
                    background-color: rgba(0, 0, 0, 0.05);
                }
            """)
    
    def create_input_card(self):
        """创建输入区域卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 标题
        title = BodyLabel("原始文本")
        setFont(title, FONTS['ui_label']['size'])
        layout.addWidget(title)
        
        # 输入文本框
        self.input_text = PlainTextEdit()
        self.input_text.setPlaceholderText("请在此粘贴Gemini AI的回答文本...")
        layout.addWidget(self.input_text, 1)
        
        return card
    
    def create_output_card(self):
        """创建输出区域卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 标题
        title = BodyLabel("格式预览")
        setFont(title, FONTS['ui_label']['size'])
        layout.addWidget(title)
        
        # HTML预览组件
        self.html_preview = TextBrowser()
        self.html_preview.setMarkdown(
            "## 📄 格式预览\n\n处理后的格式化文本将在这里预览...\n\n"
            "*支持标题层级、字体样式、段落格式等*"
        )
        
        # 设置预览字体
        font = QFont(FONTS['preview']['family'], FONTS['preview']['size'])
        self.html_preview.setFont(font)
        
        layout.addWidget(self.html_preview, 1)
        
        return card
    
    def create_button_widget(self):
        """创建按钮区域"""
        widget = QWidget()
        widget.setFixedWidth(140)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(20)
        
        # 添加顶部弹簧
        layout.addStretch(1)
        
        # 处理按钮
        self.process_btn = PrimaryPushButton(FIF.PLAY_SOLID, "处理文本")
        self.process_btn.setFixedSize(BUTTON_WIDTH, PRIMARY_BUTTON_HEIGHT)
        self.process_btn.clicked.connect(self.process_text)
        layout.addWidget(self.process_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 清空按钮
        self.clear_btn = TransparentPushButton(FIF.DELETE, "清空所有")
        self.clear_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 复制结果按钮
        self.copy_btn = PushButton(FIF.COPY, "文本复制")
        self.copy_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 带格式复制按钮
        self.copy_formatted_btn = PushButton(FIF.EDIT, "格式复制")
        self.copy_formatted_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.copy_formatted_btn.clicked.connect(self.copy_formatted_result)
        layout.addWidget(self.copy_formatted_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        
        # 添加底部弹簧
        layout.addStretch(1)
        
        return widget
    
    def set_config_interface(self, config_interface):
        """设置配置界面引用"""
        self.config_interface = config_interface
    
    def process_text(self):
        """处理文本"""
        try:
            # 获取输入文本
            input_content = self.input_text.toPlainText().strip()
            
            if not input_content:
                InfoBar.warning(
                    title="提示",
                    content=MESSAGES['warning']['no_input'],
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            self.status_updated.emit(MESSAGES['info']['processing'])
            QApplication.processEvents()
            
            # 处理文本
            cleaned_text = self.text_processor.clean_text(input_content)
            
            # 获取标题匹配设置
            if self.config_interface:
                settings = self.config_interface.get_title_matching_settings()
                enable_h1 = settings['enable_h1']
                enable_h2 = settings['enable_h2']
                enable_h3 = settings['enable_h3']
                enable_special = settings['enable_special']
            else:
                # 默认全部启用
                enable_h1 = enable_h2 = enable_h3 = enable_special = True
            
            # 生成HTML并显示预览
            body_content = self.html_generator.convert_to_html(cleaned_text, enable_h1, enable_h2, enable_h3, enable_special)
            preview_html = self.html_generator.generate_preview_html(
                body_content, isDarkTheme()
            )
            self.html_preview.setHtml(preview_html)
            
            # 保存处理后的纯文本
            self.processed_text = cleaned_text
            
            # 显示成功提示
            InfoBar.success(
                title=MESSAGES['success']['process_complete'],
                content=f"原始: {len(input_content)} 字符 → 处理后: {len(cleaned_text)} 字符",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            
            self.status_updated.emit(MESSAGES['info']['ready'])
            
        except Exception as e:
            InfoBar.error(
                title=MESSAGES['error']['process_failed'],
                content=str(e),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            self.status_updated.emit(MESSAGES['info']['ready'])
    
    def clear_all(self):
        """清空所有文本"""
        self.input_text.clear()
        self.html_preview.setMarkdown(
            "## 📄 格式预览\n\n处理后的格式化文本将在这里预览...\n\n"
            "*支持标题层级、字体样式、段落格式等*"
        )
        self.processed_text = ""
        
        InfoBar.info(
            title=MESSAGES['info']['cleared'],
            content="所有文本内容已清空",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
        self.input_text.setFocus()
    
    def copy_result(self):
        """复制处理结果到剪贴板"""
        try:
            if not self.processed_text:
                InfoBar.warning(
                    title="提示",
                    content=MESSAGES['warning']['no_content'],
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            self.clipboard_manager.copy_plain_text(self.processed_text)
            
            InfoBar.success(
                title=MESSAGES['success']['copy_success'],
                content=f"已复制 {len(self.processed_text)} 字符到剪贴板",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title=MESSAGES['error']['copy_failed'],
                content=str(e),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
    
    def copy_formatted_result(self):
        """带格式复制处理结果到剪贴板"""
        try:
            if not self.processed_text:
                InfoBar.warning(
                    title="提示",
                    content=MESSAGES['warning']['no_content'],
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            # 获取标题匹配设置
            if self.config_interface:
                settings = self.config_interface.get_title_matching_settings()
                enable_h1 = settings['enable_h1']
                enable_h2 = settings['enable_h2']
                enable_h3 = settings['enable_h3']
                enable_special = settings['enable_special']
            else:
                # 默认全部启用
                enable_h1 = enable_h2 = enable_h3 = enable_special = True
            
            # 转换为WPS格式HTML
            body_content = self.html_generator.convert_to_html(
                self.processed_text, enable_h1, enable_h2, enable_h3, enable_special
            )
            html_content = self.html_generator.generate_wps_html(body_content)
            
            # 复制到剪贴板
            self.clipboard_manager.copy_rich_text(html_content)
            
            # 生成提示信息
            selected_levels = []
            if enable_h1:
                selected_levels.append("一级标题")
            if enable_h2:
                selected_levels.append("二级标题")
            if enable_h3:
                selected_levels.append("三级标题")
            if enable_special:
                selected_levels.append("特殊格式")
            
            levels_text = "、".join(selected_levels) if selected_levels else "无格式"
            
            InfoBar.success(
                title=MESSAGES['success']['copy_success'],
                content=f"已应用{levels_text}格式，可直接粘贴到WPS/Word等软件",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title=MESSAGES['error']['formatted_copy_failed'],
                content=str(e),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
    
    def update_preview_theme(self):
        """主题切换时更新预览"""
        if hasattr(self, 'processed_text') and self.processed_text:
            # 获取标题匹配设置
            if self.config_interface:
                settings = self.config_interface.get_title_matching_settings()
                enable_h1 = settings['enable_h1']
                enable_h2 = settings['enable_h2']
                enable_h3 = settings['enable_h3']
                enable_special = settings['enable_special']
            else:
                # 默认全部启用
                enable_h1 = enable_h2 = enable_h3 = enable_special = True
            
            # 重新生成预览HTML
            body_content = self.html_generator.convert_to_html(
                self.processed_text, enable_h1, enable_h2, enable_h3, enable_special
            )
            preview_html = self.html_generator.generate_preview_html(
                body_content, isDarkTheme()
            )
            self.html_preview.setHtml(preview_html)
