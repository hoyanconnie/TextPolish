#!/usr/bin/env python3
"""
配置界面页面 - 按标题级别组织的简洁配置界面
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, 
    QGroupBox, QFrame, QLabel, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from qfluentwidgets import (
    ScrollArea, PrimaryPushButton, PushButton, TransparentPushButton,
    LineEdit, ComboBox, BodyLabel, StrongBodyLabel, TitleLabel, 
    CardWidget, CheckBox, TextEdit, FluentIcon as FIF, InfoBar, 
    InfoBarPosition, MessageBox, SubtitleLabel, CaptionLabel,
    Pivot, qconfig, setTheme, Theme, isDarkTheme, ExpandLayout,
    setCustomStyleSheet, HeaderCardWidget, IconWidget
)

from ..config import user_config_manager, StyleConfig, RegexPattern


class TitleLevelCard(CardWidget):
    """标题级别配置卡片 - 包含样式和匹配规则"""
    
    config_changed = pyqtSignal(str)  # level
    
    def __init__(self, level: str, title: str, parent=None):
        super().__init__(parent)
        self.level = level
        self.title = title
        self.config = user_config_manager.get_config(level)
        self.rule_widgets = []
        
        self.setup_ui()
        self.load_config()
        self.apply_card_style()
    
    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # 增加内边距
        layout.setSpacing(20)  # 增加组件间距
        
        # 标题 - 使用 HeaderCardWidget 替代
        # 根据级别选择不同图标
        icon_map = {
            'h1': FIF.LABEL,
            'h2': FIF.TAG,  
            'h3': FIF.BOOK_SHELF,
            'normal': FIF.DOCUMENT,
            'special_format': FIF.PALETTE
        }
        
        # 使用 HeaderCardWidget 作为标题容器
        title_header = HeaderCardWidget(self)
        title_header.setTitle(self.title)
        
        # 创建图标和描述
        icon_widget = IconWidget(icon_map.get(self.level, FIF.SETTING), self)
        icon_widget.setFixedSize(16, 16)
        
        description_label = BodyLabel(f"{self.title} 的样式和匹配规则配置", self)
        
        # 创建图标和描述的布局
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)
        header_layout.addWidget(icon_widget)
        header_layout.addWidget(description_label)
        header_layout.addStretch()
        
        title_header.viewLayout.addLayout(header_layout)
        layout.addWidget(title_header)
        
        # 样式配置区域
        style_group = self.create_style_section()
        layout.addWidget(style_group)
        
        # 匹配规则区域（只对h1、h2、h3、special_format显示）
        if self.level in ['h1', 'h2', 'h3', 'special_format']:
            rules_group = self.create_rules_section()
            layout.addWidget(rules_group)
        
    
    def create_style_section(self):
        """创建样式配置区域"""
        group = HeaderCardWidget(self)
        group.setTitle("📝 样式设置")
        
        # 使用网格布局来更好地组织控件
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(16, 16, 16, 16)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(16)
        
        # 第一行：字体设置
        grid_layout.addWidget(BodyLabel("字体:"), 0, 0)
        self.font_family_edit = LineEdit()
        self.font_family_edit.setPlaceholderText("如：方正仿宋_GBK")
        self.font_family_edit.setMinimumWidth(200)
        grid_layout.addWidget(self.font_family_edit, 0, 1)
        
        grid_layout.addWidget(BodyLabel("字号:"), 0, 2)
        self.font_size_edit = LineEdit()
        self.font_size_edit.setPlaceholderText("如：16.0000pt")
        self.font_size_edit.setMinimumWidth(120)
        grid_layout.addWidget(self.font_size_edit, 0, 3)
        
        # 第二行：样式设置
        grid_layout.addWidget(BodyLabel("粗细:"), 1, 0)
        self.font_weight_combo = ComboBox()
        self.font_weight_combo.addItems(["normal", "bold"])
        self.font_weight_combo.setMinimumWidth(120)
        grid_layout.addWidget(self.font_weight_combo, 1, 1)
        
        grid_layout.addWidget(BodyLabel("对齐:"), 1, 2)
        self.alignment_combo = ComboBox()
        self.alignment_combo.addItems(["left", "center", "right", "justify"])
        self.alignment_combo.setMinimumWidth(120)
        grid_layout.addWidget(self.alignment_combo, 1, 3)
        
        # 第三行：首行缩进（仅对正文显示）
        if self.level == 'normal':
            grid_layout.addWidget(BodyLabel("首行缩进:"), 2, 0)
            self.text_indent_edit = LineEdit()
            self.text_indent_edit.setPlaceholderText("如：36.0000pt")
            self.text_indent_edit.setMinimumWidth(120)
            grid_layout.addWidget(self.text_indent_edit, 2, 1)
        
        # 设置列拉伸
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)
        
        group.viewLayout.addWidget(grid_widget)
        
        return group
    
    def create_rules_section(self):
        """创建匹配规则区域"""
        group = HeaderCardWidget(self)
        group.setTitle("🎯 匹配规则")
        
        # 添加规则按钮和说明
        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)
        
        # 说明文本
        desc_label = CaptionLabel("配置用于识别此类型文本的正则表达式规则")
        desc_label.setStyleSheet("color: #666666;")
        header_layout.addWidget(desc_label)
        header_layout.addStretch()
        
        self.add_rule_button = PrimaryPushButton("添加规则")
        self.add_rule_button.setIcon(FIF.ADD)
        self.add_rule_button.setFixedSize(120, 32)  # 增加宽度以适应中文文字
        self.add_rule_button.clicked.connect(self.add_rule)
        header_layout.addWidget(self.add_rule_button)
        
        group.viewLayout.addWidget(header_container)
        
        # 规则列表容器
        self.rules_container = QWidget()
        self.rules_layout = QVBoxLayout(self.rules_container)
        self.rules_layout.setContentsMargins(0, 12, 0, 0)
        self.rules_layout.setSpacing(12)  # 增加规则之间的间距
        
        group.viewLayout.addWidget(self.rules_container)
        
        return group
    
    def create_rule_widget(self, pattern: RegexPattern):
        """创建单个规则组件"""
        rule_widget = CardWidget()  # 使用CardWidget增强视觉效果
        rule_widget.setBorderRadius(8)
        rule_widget.setFixedHeight(80)  # 增加高度以适应新布局
        
        layout = QVBoxLayout(rule_widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # 第一行：复选框和规则名称
        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(12)
        
        # 启用复选框
        enabled_checkbox = CheckBox()
        enabled_checkbox.setChecked(pattern.enabled)
        top_layout.addWidget(enabled_checkbox)
        
        # 规则名称
        name_edit = LineEdit()
        name_edit.setText(pattern.name)
        name_edit.setPlaceholderText("规则名称")
        name_edit.setFixedWidth(150)
        top_layout.addWidget(name_edit)
        
        top_layout.addStretch()
        
        # 删除按钮
        remove_button = TransparentPushButton("删除")
        remove_button.setIcon(FIF.DELETE)
        remove_button.setFixedSize(80, 28)  # 增加宽度以适应中文文字
        remove_button.setToolTip("删除规则")
        self.update_remove_button_style(remove_button)
        top_layout.addWidget(remove_button)
        
        layout.addWidget(top_row)
        
        # 第二行：正则表达式
        pattern_edit = LineEdit()
        pattern_edit.setText(pattern.pattern)
        pattern_edit.setPlaceholderText("输入正则表达式，如：^第[一二三四五六七八九十]+章")
        layout.addWidget(pattern_edit)
        
        # 为规则组件添加样式
        self.apply_rule_widget_style(rule_widget)
        
        # 保存组件引用和数据
        rule_widget.pattern = pattern
        rule_widget.enabled_checkbox = enabled_checkbox
        rule_widget.name_edit = name_edit
        rule_widget.pattern_edit = pattern_edit
        rule_widget.remove_button = remove_button
        
        # 连接信号
        enabled_checkbox.stateChanged.connect(self.on_rule_changed)
        name_edit.textChanged.connect(self.on_rule_changed)
        pattern_edit.textChanged.connect(self.on_rule_changed)
        remove_button.clicked.connect(lambda: self.remove_rule(rule_widget))
        
        return rule_widget
    
    def update_remove_button_style(self, button):
        """更新删除按钮样式以适应当前主题"""
        # 浅色主题样式 - 更明显的红色按钮
        light_qss = """
            PushButton {
                color: #ffffff;
                background-color: #e74c3c;
                border: 1px solid #c0392b;
                border-radius: 4px;
                font-weight: bold;
            }
            PushButton:hover {
                background-color: #c0392b;
                border-color: #a93226;
            }
            PushButton:pressed {
                background-color: #a93226;
                border-color: #922b21;
            }
        """
        
        # 深色主题样式 - 更明显的红色按钮
        dark_qss = """
            PushButton {
                color: #ffffff;
                background-color: #ff6b6b;
                border: 1px solid #ff5252;
                border-radius: 4px;
                font-weight: bold;
            }
            PushButton:hover {
                background-color: #ff5252;
                border-color: #ff3333;
            }
            PushButton:pressed {
                background-color: #ff3333;
                border-color: #ff1111;
            }
        """
        
        # 使用 QFluentWidgets 推荐的方式设置主题自适应样式
        setCustomStyleSheet(button, light_qss, dark_qss)
    
    def apply_rule_widget_style(self, widget):
        """为规则组件应用样式"""
        # 浅色主题样式
        light_qss = """
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
            }
            QWidget:hover {
                border-color: #ced4da;
                background-color: #f1f3f4;
            }
        """
        
        # 深色主题样式
        dark_qss = """
            QWidget {
                background-color: #3c4043;
                border: 1px solid #5f6368;
                border-radius: 6px;
            }
            QWidget:hover {
                border-color: #8ab4f8;
                background-color: #484a4d;
            }
        """
        
        setCustomStyleSheet(widget, light_qss, dark_qss)
    
    def update_group_box_style(self, group_box):
        """更新群组框样式以适应当前主题"""
        # 浅色主题样式
        light_qss = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                color: #333333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px 0 4px;
                color: #333333;
            }
        """
        
        # 深色主题样式
        dark_qss = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(200, 200, 200, 0.3);
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
        """
        
        # 使用 QFluentWidgets 推荐的方式设置主题自适应样式
        setCustomStyleSheet(group_box, light_qss, dark_qss)
    
    def apply_card_style(self):
        """为卡片应用美化样式"""
        light_qss = """
            TitleLevelCard {
                border: 1px solid rgba(0, 0, 0, 0.08);
                border-radius: 12px;
                background-color: #ffffff;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }
            TitleLevelCard:hover {
                border-color: rgba(0, 120, 215, 0.3);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
        """
        
        dark_qss = """
            TitleLevelCard {
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                background-color: #2d3748;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            }
            TitleLevelCard:hover {
                border-color: rgba(100, 200, 255, 0.4);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            }
        """
        
        setCustomStyleSheet(self, light_qss, dark_qss)
    
    def apply_title_label_style(self, label):
        """为标题标签应用样式"""
        light_qss = """
            SubtitleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0px;
            }
        """
        
        dark_qss = """
            SubtitleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ecf0f1;
                padding: 5px 0px;
            }
        """
        
        setCustomStyleSheet(label, light_qss, dark_qss)
    
    def load_config(self):
        """加载配置"""
        if not self.config:
            return
        
        # 加载样式配置
        style = self.config.style
        self.font_family_edit.setText(style.font_family)
        self.font_size_edit.setText(style.font_size)
        
        # 设置粗细
        weight_index = self.font_weight_combo.findText(style.font_weight)
        if weight_index >= 0:
            self.font_weight_combo.setCurrentIndex(weight_index)
        
        # 设置对齐方式
        alignment_index = self.alignment_combo.findText(style.alignment)
        if alignment_index >= 0:
            self.alignment_combo.setCurrentIndex(alignment_index)
        
        # 设置首行缩进（仅正文）
        if self.level == 'normal' and hasattr(self, 'text_indent_edit'):
            self.text_indent_edit.setText(style.text_indent)
        
        # 加载匹配规则
        if self.level in ['h1', 'h2', 'h3', 'special_format']:
            self.load_rules()
    
    def load_rules(self):
        """加载匹配规则"""
        # 清除现有规则
        self.clear_rules()
        
        # 添加配置中的规则
        for pattern in self.config.patterns:
            rule_widget = self.create_rule_widget(pattern)
            self.rule_widgets.append(rule_widget)
            self.rules_layout.addWidget(rule_widget)
        
    
    def clear_rules(self):
        """清除所有规则组件"""
        for widget in self.rule_widgets:
            widget.deleteLater()
        self.rule_widgets.clear()
    
    def add_rule(self):
        """添加新规则"""
        new_pattern = RegexPattern(
            pattern="",
            name=f"新规则{len(self.rule_widgets) + 1}",
            enabled=True,
            description=""
        )
        
        rule_widget = self.create_rule_widget(new_pattern)
        self.rule_widgets.append(rule_widget)
        self.rules_layout.addWidget(rule_widget)
    
    def remove_rule(self, rule_widget):
        """删除规则并保存配置"""
        if rule_widget in self.rule_widgets:
            self.rule_widgets.remove(rule_widget)
            rule_widget.deleteLater()
            
            # 删除规则后立即保存配置
            try:
                self.save_config_silent()
                print(f"规则已删除并保存，剩余规则数量: {len(self.rule_widgets)}")
            except Exception as e:
                print(f"删除规则后保存配置失败: {e}")
    
    def on_rule_changed(self):
        """规则改变时更新数据并自动保存"""
        for widget in self.rule_widgets:
            widget.pattern.enabled = widget.enabled_checkbox.isChecked()
            widget.pattern.name = widget.name_edit.text().strip()
            widget.pattern.pattern = widget.pattern_edit.text().strip()
        
        # 实时保存配置变化
        try:
            self.save_config_silent()
        except Exception as e:
            print(f"自动保存配置失败: {e}")
    
    def save_config_silent(self):
        """静默保存配置（不显示提示）"""
        try:
            # 保存样式配置
            style = StyleConfig(
                font_family=self.font_family_edit.text().strip(),
                font_size=self.font_size_edit.text().strip(),
                font_kerning="1.0000pt",  # 固定值
                font_weight=self.font_weight_combo.currentText(),
                alignment=self.alignment_combo.currentText(),
                text_indent=getattr(self, 'text_indent_edit', None) and self.text_indent_edit.text().strip() or "0.0000pt",
                description=""
            )
            
            # 收集匹配规则
            patterns = None
            if self.level in ['h1', 'h2', 'h3', 'special_format']:
                patterns = []
                for widget in self.rule_widgets:
                    if widget.pattern.pattern.strip():  # 只保存非空的模式
                        patterns.append(widget.pattern)
            
            # 批量更新配置（避免重复保存）
            user_config_manager.update_level_config(self.level, style, patterns)
            
            self.config_changed.emit(self.level)
            
        except Exception as e:
            raise e


class ConfigInterface(QWidget):
    """配置界面主页面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ConfigInterface")
        self.setup_ui()
        self.apply_theme_background()
    
    def setup_ui(self):
        """设置主界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(0)  # 使用0间距，让滚动区域完全填充
        
        # 添加页面标题
        page_title = TitleLabel("文档格式配置")
        page_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_page_title_style(page_title)
        layout.addWidget(page_title)
        layout.addSpacing(24)  # 标题下方间距
        
        # 创建滚动区域
        self.scroll = ScrollArea()
        self.scroll_content = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_layout.setContentsMargins(16, 16, 16, 16)  # 滚动内容内边距
        scroll_layout.setSpacing(24)  # 卡片间距
        
        # 1. 应用设置
        self.app_settings_card = self.create_app_settings_section()
        scroll_layout.addWidget(self.app_settings_card)
        
        # 2. 一级标题设置
        self.h1_card = self.create_title_settings_section("h1", "一级标题", FIF.LABEL)
        scroll_layout.addWidget(self.h1_card)
        
        # 3. 二级标题设置
        self.h2_card = self.create_title_settings_section("h2", "二级标题", FIF.TAG)
        scroll_layout.addWidget(self.h2_card)
        
        # 4. 三级标题设置
        self.h3_card = self.create_title_settings_section("h3", "三级标题", FIF.BOOK_SHELF)
        scroll_layout.addWidget(self.h3_card)
        
        # 5. 正文设置
        self.normal_card = self.create_text_settings_section("normal", "正文", FIF.DOCUMENT)
        scroll_layout.addWidget(self.normal_card)
        
        # 6. 特殊格式设置
        self.special_card = self.create_title_settings_section("special_format", "特殊格式", FIF.PALETTE)
        scroll_layout.addWidget(self.special_card)
        
        # 保存配置引用以便后续操作
        self.config_cards = {
            'h1': self.h1_card,
            'h2': self.h2_card,
            'h3': self.h3_card,
            'normal': self.normal_card,
            'special_format': self.special_card
        }
        
        # 设置滚动区域
        self.scroll.setWidget(self.scroll_content)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)
        
        # 应用滚动区域的特殊样式
        self.apply_scroll_area_style()
        
        # 底部保存按钮
        layout.addSpacing(16)
        self.setup_save_button(layout)
        
        # 加载界面设置
        self.load_ui_settings()
        
    def apply_page_title_style(self, label):
        """为页面标题应用样式"""
        light_qss = """
            TitleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #1f2937;
                padding: 16px 0px;
                margin: 0px;
            }
        """
        
        dark_qss = """
            TitleLabel {
                font-size: 28px;
                font-weight: bold;
                color: #f9fafb;
                padding: 16px 0px;
                margin: 0px;
            }
        """
        
        setCustomStyleSheet(label, light_qss, dark_qss)
    
    def create_app_settings_section(self):
        """创建应用设置区域"""
        card = CardWidget()
        card.setBorderRadius(12)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # 标题区域
        title_container = QWidget()
        title_layout = QHBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(12)
        
        settings_icon = IconWidget(FIF.SETTING, card)
        settings_icon.setFixedSize(24, 24)
        title_layout.addWidget(settings_icon)
        
        title_label = SubtitleLabel("应用设置")
        self.apply_title_label_style(title_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addWidget(title_container)
        
        # 标题级别开关
        title_group = HeaderCardWidget()
        title_group.setTitle("标题级别设置")
        
        level_label = BodyLabel("启用的标题级别:")
        title_group.viewLayout.addWidget(level_label)
        
        checkbox_container = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_container)
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setSpacing(20)
        
        self.h1_checkbox = CheckBox("一级标题")
        self.h1_checkbox.setChecked(True)
        self.h1_checkbox.stateChanged.connect(self.on_title_level_changed)
        checkbox_layout.addWidget(self.h1_checkbox)
        
        self.h2_checkbox = CheckBox("二级标题") 
        self.h2_checkbox.setChecked(True)
        self.h2_checkbox.stateChanged.connect(self.on_title_level_changed)
        checkbox_layout.addWidget(self.h2_checkbox)
        
        self.h3_checkbox = CheckBox("三级标题") 
        self.h3_checkbox.setChecked(True)
        self.h3_checkbox.stateChanged.connect(self.on_title_level_changed)
        checkbox_layout.addWidget(self.h3_checkbox)
        
        self.special_checkbox = CheckBox("特殊格式") 
        self.special_checkbox.setChecked(True)
        self.special_checkbox.stateChanged.connect(self.on_title_level_changed)
        checkbox_layout.addWidget(self.special_checkbox)
        
        checkbox_layout.addStretch()
        title_group.viewLayout.addWidget(checkbox_container)
        
        layout.addWidget(title_group)
        
        # 主题设置
        ui_group = HeaderCardWidget()
        ui_group.setTitle("界面设置")
        
        theme_container = QWidget()
        theme_layout = QHBoxLayout(theme_container)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(12)
        
        theme_layout.addWidget(BodyLabel("主题:"))
        self.theme_combo = ComboBox()
        self.theme_combo.addItems(["自动", "浅色", "深色"])
        self.theme_combo.setCurrentIndex(0)
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        
        ui_group.viewLayout.addWidget(theme_container)
        layout.addWidget(ui_group)
        
        return card
    
    def update_group_box_style(self, group_box):
        """更新群组框样式以适应当前主题"""
        # 浅色主题样式
        light_qss = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                color: #333333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px 0 4px;
                color: #333333;
            }
        """
        
        # 深色主题样式
        dark_qss = """
            QGroupBox {
                font-weight: bold;
                border: 1px solid rgba(200, 200, 200, 0.3);
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 4px 0 4px;
                color: #ffffff;
            }
        """
        
        # 使用 QFluentWidgets 推荐的方式设置主题自适应样式
        setCustomStyleSheet(group_box, light_qss, dark_qss)
    
    def apply_theme_background(self):
        """为配置界面应用主题背景"""
        # 主界面背景样式 - 使用渐变背景
        main_light_qss = """
            ConfigInterface {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc, stop:1 #f1f5f9);
                color: #1e293b;
            }
        """
        
        main_dark_qss = """
            ConfigInterface {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0f172a, stop:1 #1e293b);
                color: #f8fafc;
            }
        """
        
        # 应用主界面样式
        setCustomStyleSheet(self, main_light_qss, main_dark_qss)
    
    
    def apply_title_label_style(self, label):
        """为标题标签应用样式"""
        light_qss = """
            SubtitleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 5px 0px;
            }
        """
        
        dark_qss = """
            SubtitleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #ecf0f1;
                padding: 5px 0px;
            }
        """
        
        setCustomStyleSheet(label, light_qss, dark_qss)
    
    def apply_scroll_area_style(self):
        """为滚动区域应用特殊样式"""
        # 美化滚动区域样式
        light_qss = """
            QScrollArea {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: rgba(0, 0, 0, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(0, 0, 0, 0.3);
            }
        """
        
        dark_qss = """
            QScrollArea {
                background: transparent;
                border: none;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """
        
        setCustomStyleSheet(self.scroll, light_qss, dark_qss)
        # 内容区域保持透明背景
        self.scroll_content.setStyleSheet("QWidget{background: transparent}")
    
    def setup_save_button(self, layout):
        """设置保存按钮"""
        # 创建底部操作区域
        bottom_container = CardWidget()
        bottom_container.setBorderRadius(12)
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(24, 16, 24, 16)
        bottom_layout.setSpacing(12)
        
        # 配置文件路径信息
        from ..config import user_config_manager
        config_path = user_config_manager.get_config_file_path()
        path_label = CaptionLabel(f"📁 配置文件路径: {config_path}")
        path_label.setStyleSheet("color: #888888; font-size: 10px;")
        path_label.setWordWrap(True)
        bottom_layout.addWidget(path_label)
        
        # 按钮行
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(16)
        
        # 左侧提示信息
        tip_label = CaptionLabel("💡 配置修改后需要点击保存按钮才能生效")
        tip_label.setStyleSheet("color: #666666;")
        button_layout.addWidget(tip_label)
        
        button_layout.addStretch()
        
        # 导出配置按钮
        export_button = PushButton("导出配置")
        export_button.setIcon(FIF.UP)
        export_button.setFixedSize(120, 36)
        export_button.clicked.connect(self.export_config)
        button_layout.addWidget(export_button)
        
        # 导入配置按钮
        import_button = PushButton("导入配置")
        import_button.setIcon(FIF.DOWN)
        import_button.setFixedSize(120, 36)
        import_button.clicked.connect(self.import_config)
        button_layout.addWidget(import_button)
        
        # 保存按钮
        save_all_button = PrimaryPushButton("保存所有配置")
        save_all_button.setIcon(FIF.SAVE)
        save_all_button.setFixedSize(160, 36)  # 增加宽度确保文字完整显示
        save_all_button.clicked.connect(self.save_all_config)
        
        # 应用保存按钮特殊样式
        self.apply_save_button_style(save_all_button)
        button_layout.addWidget(save_all_button)
        
        bottom_layout.addWidget(button_container)
        layout.addWidget(bottom_container)
    
    def apply_save_button_style(self, button):
        """为保存按钮应用特殊样式"""
        light_qss = """
            PrimaryPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0078d4, stop:1 #106ebe);
                border: 1px solid #005a9e;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            PrimaryPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #106ebe, stop:1 #005a9e);
            }
            PrimaryPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #005a9e, stop:1 #004578);
            }
        """
        
        dark_qss = """
            PrimaryPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0066cc, stop:1 #004499);
                border: 1px solid #003366;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            PrimaryPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0080ff, stop:1 #0066cc);
            }
            PrimaryPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #004499, stop:1 #003366);
            }
        """
        
        setCustomStyleSheet(button, light_qss, dark_qss)
    
    def on_config_changed(self, level):
        """配置改变时的处理"""
        pass  # 目前不需要特殊处理
    
    def on_theme_changed(self, theme_text):
        """主题改变时的处理"""
        from qfluentwidgets import setTheme, Theme
        
        if theme_text == "浅色":
            setTheme(Theme.LIGHT)
        elif theme_text == "深色":
            setTheme(Theme.DARK)
        else:  # 自动
            setTheme(Theme.AUTO)
            
        InfoBar.success(
            title="主题已切换",
            content=f"已切换到{theme_text}主题",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
    
    def get_title_matching_settings(self):
        """获取标题匹配设置"""
        return {
            'enable_h1': self.h1_checkbox.isChecked(),
            'enable_h2': self.h2_checkbox.isChecked(),
            'enable_h3': self.h3_checkbox.isChecked(),
            'enable_special': self.special_checkbox.isChecked()
        }
    
    def on_title_level_changed(self):
        """标题级别设置改变时的处理"""
        try:
            # 获取当前设置
            settings = self.get_title_matching_settings()
            
            # 保存到配置管理器
            from ..config import user_config_manager
            user_config_manager.save_ui_settings(settings)
            
        except Exception as e:
            print(f"保存标题级别设置失败: {e}")
    
    def load_ui_settings(self):
        """加载界面设置"""
        try:
            from ..config import user_config_manager
            settings = user_config_manager.load_ui_settings()
            
            # 设置复选框状态
            self.h1_checkbox.setChecked(settings.get('enable_h1', True))
            self.h2_checkbox.setChecked(settings.get('enable_h2', True))
            self.h3_checkbox.setChecked(settings.get('enable_h3', True))
            self.special_checkbox.setChecked(settings.get('enable_special', True))
            
            print(f"界面设置已加载: {settings}")
            
        except Exception as e:
            print(f"加载界面设置失败: {e}")
    
    def save_all_config(self):
        """保存所有配置"""
        try:
            # 统计配置项
            total_rules = 0
            total_levels = 0
            
            for level, card in self.config_cards.items():
                # 触发每个卡片的保存
                if hasattr(card, 'save_config_silent'):
                    try:
                        card.save_config_silent()  # 静默保存，不显示单独的提示
                        total_levels += 1
                        
                        # 统计规则数量
                        if hasattr(card, 'rule_widgets'):
                            rule_count = len([w for w in card.rule_widgets if w.pattern.pattern.strip()])
                            total_rules += rule_count
                            print(f"已保存 {card.title}: 样式配置 + {rule_count} 个规则")
                        else:
                            print(f"已保存 {card.title}: 样式配置")
                            
                    except Exception as e:
                        print(f"保存 {level} 配置失败: {e}")
                        total_levels -= 1
            
            # 保存界面设置
            ui_settings = self.get_title_matching_settings()
            from ..config import user_config_manager
            user_config_manager.save_ui_settings(ui_settings)
            
            # 生成更有意义的提示信息
            if total_rules > 0:
                content = f"已保存 {total_levels} 个级别配置、{total_rules} 个正则规则、界面设置"
            else:
                content = f"已保存 {total_levels} 个级别配置和界面设置"
            
            InfoBar.success(
                title="保存成功",
                content=content,
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title="保存失败",
                content=f"保存配置时出错: {str(e)}",
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=3000,
                parent=self
            )
    
    def create_title_settings_section(self, level: str, title: str, icon):
        """创建标题设置区域（一级标题、二级标题、特殊格式）"""
        card = TitleLevelCard(level, title)
        card.config_changed.connect(self.on_config_changed)
        return card
    
    def create_text_settings_section(self, level: str, title: str, icon):
        """创建文本设置区域（正文）"""
        card = TitleLevelCard(level, title)
        card.config_changed.connect(self.on_config_changed)
        return card
    
    def export_config(self):
        """导出配置到文件"""
        from PyQt6.QtWidgets import QFileDialog
        from ..config import user_config_manager
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出配置文件",
            "textpolish_config.json",
            "JSON文件 (*.json)"
        )
        
        if file_path:
            success = user_config_manager.export_config_to_file(file_path)
            if success:
                InfoBar.success(
                    title="导出成功",
                    content=f"配置已导出到: {file_path}",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
            else:
                InfoBar.error(
                    title="导出失败",
                    content="导出配置文件时出错",
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=3000,
                    parent=self
                )
    
    def import_config(self):
        """从文件导入配置"""
        from PyQt6.QtWidgets import QFileDialog
        from ..config import user_config_manager
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入配置文件",
            "",
            "JSON文件 (*.json)"
        )
        
        if file_path:
            # 先确认是否要覆盖当前配置
            reply = MessageBox(
                "确认导入",
                "导入配置将覆盖当前所有设置，是否继续？",
                self
            )
            reply.yesButton.setText("确认导入")
            reply.cancelButton.setText("取消")
            
            if reply.exec():
                success = user_config_manager.import_config_from_file(file_path)
                if success:
                    InfoBar.success(
                        title="导入成功",
                        content="配置已成功导入，请重启应用使配置生效",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=4000,
                        parent=self
                    )
                    # 刷新配置界面
                    self.refresh_all_configs()
                else:
                    InfoBar.error(
                        title="导入失败",
                        content="导入配置文件时出错，请检查文件格式",
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=3000,
                        parent=self
                    )
    
    def refresh_all_configs(self):
        """刷新所有配置卡片"""
        for card in self.config_cards.values():
            if hasattr(card, 'load_config'):
                card.load_config()