# TextPolish 构建说明

## 📦 构建Windows可执行文件

### 快速构建
```bash
uv run python build.py
```

### 手动构建（备用方案）
```bash
uv run python -m PyInstaller --onefile --windowed main.py
```

## 🎯 构建结果
- 输出文件：`dist/TextPolish.exe`
- 文件大小：约 87MB
- 依赖：无需额外安装

## 📋 环境要求
- Python 3.13+
- uv 包管理器
- Windows 系统

## 🔧 故障排除
如果构建失败，请尝试：
1. 确保依赖已安装：`uv sync`
2. 检查main.py能否正常运行：`uv run python main.py`
3. 手动运行PyInstaller命令

## 📁 项目结构
```
TextPolish/
├── main.py          # 主程序入口
├── build.py         # 构建脚本
├── pyproject.toml   # 项目配置
├── uv.lock          # 依赖锁定文件
├── .gitignore       # Git忽略文件
└── dist/            # 构建输出目录（生成）
    └── TextPolish.exe
```
