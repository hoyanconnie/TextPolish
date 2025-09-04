#!/usr/bin/env python3
"""
HTML生成模块 - 负责将文本转换为格式化的HTML
"""

import re
from typing import Dict, List, Tuple, Optional

from ..config import TITLE_PATTERNS, TITLE_FORMATS, THEME_COLORS, HTML_NAMESPACE


class HTMLGenerator:
    """HTML生成器 - 负责将文本转换为HTML格式"""
    
    def __init__(self):
        """初始化HTML生成器"""
        self.title_patterns = TITLE_PATTERNS
        self.title_formats = TITLE_FORMATS
        self.theme_colors = THEME_COLORS
    
    def convert_to_html(self, text: str, enable_h1: bool = True, 
                       enable_h2: bool = True, enable_h3: bool = True) -> str:
        """
        将文本转换为HTML格式，根据标题规则识别标题层级
        
        Args:
            text: 输入文本
            enable_h1: 是否启用一级标题格式
            enable_h2: 是否启用二级标题格式 
            enable_h3: 是否启用三级标题格式
            
        Returns:
            HTML body内容（不包含完整HTML文档结构）
        """
        if not text.strip():
            return ""
        
        lines = text.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 识别并处理各级标题
            html_line = self._process_line(line, enable_h1, enable_h2, enable_h3)
            html_lines.append(html_line)
        
        return '\n'.join(html_lines)
    
    def _wrap_numbers_with_western_font(self, text: str) -> str:
        """将数字序列包裹为 Times New Roman 字体，保留其余文本字体不变"""
        def repl(match):
            num = match.group(0)
            return (
                '<span style="font-family:\'Times New Roman\';" '
                + 'mso-ascii-font-family:\'Times New Roman\';'
                + 'mso-hansi-font-family:\'Times New Roman\';'
                + 'mso-bidi-font-family:\'Times New Roman\';>'
                + num
                + '</span>'
            )
        # 数字序列：支持千分位逗号、小数点、百分号、年号中的数字
        pattern = r"(?<![A-Za-z])(?:\d[\d,\.]*%?)"
        return re.sub(pattern, repl, text)
    
    def _process_line(self, line: str, enable_h1: bool, 
                     enable_h2: bool, enable_h3: bool) -> str:
        """
        处理单行文本，识别标题级别并生成相应HTML
        
        Args:
            line: 单行文本
            enable_h1: 是否启用一级标题
            enable_h2: 是否启用二级标题
            enable_h3: 是否启用三级标题
            
        Returns:
            格式化的HTML行
        """
        # 检查一级标题
        if enable_h1 and self._is_title_level(line, 'h1'):
            return self._generate_title_html(line, 'h1')
        
        # 检查二级标题
        if enable_h2 and self._is_title_level(line, 'h2'):
            return self._generate_title_html(line, 'h2')
        
        # 检查三级标题
        if enable_h3 and self._is_title_level(line, 'h3'):
            return self._generate_title_html(line, 'h3')
        
        # 检查特殊格式段落
        if enable_h3:
            special_html = self._process_special_format(line)
            if special_html:
                return special_html
        
        # 普通正文
        return self._generate_normal_paragraph(line)
    
    def _is_title_level(self, line: str, level: str) -> bool:
        """
        检查行是否匹配指定级别的标题模式
        
        Args:
            line: 文本行
            level: 标题级别 ('h1', 'h2', 'h3')
            
        Returns:
            是否匹配
        """
        patterns = self.title_patterns.get(level, [])
        return any(re.match(pattern, line) for pattern in patterns)
    
    def _generate_title_html(self, line: str, level: str) -> str:
        """
        生成标题HTML
        
        Args:
            line: 标题文本
            level: 标题级别
            
        Returns:
            标题HTML
        """
        format_info = self.title_formats[level]
        
        span_style = (
            f"mso-spacerun:'yes';"
            f"mso-fareast-font-family:{format_info['font_family']};"
            f"mso-ascii-font-family:{format_info['font_family']};"
            f"mso-hansi-font-family:{format_info['font_family']};"
            f"mso-bidi-font-family:{format_info['font_family']};"
            f"font-size:{format_info['font_size']};"
            f"mso-font-kerning:{format_info['font_kerning']};"
        )
        
        if level == 'h3' and 'font_weight' in format_info:
            span_style += f"font-weight:{format_info['font_weight']};"
        
        content = self._wrap_numbers_with_western_font(line)
        return f'<{level}><span style="{span_style}">{content}</span></{level}>'
    
    def _process_special_format(self, line: str) -> Optional[str]:
        """
        处理特殊格式段落（第一句到句号、开头到冒号）
        
        Args:
            line: 文本行
            
        Returns:
            特殊格式HTML或None
        """
        # 检查第一句到句号
        first_sentence_match = re.match(self.title_patterns['special_format'][0], line)
        # 检查开头到冒号  
        colon_match = re.match(self.title_patterns['special_format'][1], line)
        
        if first_sentence_match or colon_match:
            if first_sentence_match:
                special_part = first_sentence_match.group(1)
                remaining_text = first_sentence_match.group(2).strip()
            else:  # colon_match
                special_part = colon_match.group(1)
                remaining_text = colon_match.group(2).strip()
            
            # 构建特殊格式HTML
            html_content = '<p class="MsoNormal" style="text-align:justify;text-justify:inter-ideograph;">'
            
            # 特殊部分（楷体加粗）
            special_style = (
                "mso-spacerun:'yes';"
                "mso-fareast-font-family:方正楷体_GBK;"
                "mso-ascii-font-family:方正楷体_GBK;"
                "mso-hansi-font-family:方正楷体_GBK;"
                "mso-bidi-font-family:方正楷体_GBK;"
                "font-size:16.0000pt;"
                "font-weight:bold;"
                "mso-font-kerning:1.0000pt;"
            )
            html_content += f'<b><span style="{special_style}">{self._wrap_numbers_with_western_font(special_part)}</span></b>'
            
            # 剩余部分（正文格式）
            if remaining_text:
                normal_style = (
                    "mso-spacerun:'yes';"
                    "mso-fareast-font-family:方正仿宋_GBK;"
                    "mso-ascii-font-family:方正仿宋_GBK;"
                    "mso-hansi-font-family:方正仿宋_GBK;"
                    "mso-bidi-font-family:方正仿宋_GBK;"
                    "font-size:16.0000pt;"
                    "mso-font-kerning:1.0000pt;"
                )
                html_content += f'<span style="{normal_style}">{self._wrap_numbers_with_western_font(remaining_text)}</span>'
            
            html_content += '</p>'
            return html_content
        
        return None
    
    def _generate_normal_paragraph(self, line: str) -> str:
        """
        生成普通正文段落HTML
        
        Args:
            line: 文本行
            
        Returns:
            段落HTML
        """
        normal_style = (
            "mso-spacerun:'yes';"
            "mso-fareast-font-family:方正仿宋_GBK;"
            "mso-ascii-font-family:方正仿宋_GBK;"
            "mso-hansi-font-family:方正仿宋_GBK;"
            "mso-bidi-font-family:方正仿宋_GBK;"
            "font-size:16.0000pt;"
            "mso-font-kerning:1.0000pt;"
        )
        
        content = self._wrap_numbers_with_western_font(line)
        return f'<p class="MsoNormal"><span style="{normal_style}">{content}</span></p>'
    
    def generate_preview_html(self, body_content: str, is_dark_theme: bool = False) -> str:
        """
        生成用于预览的HTML（带主题颜色）
        
        Args:
            body_content: HTML body内容
            is_dark_theme: 是否为深色主题
            
        Returns:
            完整的预览HTML文档
        """
        theme_key = "dark" if is_dark_theme else "light"
        colors = self.theme_colors[theme_key]
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>格式预览</title>
<style>
/* 简化样式，确保TextBrowser兼容性，支持暗色模式 */
body {{
    font-family: "Microsoft YaHei", "SimSun", serif;
    font-size: 14px;
    line-height: 1.5;
    margin: 15px;
    color: {colors['body']};
}}

/* 一级标题 */
h1 {{
    font-size: 18px;
    font-weight: bold;
    text-align: center;
    margin: 10px 0;
    color: {colors['h1']};
}}

/* 二级标题 */
h2 {{
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    margin: 8px 0;
    color: {colors['h2']};
}}

/* 三级标题 */
h3 {{
    font-size: 14px;
    font-weight: bold;
    text-align: left;
    margin: 6px 0;
    color: {colors['h3']};
}}

/* 正文段落 */
p.MsoNormal {{
    margin: 5px 0;
    text-indent: 2em;
    text-align: justify;
    font-size: 14px;
    color: {colors['normal']};
}}

/* 特殊格式段落中的加粗部分 */
.special-bold {{
    font-weight: bold;
    color: {colors['special']};
}}

/* 普通段落中的文本 */
.normal-text {{
    font-weight: normal;
    color: {colors['normal']};
}}
</style>
</head>
<body>
{body_content}
</body>
</html>"""
        return html_template
    
    def generate_wps_html(self, body_content: str) -> str:
        """
        生成用于复制到WPS的HTML（严格按照要求.md）
        
        Args:
            body_content: HTML body内容
            
        Returns:
            完整的WPS兼容HTML文档
        """
        html_template = f"""<html {HTML_NAMESPACE}>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="ProgId" content="Word.Document">
<meta name="Generator" content="Microsoft Word 14">
<title>处理后的文档</title>
<style>
# @font-face {{
#     font-family: "Times New Roman";
# }}

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
    mso-fareast-font-family: 方正仿宋_GBK;
    mso-ascii-font-family: 方正仿宋_GBK;
    mso-hansi-font-family: 方正仿宋_GBK;
    mso-bidi-font-family: 方正仿宋_GBK;
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
    mso-fareast-font-family: 方正小标宋_GBK;
    mso-ascii-font-family: 方正小标宋_GBK;
    mso-hansi-font-family: 方正小标宋_GBK;
    mso-bidi-font-family: 方正小标宋_GBK;
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
    mso-fareast-font-family: 方正黑体_GBK;
    mso-ascii-font-family: 方正黑体_GBK;
    mso-hansi-font-family: 方正黑体_GBK;
    mso-bidi-font-family: 方正黑体_GBK;
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
    mso-fareast-font-family: 方正楷体_GBK;
    mso-ascii-font-family: 方正楷体_GBK;
    mso-hansi-font-family: 方正楷体_GBK;
    mso-bidi-font-family: 方正楷体_GBK;
    font-size: 16.0000pt;
    font-weight: bold;
    mso-font-kerning: 1.0000pt;
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
        return html_template
