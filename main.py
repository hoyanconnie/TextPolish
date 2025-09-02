#!/usr/bin/env python3
"""
TextPolish - Gemini文本格式修复工具
主程序入口文件

用于处理Gemini AI回答文本复制到Word后的格式混乱问题
"""

import sys
import os
from src.textpolish.app import main

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')

if __name__ == "__main__":
    sys.exit(main())

