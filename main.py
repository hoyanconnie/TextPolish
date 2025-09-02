#!/usr/bin/env python3
"""
TextPolish - Gemini文本格式修复工具
主程序入口文件

用于处理Gemini AI回答文本复制到Word后的格式混乱问题
"""

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

if __name__ == "__main__":
    try:
        from src.textpolish.app import main
        sys.exit(main())
    except ImportError as e:
        print(f"模块导入失败: {e}")
        print("请检查项目结构是否完整")
        sys.exit(1)
    except Exception as e:
        print(f"程序启动失败: {e}")
        sys.exit(1)
