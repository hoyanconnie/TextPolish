#!/usr/bin/env python3
"""
TextPolish 版本发布脚本
用于自动创建Git标签并触发GitHub Actions构建
"""

import subprocess
import sys
import re
from pathlib import Path


def get_current_version():
    """从pyproject.toml获取当前版本"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    if not pyproject_path.exists():
        print("❌ 未找到 pyproject.toml 文件")
        return None
        
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1)
    
    print("❌ 无法从 pyproject.toml 中解析版本号")
    return None


def update_version(new_version):
    """更新pyproject.toml中的版本号"""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with open(pyproject_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换版本号
    new_content = re.sub(
        r'version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    with open(pyproject_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 已更新版本号为: {new_version}")


def run_command(cmd, description=""):
    """运行命令并处理结果"""
    if description:
        print(f"🔄 {description}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {cmd}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False


def check_git_status():
    """检查Git工作区状态"""
    try:
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            print("❌ Git工作区有未提交的更改，请先提交所有更改")
            print("未提交的文件:")
            print(result.stdout)
            return False
        
        return True
    except subprocess.CalledProcessError:
        print("❌ 无法检查Git状态")
        return False


def get_latest_tag():
    """获取最新的Git标签"""
    try:
        result = subprocess.run(
            "git describe --tags --abbrev=0",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """主函数"""
    print("=" * 50)
    print("TextPolish 版本发布工具")
    print("=" * 50)
    print()
    
    # 检查Git状态
    if not check_git_status():
        return False
    
    # 获取当前版本
    current_version = get_current_version()
    if not current_version:
        return False
    
    print(f"📦 当前版本: {current_version}")
    
    # 获取最新标签
    latest_tag = get_latest_tag()
    if latest_tag:
        print(f"🏷️  最新标签: {latest_tag}")
    else:
        print("🏷️  尚未创建任何标签")
    
    print()
    
    # 询问发布类型
    print("选择发布类型:")
    print("1. 补丁版本 (patch) - 修复bug")
    print("2. 次要版本 (minor) - 新功能")
    print("3. 主要版本 (major) - 重大更改")
    print("4. 自定义版本")
    print("5. 使用当前版本")
    
    choice = input("\n请选择 (1-5): ").strip()
    
    if choice == "1":
        # 补丁版本
        parts = current_version.split('.')
        if len(parts) >= 3:
            parts[2] = str(int(parts[2]) + 1)
            new_version = '.'.join(parts)
        else:
            print("❌ 版本格式不支持自动递增")
            return False
    elif choice == "2":
        # 次要版本
        parts = current_version.split('.')
        if len(parts) >= 3:
            parts[1] = str(int(parts[1]) + 1)
            parts[2] = "0"
            new_version = '.'.join(parts)
        else:
            print("❌ 版本格式不支持自动递增")
            return False
    elif choice == "3":
        # 主要版本
        parts = current_version.split('.')
        if len(parts) >= 3:
            parts[0] = str(int(parts[0]) + 1)
            parts[1] = "0"
            parts[2] = "0"
            new_version = '.'.join(parts)
        else:
            print("❌ 版本格式不支持自动递增")
            return False
    elif choice == "4":
        # 自定义版本
        new_version = input("请输入新版本号 (例如: 1.2.3): ").strip()
        if not re.match(r'^\d+\.\d+\.\d+$', new_version):
            print("❌ 版本号格式错误，应为 x.y.z 格式")
            return False
    elif choice == "5":
        # 使用当前版本
        new_version = current_version
    else:
        print("❌ 无效选择")
        return False
    
    print(f"\n🎯 准备发布版本: {new_version}")
    
    # 确认发布
    confirm = input("确认发布? (y/N): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("❌ 取消发布")
        return False
    
    print("\n🚀 开始发布流程...")
    
    # 更新版本号（如果需要）
    if new_version != current_version:
        update_version(new_version)
        
        # 提交版本更新
        if not run_command("git add pyproject.toml", "添加版本文件到Git"):
            return False
        
        if not run_command(f'git commit -m "chore: bump version to {new_version}"', "提交版本更新"):
            return False
    
    # 创建Git标签
    tag_name = f"v{new_version}"
    if not run_command(f'git tag -a {tag_name} -m "Release {tag_name}"', f"创建标签 {tag_name}"):
        return False
    
    # 推送到远程仓库
    if not run_command("git push origin main", "推送代码到远程仓库"):
        return False
    
    if not run_command(f"git push origin {tag_name}", f"推送标签 {tag_name} 到远程仓库"):
        return False
    
    print("\n" + "=" * 50)
    print("🎉 发布完成！")
    print("=" * 50)
    print(f"📦 版本: {new_version}")
    print(f"🏷️  标签: {tag_name}")
    print()
    print("接下来会发生什么:")
    print("1. GitHub Actions 将自动开始构建")
    print("2. 构建完成后会自动创建 Release")
    print("3. TextPolish.exe 文件会自动上传到 Release")
    print()
    print(f"🔗 查看构建进度: https://github.com/你的用户名/TextPolish/actions")
    print(f"🔗 查看发布页面: https://github.com/你的用户名/TextPolish/releases")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消发布")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发布过程发生错误: {e}")
        sys.exit(1)
