#!/usr/bin/env python3
"""
配置文件 - 包含应用程序的所有配置常量
"""

# 应用程序信息
APP_NAME = "TextPolish"
APP_VERSION = "2.0.0"
APP_TITLE = "Gemini文本格式修复工具"
APP_ORGANIZATION = "TextPolish"

# 窗口配置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 40
PRIMARY_BUTTON_HEIGHT = 45

# 分割器配置
SPLITTER_SIZES = [400, 200, 400]  # 左侧40%，中间20%，右侧40%
SPLITTER_HANDLE_WIDTH = 1

# 字体配置
FONTS = {
    "preview": {
        "family": "Microsoft YaHei",
        "size": 14
    },
    "ui_label": {
        "size": 10
    },
    "level_label": {
        "size": 9
    }
}

# 旧的静态配置已移除，现在使用用户可配置系统 user_config_manager

# 标点符号替换映射
PUNCTUATION_MAP = {
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

# 主题颜色配置
THEME_COLORS = {
    "dark": {
        "body": "#ffffff",
        "h1": "#74b9ff",
        "h2": "#a29bfe", 
        "h3": "#fd79a8",
        "special": "#ff7675",
        "normal": "#ddd"
    },
    "light": {
        "body": "#333333",
        "h1": "#2c3e50",
        "h2": "#34495e",
        "h3": "#2980b9", 
        "special": "#e74c3c",
        "normal": "#333"
    }
}

# 消息配置
MESSAGES = {
    "success": {
        "process_complete": "处理完成",
        "copy_success": "复制成功",
        "theme_switched": "主题已切换"
    },
    "warning": {
        "no_input": "请先输入要处理的文本！",
        "no_content": "没有可复制的内容"
    },
    "error": {
        "process_failed": "处理失败",
        "copy_failed": "复制失败",
        "formatted_copy_failed": "格式化复制失败",
        "icon_load_failed": "设置窗口图标失败",
        "app_icon_failed": "设置应用程序图标失败",
        "startup_failed": "程序启动失败"
    },
    "info": {
        "cleared": "已清空",
        "processing": "正在处理...",
        "ready": "就绪"
    }
}

# 图标文件路径配置
ICON_PATHS = {
    "ico": "icon.ico"
}

# HTML模板配置
HTML_NAMESPACE = 'xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40"'


# =============================================
# 新的用户可配置系统
# =============================================

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from PyQt6.QtCore import QSettings


@dataclass
class StyleConfig:
    """标题样式配置"""
    font_family: str = "方正仿宋_GBK"
    font_size: str = "16.0000pt"
    font_kerning: str = "1.0000pt"
    font_weight: str = "normal"
    alignment: str = "left"
    text_indent: str = "0.0000pt"
    description: str = ""


@dataclass
class RegexPattern:
    """正则表达式模式"""
    pattern: str
    name: str
    enabled: bool = True
    description: str = ""


@dataclass
class TitleConfig:
    """标题级别配置"""
    style: StyleConfig
    patterns: List[RegexPattern]


class UserConfigManager:
    """用户配置管理器"""
    
    def __init__(self):
        # 设置QSettings的组织名称和应用名称，确保配置文件有合适的路径
        self.settings = QSettings(APP_ORGANIZATION, APP_NAME)
        self._config: Dict[str, TitleConfig] = {}
        self._load_default_config()
        self.load_config()
    
    def _load_default_config(self):
        """加载默认配置"""
        # 尝试从应用配置文件加载
        app_config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'app_config.json')
        app_config_path = os.path.abspath(app_config_path)
        
        if self.load_from_app_config(app_config_path):
            print("成功从应用配置文件加载默认设置")
            return
        
        # 如果应用配置文件不存在或加载失败，使用代码中的默认配置
        print("使用代码中的默认配置")
        self._config = {
            "h1": TitleConfig(
                style=StyleConfig(
                    font_family="方正小标宋_GBK",
                    font_size="18.0000pt",
                    font_kerning="22.0000pt",
                    font_weight="normal",
                    alignment="center",
                    text_indent="0.0000pt",
                    description="一级标题：第一章第二章到换行符为止，字体：方正小标宋_GBK；字号：小二；格式：居中"
                ),
                patterns=[
                    RegexPattern(
                        pattern=r'^第[一二三四五六七八九十\d]+章',
                        name="章节标题",
                        enabled=True,
                        description="第一章、第二章等"
                    ),
                    RegexPattern(
                        pattern=r'^前言$',
                        name="前言标题",
                        enabled=True,
                        description="前言"
                    )
                ]
            ),
            "h2": TitleConfig(
                style=StyleConfig(
                    font_family="方正黑体_GBK",
                    font_size="16.0000pt",
                    font_kerning="1.0000pt",
                    font_weight="normal",
                    alignment="center",
                    text_indent="0.0000pt",
                    description="二级标题：第一节第二节到换行符为止或者一、二、到换行符为止，字体：方正黑体_GBK；字号：三号；格式：居中"
                ),
                patterns=[
                    RegexPattern(
                        pattern=r'^第[一二三四五六七八九十\d]+节',
                        name="节次标题",
                        enabled=True,
                        description="第一节、第二节等"
                    ),
                    RegexPattern(
                        pattern=r'^[一二三四五六七八九十]+、',
                        name="序号标题",
                        enabled=True,
                        description="一、二、等"
                    )
                ]
            ),
            "h3": TitleConfig(
                style=StyleConfig(
                    font_family="方正楷体_GBK",
                    font_size="16.0000pt",
                    font_kerning="1.0000pt",
                    font_weight="bold",
                    alignment="justify",
                    text_indent="0.0000pt",
                    description="三级标题：段落的开始第一句到句号为止，字体：方正楷体_GBK；字号：三号加粗；格式：两端对齐"
                ),
                patterns=[
                    RegexPattern(
                        pattern=r'^（[一二三四五六七八九十\d]+）',
                        name="带括号序号",
                        enabled=True,
                        description="（一）、（二）等"
                    )
                ]
            ),
            "normal": TitleConfig(
                style=StyleConfig(
                    font_family="方正仿宋_GBK",
                    font_size="16.0000pt",
                    font_kerning="1.0000pt",
                    text_indent="36.0000pt",
                    description="正文：字体：方正仿宋_GBK；字号：三号；格式：首行缩进2字符"
                ),
                patterns=[]
            ),
            "special_format": TitleConfig(
                style=StyleConfig(
                    font_family="方正楷体_GBK",
                    font_size="16.0000pt",
                    font_kerning="1.0000pt",
                    font_weight="bold",
                    alignment="justify",
                    text_indent="0.0000pt",
                    description="特殊格式：特殊句式识别"
                ),
                patterns=[
                    RegexPattern(
                        pattern=r'^（([一二三四五六七八九十\d]+)）([^。]+。)(.*)',
                        name="括号序号标题",
                        enabled=True,
                        description="（一）、（二）等格式到句号"
                    ),
                    RegexPattern(
                        pattern=r'^([一二三四五六七八九十\d]+[是的][^。]*。)(.*)',
                        name="特殊句式到句号",
                        enabled=True,
                        description="第一句到句号"
                    ),
                    RegexPattern(
                        pattern=r'^([^：]*：)(.*)',
                        name="标题到冒号",
                        enabled=True,
                        description="段落开头到冒号"
                    )
                ]
            )
        }
    
    def get_config(self, level: str) -> Optional[TitleConfig]:
        """获取指定级别的配置"""
        return self._config.get(level)
    
    def get_all_configs(self) -> Dict[str, TitleConfig]:
        """获取所有配置"""
        return self._config.copy()
    
    def update_style(self, level: str, style: StyleConfig):
        """更新样式配置"""
        if level in self._config:
            self._config[level].style = style
            self.save_config()
    
    def update_patterns(self, level: str, patterns: List[RegexPattern]):
        """更新正则表达式配置"""
        if level in self._config:
            self._config[level].patterns = patterns
            self.save_config()
    
    def update_level_config(self, level: str, style: StyleConfig = None, patterns: List[RegexPattern] = None):
        """批量更新指定级别的配置（避免重复保存）"""
        if level in self._config:
            if style:
                self._config[level].style = style
            if patterns is not None:
                self._config[level].patterns = patterns
            self.save_config()
    
    def add_pattern(self, level: str, pattern: RegexPattern):
        """添加新的正则表达式"""
        if level in self._config:
            self._config[level].patterns.append(pattern)
            self.save_config()
    
    def remove_pattern(self, level: str, pattern_index: int):
        """移除正则表达式"""
        if level in self._config and 0 <= pattern_index < len(self._config[level].patterns):
            del self._config[level].patterns[pattern_index]
            self.save_config()
    
    def toggle_pattern(self, level: str, pattern_index: int):
        """切换正则表达式启用状态"""
        if level in self._config and 0 <= pattern_index < len(self._config[level].patterns):
            pattern = self._config[level].patterns[pattern_index]
            pattern.enabled = not pattern.enabled
            self.save_config()
    
    def save_config(self):
        """保存配置到QSettings"""
        try:
            # 确保配置目录存在
            import os
            config_file_path = self.settings.fileName()
            config_dir = os.path.dirname(config_file_path)
            if not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
                print(f"创建配置目录: {config_dir}")
            
            config_dict = {}
            for level, title_config in self._config.items():
                config_dict[level] = {
                    'style': asdict(title_config.style),
                    'patterns': [asdict(pattern) for pattern in title_config.patterns]
                }
            
            self.settings.setValue("user_config", json.dumps(config_dict, ensure_ascii=False))
            # 强制同步到文件
            self.settings.sync()
            print(f"配置已保存到: {config_file_path}")
            
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def load_config(self):
        """从QSettings加载配置，如果没有用户配置则使用默认配置"""
        try:
            config_data = self.settings.value("user_config", "")
            if config_data:
                print("加载用户配置...")
                config_dict = json.loads(config_data)
                
                for level, data in config_dict.items():
                    if level in self._config:
                        # 加载样式配置
                        style_data = data.get('style', {})
                        style = StyleConfig(**style_data)
                        
                        # 加载正则表达式配置
                        patterns_data = data.get('patterns', [])
                        patterns = [RegexPattern(**pattern_data) for pattern_data in patterns_data]
                        
                        self._config[level] = TitleConfig(style=style, patterns=patterns)
                
                print(f"用户配置加载成功，共 {len(config_dict)} 个级别")
            else:
                print("未找到用户配置，使用默认配置")
                # 第一次运行时保存默认配置
                self.save_config()
                        
        except Exception as e:
            print(f"加载配置失败，使用默认配置: {e}")
            # 发生错误时重新加载默认配置
            self._load_default_config()
    
    def reset_to_default(self):
        """重置为默认配置"""
        self._load_default_config()
        self.save_config()
    
    def get_enabled_patterns(self, level: str) -> List[str]:
        """获取指定级别的启用正则表达式"""
        if level not in self._config:
            return []
        
        return [pattern.pattern for pattern in self._config[level].patterns if pattern.enabled]
    
    def get_style_dict(self, level: str) -> Dict:
        """获取指定级别的样式字典（兼容原有格式）"""
        if level not in self._config:
            return {}
        
        style = self._config[level].style
        return asdict(style)
    
    def save_ui_settings(self, settings: Dict):
        """保存界面设置"""
        try:
            self.settings.setValue("ui_settings", json.dumps(settings, ensure_ascii=False))
            self.settings.sync()
            print(f"界面设置已保存: {settings}")
        except Exception as e:
            print(f"保存界面设置失败: {e}")
    
    def load_ui_settings(self) -> Dict:
        """加载界面设置"""
        try:
            settings_data = self.settings.value("ui_settings", "")
            if settings_data:
                return json.loads(settings_data)
            else:
                # 返回默认设置
                return {
                    'enable_h1': True,
                    'enable_h2': True, 
                    'enable_h3': True,
                    'enable_special': True
                }
        except Exception as e:
            print(f"加载界面设置失败: {e}")
            # 返回默认设置
            return {
                'enable_h1': True,
                'enable_h2': True,
                'enable_h3': True, 
                'enable_special': True
            }
    
    def get_config_file_path(self) -> str:
        """获取配置文件的完整路径"""
        return self.settings.fileName()
    
    def export_config_to_file(self, file_path: str):
        """导出配置到指定文件"""
        try:
            config_dict = {}
            for level, title_config in self._config.items():
                config_dict[level] = {
                    'style': asdict(title_config.style),
                    'patterns': [asdict(pattern) for pattern in title_config.patterns]
                }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出配置失败: {e}")
            return False
    
    def import_config_from_file(self, file_path: str):
        """从指定文件导入配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            for level, data in config_dict.items():
                if level in self._config:
                    # 加载样式配置
                    style_data = data.get('style', {})
                    style = StyleConfig(**style_data)
                    
                    # 加载正则表达式配置
                    patterns_data = data.get('patterns', [])
                    patterns = [RegexPattern(**pattern_data) for pattern_data in patterns_data]
                    
                    self._config[level] = TitleConfig(style=style, patterns=patterns)
            
            # 保存到QSettings
            self.save_config()
            return True
            
        except Exception as e:
            print(f"导入配置失败: {e}")
            return False
    
    def initialize_from_project_config(self, project_config_path: str):
        """从项目配置文件初始化用户配置（仅在首次运行时）"""
        try:
            # 检查是否已有用户配置
            if self.settings.value("user_config", ""):
                return False  # 已有用户配置，不需要初始化
            
            # 从项目配置文件导入
            if os.path.exists(project_config_path):
                print(f"首次运行，从项目配置初始化: {project_config_path}")
                return self.import_config_from_file(project_config_path)
            
            return False
            
        except Exception as e:
            print(f"从项目配置初始化失败: {e}")
            return False
    
    def load_from_app_config(self, app_config_path: str):
        """从合并的应用配置文件加载默认配置"""
        try:
            if os.path.exists(app_config_path):
                with open(app_config_path, 'r', encoding='utf-8') as f:
                    app_config = json.load(f)
                
                # 加载默认用户配置
                default_user_config = app_config.get('default_user_config', {})
                if default_user_config:
                    print(f"从应用配置加载默认设置: {app_config_path}")
                    
                    for level, data in default_user_config.items():
                        if level in self._config:
                            # 加载样式配置
                            style_data = data.get('style', {})
                            style = StyleConfig(**style_data)
                            
                            # 加载正则表达式配置
                            patterns_data = data.get('patterns', [])
                            patterns = [RegexPattern(**pattern_data) for pattern_data in patterns_data]
                            
                            self._config[level] = TitleConfig(style=style, patterns=patterns)
                    
                    return True
                
        except Exception as e:
            print(f"从应用配置加载失败: {e}")
        
        return False


# 全局配置管理器实例
user_config_manager = UserConfigManager()
