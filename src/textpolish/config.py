#!/usr/bin/env python3
"""
配置文件 - 包含应用程序的所有配置常量
"""

# 应用程序信息
APP_NAME = "TextPolish"
APP_VERSION = "2.0.0"
APP_TITLE = "TextPolish - Gemini文本格式修复工具"
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

# 标题格式配置（来自要求.md）
TITLE_FORMATS = {
    "h1": {
        "font_family": "方正小标宋_GBK",
        "font_size": "18.0000pt",
        "font_kerning": "22.0000pt",
        "alignment": "center",
        "description": "一级标题：第一章第二章到换行符为止，字体：方正小标宋_GBK；字号：小二；格式：居中"
    },
    "h2": {
        "font_family": "方正黑体_GBK", 
        "font_size": "16.0000pt",
        "font_kerning": "1.0000pt",
        "alignment": "center",
        "description": "二级标题：第一节第二节到换行符为止或者一、二、到换行符为止，字体：方正黑体_GBK；字号：三号；格式：居中"
    },
    "h3": {
        "font_family": "方正楷体_GBK",
        "font_size": "16.0000pt", 
        "font_kerning": "1.0000pt",
        "font_weight": "bold",
        "alignment": "justify",
        "description": "三级标题：段落的开始第一句到句号为止，字体：方正楷体_GBK；字号：三号加粗；格式：两端对齐"
    },
    "normal": {
        "font_family": "方正仿宋_GBK",
        "font_size": "16.0000pt",
        "font_kerning": "1.0000pt", 
        "text_indent": "36.0000pt",
        "description": "正文：字体：方正仿宋_GBK；字号：三号；格式：首行缩进2字符"
    }
}

# 标题识别正则表达式
TITLE_PATTERNS = {
    "h1": [
        r'^第[一二三四五六七八九十\d]+章',  # 第一章、第二章等
        r'^前言$'  # 前言
    ],
    "h2": [
        r'^第[一二三四五六七八九十\d]+节',  # 第一节、第二节等
        r'^[一二三四五六七八九十]+、'  # 一、二、等
    ],
    "h3": [
        r'^（[一二三四五六七八九十\d]+）'  # （一）、（二）等
    ],
    "special_format": [
        r'^([一二三四五六七八九十\d]+[是的][^。]*。)(.*)',  # 第一句到句号
        r'^([^：]*：)(.*)'  # 段落开头到冒号
    ]
}

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
