#!/usr/bin/env python3
"""
核心模块 - 包含文本处理和HTML生成的核心功能
"""

from .text_processor import TextProcessor
from .html_generator import HTMLGenerator

__all__ = ['TextProcessor', 'HTMLGenerator']
