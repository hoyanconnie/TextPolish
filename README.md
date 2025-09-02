# TextPolish - Gemini文本格式修复工具

> 专门解决Gemini AI回答复制到Word后格式混乱问题的Windows桌面工具

## 🚀 快速开始

### 方式1：直接使用（推荐）
双击运行 `dist\TextPolish.exe`，无需安装Python环境。

### 方式2：重新构建
双击运行 `build_windows.bat`，自动构建新的exe文件。

### 方式3：开发运行
```cmd
# 使用uv（推荐）
uv run python main.py

# 或使用pip
pip install pyperclip
python main.py
```

## ✨ 主要功能

- 🔧 **删除特殊符号**：自动删除 ·、•、▲、■ 等Gemini输出符号
- 📝 **标点转换**：智能将英文标点转为中文标点（，。：！？等）
- 🎯 **格式优化**：清理多余空格和换行，保持文本紧凑
- 📋 **一键复制**：处理结果直接复制到剪贴板
- ⚡ **快捷操作**：支持 Ctrl+Enter 和 F5 快捷键

## 🔧 处理效果示例

### 处理前：
```
· Gemini AI是一个强大的工具, 它能够: 
• 生成文本
▲ 回答问题
■ 提供帮助
但是(复制到Word后), 格式会很混乱! 真的吗?
```

### 处理后：
```
Gemini AI是一个强大的工具，它能够：
生成文本
回答问题
提供帮助
但是（复制到Word后），格式会很混乱！真的吗？
```

## 📁 文件说明

- `dist/TextPolish.exe` - 可执行程序（推荐使用）
- `main.py` - 程序源码
- `build_windows.bat` - exe构建脚本
- `pyproject.toml` - 项目配置（uv管理）
- `requirements.txt` - pip依赖列表

## 💡 使用方法

1. **启动程序**：双击 `TextPolish.exe`
2. **粘贴文本**：在左侧输入框粘贴Gemini回答的文本
3. **处理文本**：点击"处理文本"按钮或按 Ctrl+Enter
4. **复制结果**：点击"复制结果"按钮，粘贴到Word等应用

## ⚙️ 系统要求

- **Windows 7/8/10/11**（64位）
- **内存**：至少 100MB 可用内存
- **存储**：约 30MB 磁盘空间

## 🔨 开发构建

### 重新构建exe
```cmd
# 自动构建（推荐）
build_windows.bat

# 手动构建
uv sync --dev
uv run pyinstaller TextPolish.spec
```

### 开发环境
```cmd
# 安装依赖
uv sync

# 运行开发版
uv run python main.py
```

## 🆘 常见问题

**Q: exe文件被杀毒软件拦截？**  
A: PyInstaller打包程序的常见误报，请添加到白名单。

**Q: 程序无法启动？**  
A: 确保是64位Windows系统，尝试"以管理员身份运行"。

**Q: 处理效果不满意？**  
A: 程序专门针对Gemini AI输出格式优化，其他来源文本可能效果不同。

## 📜 许可证

MIT License - 免费使用，无需商业授权。

---

**提示**：首次使用建议用少量文本测试效果，确认满意后再处理大量内容。
