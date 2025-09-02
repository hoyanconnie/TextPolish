#!/usr/bin/env python3
"""
TextPolish - Gemini文本格式修复工具
用于处理Gemini AI回答文本复制到Word后的格式混乱问题
"""

import sys
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal, QMimeData
from PyQt6.QtGui import QFont
from qfluentwidgets import (
    FluentWindow, NavigationItemPosition, SubtitleLabel, BodyLabel,
    PlainTextEdit, PrimaryPushButton, PushButton, TransparentPushButton,
    InfoBar, InfoBarPosition, Theme, setTheme, CardWidget, setFont,
    FluentIcon as FIF, MessageBox, Action, RoundMenu, TransparentToolButton,
    isDarkTheme, qconfig, TogglePushButton, CheckBox
)
import pyperclip
from bs4 import BeautifulSoup


class TextPolishInterface(QWidget):
    """主界面组件"""
    
    # 定义状态更新信号
    status_updated = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TextPolishInterface")
        self.initUI()
    
    def initUI(self):
        """初始化用户界面"""
        # 创建主布局 - 直接使用水平分割器占满整个窗口
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(1)  # 设置分割器手柄宽度为1像素
        # 设置分割器样式，适应亮暗主题
        self.update_splitter_style(splitter)
        main_layout.addWidget(splitter)
        
        # 左侧输入区域 - 占满
        input_card = self.create_input_card()
        splitter.addWidget(input_card)
        
        # 中间按钮区域
        button_widget = self.create_button_widget()
        splitter.addWidget(button_widget)
        
        # 右侧输出区域 - 占满
        output_card = self.create_output_card()
        splitter.addWidget(output_card)
        
        # 设置分割器比例：左侧40%，中间20%，右侧40%
        splitter.setSizes([400, 200, 400])
        splitter.setChildrenCollapsible(False)  # 防止面板被完全折叠
        
        # 保存分割器引用，用于主题切换时更新样式
        self.splitter = splitter
    
    def update_splitter_style(self, splitter):
        """更新分割器样式以适应当前主题"""
        if isDarkTheme():
            # 暗色主题：使用较亮的分割线
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
            # 亮色主题：使用较暗但很淡的分割线
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
        
        # 简化标题
        title = BodyLabel("原始文本")
        setFont(title, 10)
        layout.addWidget(title)
        
        # 输入文本框 - 占满剩余空间
        self.input_text = PlainTextEdit()
        self.input_text.setPlaceholderText("请在此粘贴Gemini AI的回答文本...")
        layout.addWidget(self.input_text, 1)  # 设置拉伸因子为1，占满剩余空间
        
        return card
    
    def create_output_card(self):
        """创建输出区域卡片"""
        card = CardWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # 简化标题
        title = BodyLabel("处理结果")
        setFont(title, 10)
        layout.addWidget(title)
        
        # 输出文本框 - 占满剩余空间
        self.output_text = PlainTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("处理后的文本将显示在这里...")
        layout.addWidget(self.output_text, 1)  # 设置拉伸因子为1，占满剩余空间
        
        return card
    
    def create_button_widget(self):
        """创建按钮区域"""
        widget = QWidget()
        widget.setFixedWidth(140)  # 固定宽度
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(20)
        
        # 添加顶部弹簧，使按钮垂直居中
        layout.addStretch(1)
        
        # 处理按钮
        self.process_btn = PrimaryPushButton(FIF.PLAY_SOLID, "处理文本")
        self.process_btn.setFixedSize(120, 45)
        self.process_btn.clicked.connect(self.process_text)
        layout.addWidget(self.process_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 清空按钮
        self.clear_btn = TransparentPushButton(FIF.DELETE, "清空所有")
        self.clear_btn.setFixedSize(120, 40)
        self.clear_btn.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 复制结果按钮
        self.copy_btn = PushButton(FIF.COPY, "文本复制")
        self.copy_btn.setFixedSize(120, 40)
        self.copy_btn.clicked.connect(self.copy_result)
        layout.addWidget(self.copy_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 带格式复制按钮
        self.copy_formatted_btn = PushButton(FIF.EDIT, "格式复制")
        self.copy_formatted_btn.setFixedSize(120, 40)
        self.copy_formatted_btn.clicked.connect(self.copy_formatted_result)
        layout.addWidget(self.copy_formatted_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 添加标题级别选择
        layout.addSpacing(10)
        
        # 标题级别选择标签
        level_label = BodyLabel("标题级别:")
        setFont(level_label, 9)
        layout.addWidget(level_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 一级标题选择框
        self.h1_checkbox = CheckBox("一级标题")
        self.h1_checkbox.setChecked(True)  # 默认选中
        layout.addWidget(self.h1_checkbox, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 二级标题选择框
        self.h2_checkbox = CheckBox("二级标题")
        self.h2_checkbox.setChecked(True)  # 默认选中
        layout.addWidget(self.h2_checkbox, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 三级标题选择框
        self.h3_checkbox = CheckBox("三级标题")
        self.h3_checkbox.setChecked(True)  # 默认选中
        layout.addWidget(self.h3_checkbox, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 添加分隔线
        layout.addSpacing(20)
        
        # 主题切换按钮
        self.theme_btn = self.create_theme_button()
        layout.addWidget(self.theme_btn, 0, Qt.AlignmentFlag.AlignCenter)
        
        # 添加底部弹簧，使按钮垂直居中
        layout.addStretch(1)
        
        return widget
    
    def create_theme_button(self):
        """创建主题切换按钮"""
        # 使用透明按钮显示当前主题图标
        icon_text = "🌙" if isDarkTheme() else "☀️"
        btn = TransparentPushButton(icon_text)
        btn.setFixedSize(120, 40)
        btn.clicked.connect(self.toggle_theme)
        btn.setToolTip("切换亮暗主题")
        
        return btn
    
    def toggle_theme(self):
        """切换亮暗主题"""
        # 根据当前主题切换
        if isDarkTheme():
            setTheme(Theme.LIGHT)
            self.theme_btn.setText("☀️")
            theme_name = "浅色主题"
        else:
            setTheme(Theme.DARK) 
            self.theme_btn.setText("🌙")
            theme_name = "深色主题"
        
        # 更新分割器样式以适应新主题
        self.update_splitter_style(self.splitter)
        
        # 显示主题切换提示
        InfoBar.success(
            title="主题已切换",
            content=f"已切换到{theme_name}",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=1000,
            parent=self
        )
    
    def clean_text(self, text):
        """
        清理文本格式问题
        """
        if not text.strip():
            return text
        
        # 删除特殊符号
        # 删除项目符号·
        text = re.sub(r'·\s*', '', text)
        
        # 删除其他常见的特殊符号
        text = re.sub(r'[•▪▫◦‣⁃]\s*', '', text)  # 各种项目符号
        text = re.sub(r'[▲▼◆◇■□●○]\s*', '', text)  # 几何符号
        
        # 替换英文标点为中文标点
        punctuation_map = {
            ',': '，',
            ';': '；', 
            ':': '：',
            '!': '！',
            '?': '？',
            '(': '（',
            ')': '）',
            '[': '【',
            ']': '】',
        }
        
        # 智能替换：只替换中文上下文中的英文标点
        for en_punct, cn_punct in punctuation_map.items():
            # 检查标点前后是否有中文字符
            pattern = r'([\u4e00-\u9fff])\s*' + re.escape(en_punct) + r'\s*([\u4e00-\u9fff])'
            text = re.sub(pattern, r'\1' + cn_punct + r'\2', text)
            
            # 处理行首和行尾的标点
            pattern_start = r'^' + re.escape(en_punct) + r'\s*([\u4e00-\u9fff])'
            text = re.sub(pattern_start, cn_punct + r'\1', text, flags=re.MULTILINE)
            
            pattern_end = r'([\u4e00-\u9fff])\s*' + re.escape(en_punct) + r'$'
            text = re.sub(pattern_end, r'\1' + cn_punct, text, flags=re.MULTILINE)
        
        # 处理引号的特殊情况
        # 将连续的英文双引号替换为中文引号
        text = re.sub(r'"([^"]*)"', r'"\1"', text)
        # 单引号替换
        text = re.sub(r"'([^']*)'", r"'\1'", text)
        
        # 暴力删除所有空格（针对中文文本优化）
        text = re.sub(r' +', '', text)  # 删除所有空格
        text = re.sub(r'\t+', '', text)  # 删除所有制表符
        
        # 清理行首行尾空白
        text = re.sub(r'[ \t]+\n', '\n', text)  # 行尾空格
        text = re.sub(r'\n[ \t]+', '\n', text)  # 行首空格
        
        # 删除段落之间的多余换行
        # 将多个连续换行替换为单个换行
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # 多个连续换行替换为两个
        # 进一步优化：将双换行替换为单换行（如果需要更紧凑的格式）
        text = re.sub(r'\n\n+', '\n', text)  # 所有多个换行都替换为单个换行
        
        # 清理段落间距
        text = text.strip()
        
        return text
    
    def convert_to_html(self, text, enable_h1=True, enable_h2=True, enable_h3=True):
        """
        将文本转换为HTML格式，根据标题规则识别标题层级
        """
        if not text.strip():
            return ""
        
        lines = text.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 根据要求识别标题，但要检查用户选择
            # 1. 一级标题：第一章、第二章等到换行符为止，或者"前言" (方正小标宋_GBK，小二号字，居中)
            if (re.match(r'^第[一二三四五六七八九十\d]+章', line) or line.strip() == '前言') and enable_h1:
                html_lines.append(f'<h1><span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-fareast-font-family:方正小标宋_GBK;font-size:18.0000pt;mso-font-kerning:22.0000pt;">{line}</span></h1>')
            # 2. 二级标题：第一节、第二节等到换行符为止 或者 一、二、到换行符为止 (方正黑体_GBK，三号字，居中)
            elif (re.match(r'^第[一二三四五六七八九十\d]+节', line) or re.match(r'^[一二三四五六七八九十]+、', line)) and enable_h2:
                html_lines.append(f'<h2><span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-fareast-font-family:方正黑体_GBK;font-size:16.0000pt;mso-font-kerning:1.0000pt;">{line}</span></h2>')
            # 3. 三级标题：（一）、（二）等格式 (方正楷体_GBK，三号加粗，两端对齐)
            elif re.match(r'^（[一二三四五六七八九十\d]+）', line) and enable_h3:
                html_lines.append(f'<h3><span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-fareast-font-family:方正楷体_GBK;font-size:16.0000pt;font-weight:bold;mso-font-kerning:1.0000pt;">{line}</span></h3>')
            else:
                # 检查是否包含段落开始需要特殊格式的部分
                # 1. 第一句到句号为止
                first_sentence_match = re.match(r'^([一二三四五六七八九十\d]+[是的][^。]*。)(.*)', line)
                # 2. 段落开头到冒号为止
                colon_match = re.match(r'^([^：]*：)(.*)', line)
                
                if (first_sentence_match or colon_match) and enable_h3:
                    if first_sentence_match:
                        # 分离出第一句和剩余部分
                        special_part = first_sentence_match.group(1)
                        remaining_text = first_sentence_match.group(2).strip()
                    else:  # colon_match
                        # 分离出冒号前的部分和剩余部分
                        special_part = colon_match.group(1)
                        remaining_text = colon_match.group(2).strip()
                    
                    # 构建HTML：特殊部分用楷体加粗格式，剩余部分用正文格式
                    html_content = f'<p class="MsoNormal" style="text-align:justify;text-justify:inter-ideograph;">'
                    html_content += f'<b><span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-fareast-font-family:方正楷体_GBK;font-size:16.0000pt;font-weight:bold;mso-font-kerning:1.0000pt;">{special_part}</span></b>'
                    
                    if remaining_text:
                        html_content += f'<span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-ascii-font-family:\'Times New Roman\';mso-hansi-font-family:\'Times New Roman\';mso-bidi-font-family:\'Times New Roman\';mso-fareast-font-family:方正仿宋_GBK;font-size:16.0000pt;mso-font-kerning:1.0000pt;">{remaining_text}</span>'
                    
                    html_content += '</p>'
                    html_lines.append(html_content)
                else:
                    # 普通正文 (西文：Times New Roman，中文：方正仿宋_GBK，三号字，首行缩进2字符)
                    html_lines.append(f'<p class="MsoNormal"><span style="mso-spacerun:\'yes\';font-family:\'Times New Roman\';mso-ascii-font-family:\'Times New Roman\';mso-hansi-font-family:\'Times New Roman\';mso-bidi-font-family:\'Times New Roman\';mso-fareast-font-family:方正仿宋_GBK;font-size:16.0000pt;mso-font-kerning:1.0000pt;">{line}</span></p>')
        
        # 生成完整的HTML文档
        html_content = self.generate_complete_html('\n'.join(html_lines))
        return html_content
    
    def generate_complete_html(self, body_content):
        """
        生成完整的HTML文档结构，模仿WPS/Word的HTML格式
        """
        html_template = """<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="ProgId" content="Word.Document">
<meta name="Generator" content="Microsoft Word 14">
<title>处理后的文档</title>
<style>
@font-face {{
    font-family: "Times New Roman";
}}

@font-face {{
    font-family: "方正小标宋_GBK";
}}

@font-face {{
    font-family: "方正黑体_GBK";
}}

@font-face {{
    font-family: "方正楷体_GBK";
}}

@font-face {{
    font-family: "方正仿宋_GBK";
}}

p.MsoNormal {{
    mso-style-name: 正文;
    margin: 0pt;
    margin-bottom: .0001pt;
    text-indent: 36.0000pt;
    mso-char-indent-count: 2.0000;
    mso-pagination: none;
    text-align: justify;
    text-justify: inter-ideograph;
    font-family: 'Times New Roman';
    mso-fareast-font-family: 方正仿宋_GBK;
    font-size: 16.0000pt;
    mso-font-kerning: 1.0000pt;
    line-height: 100%;
}}

h1 {{
    mso-style-name: "标题 1";
    mso-style-next: 正文;
    mso-para-margin-top: 0pt;
    mso-para-margin-bottom: 0pt;
    page-break-after: avoid;
    mso-pagination: lines-together;
    text-align: center;
    mso-outline-level: 1;
    line-height: 100%;
    font-family: 'Times New Roman';
    mso-fareast-font-family: 方正小标宋_GBK;
    font-size: 18.0000pt;
    mso-font-kerning: 22.0000pt;
}}

h2 {{
    mso-style-name: "标题 2";
    mso-style-next: 正文;
    mso-para-margin-top: 0pt;
    mso-para-margin-bottom: 0pt;
    page-break-after: avoid;
    mso-pagination: lines-together;
    text-align: center;
    mso-outline-level: 2;
    line-height: 100%;
    font-family: 'Times New Roman';
    mso-fareast-font-family: 方正黑体_GBK;
    font-size: 16.0000pt;
    mso-font-kerning: 1.0000pt;
}}

h3 {{
    mso-style-name: "标题 3";
    mso-style-next: 正文;
    mso-para-margin-top: 0pt;
    mso-para-margin-bottom: 0pt;
    page-break-after: avoid;
    mso-pagination: lines-together;
    text-align: justify;
    text-justify: inter-ideograph;
    mso-outline-level: 3;
    line-height: 100%;
    font-family: 'Times New Roman';
    mso-fareast-font-family: 方正楷体_GBK;
    font-size: 16.0000pt;
    font-weight: bold;
    mso-font-kerning: 1.0000pt;
}}

.bold {{
    font-family: 'Times New Roman';
    mso-fareast-font-family: 楷体;
    font-weight: bold;
    font-size: 16.0000pt;
}}

@page {{
    mso-page-border-surround-header: no;
    mso-page-border-surround-footer: no;
}}

@page Section0 {{
}}

div.Section0 {{
    page: Section0;
}}
</style>
</head>
<body style="tab-interval:21pt;text-justify-trim:punctuation;">
<!--StartFragment-->
{body_content}
<!--EndFragment-->
</body>
</html>"""
        return html_template.format(body_content=body_content)
    
    def write_to_clipboard(self, html_content):
        """
        将HTML字符串和其对应的纯文本版本放入剪贴板
        """
        app = QApplication.instance()
        clipboard = app.clipboard()
        
        # 从HTML中提取纯文本，作为备用格式
        plain_text = BeautifulSoup(html_content, 'html.parser').get_text(separator='\n', strip=True)
        
        mime_data = QMimeData()
        # 关键：同时设置HTML格式和纯文本格式
        mime_data.setHtml(html_content)
        mime_data.setText(plain_text)
        
        clipboard.setMimeData(mime_data)
    
    def process_text(self):
        """处理文本"""
        try:
            # 获取输入文本
            input_content = self.input_text.toPlainText().strip()
            
            if not input_content:
                InfoBar.warning(
                    title="提示",
                    content="请先输入要处理的文本！",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            self.status_updated.emit("正在处理...")
            QApplication.processEvents()
            
            # 处理文本
            cleaned_text = self.clean_text(input_content)
            
            # 显示结果
            self.output_text.setPlainText(cleaned_text)
            
            # 显示成功气泡
            InfoBar.success(
                title="处理完成",
                content=f"原始: {len(input_content)} 字符 → 处理后: {len(cleaned_text)} 字符",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            
            self.status_updated.emit("就绪")
            
        except Exception as e:
            InfoBar.error(
                title="处理失败",
                content=str(e),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            self.status_updated.emit("就绪")
    
    def clear_all(self):
        """清空所有文本"""
        self.input_text.clear()
        self.output_text.clear()
        InfoBar.info(
            title="已清空",
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
            result_text = self.output_text.toPlainText().strip()
            if not result_text:
                InfoBar.warning(
                    title="提示",
                    content="没有可复制的内容",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            pyperclip.copy(result_text)
            InfoBar.success(
                title="复制成功",
                content=f"已复制 {len(result_text)} 字符到剪贴板",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title="复制失败",
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
            result_text = self.output_text.toPlainText().strip()
            if not result_text:
                InfoBar.warning(
                    title="提示",
                    content="没有可复制的内容",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=1000,
                    parent=self
                )
                return
            
            # 获取用户选择的标题级别
            enable_h1 = self.h1_checkbox.isChecked()
            enable_h2 = self.h2_checkbox.isChecked()
            enable_h3 = self.h3_checkbox.isChecked()
            
            # 转换为HTML格式
            html_content = self.convert_to_html(result_text, enable_h1, enable_h2, enable_h3)
            
            # 复制到剪贴板（同时包含HTML和纯文本格式）
            self.write_to_clipboard(html_content)
            
            # 生成提示信息
            selected_levels = []
            if enable_h1:
                selected_levels.append("一级标题")
            if enable_h2:
                selected_levels.append("二级标题")
            if enable_h3:
                selected_levels.append("三级标题")
            
            levels_text = "、".join(selected_levels) if selected_levels else "无格式"
            
            InfoBar.success(
                title="格式化复制成功",
                content=f"已应用{levels_text}格式，可直接粘贴到WPS/Word等软件",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title="格式化复制失败",
                content=str(e),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )


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
        self.setWindowTitle("TextPolish - Gemini文本格式修复工具")
        self.resize(1200, 700)  # 增加窗口大小以适应新布局
        
        # 居中显示
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = screen.width(), screen.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        
        # 设置当前界面
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
        
        # 连接界面的状态更新信号到窗口标题
        self.homeInterface.status_updated.connect(self.update_status)
        
        # 初始状态
        self.base_title = "TextPolish - Gemini文本格式修复工具"
        
    def update_status(self, message):
        """更新状态显示"""
        # 只在处理过程中显示状态，其他时候保持原标题
        if message == "正在处理...":
            self.setWindowTitle(f"{self.base_title} - {message}")
        else:
            self.setWindowTitle(self.base_title)


def main():
    """主函数"""
    try:
        # 创建应用实例
        app = QApplication(sys.argv)
        
        # 设置应用信息
        app.setApplicationName("TextPolish")
        app.setApplicationVersion("1.0")
        app.setOrganizationName("TextPolish")
        
        # 设置主题
        setTheme(Theme.AUTO)
        
        # 创建主窗口
        window = TextPolishWindow()
        window.show()
        
        # 启动事件循环
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"程序启动失败: {e}")


if __name__ == "__main__":
    main()