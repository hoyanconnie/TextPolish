#!/usr/bin/env python3
"""
TextPolish Windows exe 构建工具
经过测试的可行方案
"""
import subprocess
import sys
import shutil
from pathlib import Path


def main():
    """主构建函数"""
    print("=" * 50)
    print("TextPolish Windows exe 构建工具")
    print("=" * 50)
    print()
    
    project_root = Path.cwd()
    main_py = project_root / "main.py"
    icon_file = project_root / "icon.ico"
    
    # 检查入口文件
    if not main_py.exists():
        print(f"❌ 未找到入口文件: {main_py}")
        return False
    
    print(f"✅ 找到入口文件: {main_py}")
    
    # 检查图标文件
    if icon_file.exists():
        print(f"✅ 找到图标文件: {icon_file}")
    else:
        print(f"⚠️  未找到图标文件: {icon_file}")
    print()
    
    # 清理旧的构建文件
    print("清理旧的构建文件...")
    for dirname in ["build", "dist"]:
        dir_path = project_root / dirname
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"✅ 已删除 {dirname}/")
    
    # 清理spec文件
    for spec_file in project_root.glob("*.spec"):
        spec_file.unlink()
        print(f"✅ 已删除 {spec_file.name}")
    
    print()
    print("🚀 开始构建...")
    print("这可能需要几分钟时间，请耐心等待...")
    print()
    
    # 使用PyInstaller构建
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",           # 单文件模式
            "--windowed",          # 窗口模式（不显示控制台）
            "--name=TextPolish",   # 指定输出文件名
            "--clean",             # 清理缓存
            "--noconfirm",         # 不询问确认
            "--add-data=icon.ico;.",
        ]
        
        # 如果存在图标文件，添加图标参数
        if icon_file.exists():
            cmd.append(f"--icon={icon_file}")
            
        cmd.append(str(main_py))
        
        print(f"执行命令: {' '.join(cmd[:4])} ... {cmd[-1]}")
        print()
        
        # 运行PyInstaller
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=project_root
        )
        
        print("✅ PyInstaller 执行完成!")
        print()
        
        # 检查构建结果
        exe_path = project_root / "dist" / "TextPolish.exe"
        if exe_path.exists():
            file_size = exe_path.stat().st_size
            size_mb = file_size / (1024 * 1024)
            
            print("=" * 50)
            print("🎉 构建成功！")
            print("=" * 50)
            print()
            print(f"📦 exe文件位置: {exe_path.absolute()}")
            print(f"📏 文件大小: {file_size:,} bytes ({size_mb:.1f} MB)")
            print()
            print("使用说明:")
            print("• 双击 TextPolish.exe 即可运行")
            print("• 可以复制到任何Windows电脑上使用")
            print("• 无需安装Python或其他依赖")
            print()
            return True
        else:
            print("❌ 构建完成但未找到exe文件")
            return False
        
    except subprocess.CalledProcessError as e:
        print("❌ 构建失败！")
        print()
        print("错误信息:")
        if e.stderr:
            print(e.stderr)
        if e.stdout:
            print("输出信息:")
            print(e.stdout)
        print()
        print("💡 解决建议:")
        print("1. 确保已安装所有依赖: uv sync")
        print("2. 检查main.py文件是否可以正常运行")
        print("3. 尝试手动运行: uv run python -m PyInstaller --onefile --windowed main.py")
        return False
        
    except Exception as e:
        print(f"❌ 构建过程发生错误: {e}")
        return False


if __name__ == "__main__":
    try:
        success = main()
        print("构建完成！")
        
        if not success:
            print()
            print("🛠️  如果构建失败，可以尝试手动构建:")
            print("1. uv run python -m PyInstaller --onefile --windowed main.py")
            print("2. 或者: uv run python -m PyInstaller --onefile main.py")
        
        input("\n按回车键退出...")
        
    except KeyboardInterrupt:
        print("\n\n用户中断构建过程")
    except Exception as e:
        print(f"\n发生未预期的错误: {e}")
        input("按回车键退出...")
