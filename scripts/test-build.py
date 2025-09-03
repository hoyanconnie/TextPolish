#!/usr/bin/env python3
"""
本地构建测试脚本
用于在提交前本地测试构建流程
"""

import subprocess
import sys
import shutil
from pathlib import Path
import time


def run_command(cmd, description="", cwd=None):
    """运行命令并处理结果"""
    if description:
        print(f"🔄 {description}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            cwd=cwd,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {cmd}")
        print(f"错误代码: {e.returncode}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("TextPolish 本地构建测试")
    print("=" * 50)
    print()
    
    project_root = Path(__file__).parent.parent
    print(f"📁 项目根目录: {project_root.absolute()}")
    
    # 检查必要文件
    required_files = ["main.py", "pyproject.toml", "build.py"]
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"✅ 找到: {file}")
        else:
            print(f"❌ 缺失: {file}")
            return False
    
    print()
    
    # 模拟GitHub Actions环境测试
    print("🧪 模拟GitHub Actions构建流程...")
    print()
    
    # 1. 安装依赖
    if not run_command("uv sync", "安装项目依赖", cwd=project_root):
        return False
    
    print("✅ 依赖安装完成")
    print()
    
    # 2. 运行构建
    print("🔨 开始构建...")
    start_time = time.time()
    
    if not run_command("uv run python build.py", "执行构建脚本", cwd=project_root):
        return False
    
    build_time = time.time() - start_time
    print(f"✅ 构建完成 (耗时: {build_time:.1f}秒)")
    print()
    
    # 3. 验证构建结果
    exe_path = project_root / "dist" / "TextPolish.exe"
    if exe_path.exists():
        file_size = exe_path.stat().st_size
        size_mb = file_size / (1024 * 1024)
        
        print("=" * 50)
        print("🎉 本地构建测试成功！")
        print("=" * 50)
        print(f"📦 exe文件: {exe_path}")
        print(f"📏 文件大小: {file_size:,} bytes ({size_mb:.1f} MB)")
        print(f"⏱️  构建耗时: {build_time:.1f}秒")
        print()
        print("✅ GitHub Actions构建应该能够正常工作")
        print()
        
        # 询问是否清理构建文件
        clean = input("是否清理构建文件? (Y/n): ").strip().lower()
        if clean in ['', 'y', 'yes']:
            # 清理构建文件
            for dirname in ["build", "dist"]:
                dir_path = project_root / dirname
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                    print(f"🗑️  已删除 {dirname}/")
            
            # 清理spec文件
            for spec_file in project_root.glob("*.spec"):
                spec_file.unlink()
                print(f"🗑️  已删除 {spec_file.name}")
        
        return True
    else:
        print("❌ 构建失败：未找到exe文件")
        return False


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n💡 建议:")
            print("1. 检查所有依赖是否正确安装")
            print("2. 确保main.py可以正常运行")
            print("3. 检查build.py脚本是否有问题")
            sys.exit(1)
        else:
            print("🚀 可以安全地提交代码并创建标签了！")
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程发生错误: {e}")
        sys.exit(1)
