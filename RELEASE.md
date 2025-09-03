# TextPolish 自动发布指南

这个文档详细说明了如何使用GitHub Actions自动构建和发布TextPolish exe文件。

## 🚀 快速开始

### 1. 首次设置

确保你的GitHub仓库已经配置了SSH密钥并能正常推送。

### 2. 发布新版本

使用提供的脚本进行版本发布：

```powershell
# Windows PowerShell
uv run python scripts/release.py
```

或者手动创建标签：

```bash
# 更新版本号（编辑 pyproject.toml）
# 提交更改
git add pyproject.toml
git commit -m "chore: bump version to 1.0.1"

# 创建标签
git tag -a v1.0.1 -m "Release v1.0.1"

# 推送到GitHub
git push origin main
git push origin v1.0.1
```

### 3. 自动构建

一旦推送标签到GitHub，会自动触发以下流程：

1. **构建触发**: GitHub检测到新的`v*`标签
2. **环境准备**: 设置Python 3.13和uv环境
3. **依赖安装**: 运行`uv sync`安装所有依赖
4. **exe构建**: 执行`build.py`生成Windows可执行文件
5. **文件验证**: 检查exe文件是否成功生成
6. **创建Release**: 自动创建GitHub Release并上传exe文件

## 📋 工作流程详解

### 构建环境

- **操作系统**: Windows Latest (GitHub Actions)
- **Python版本**: 3.13
- **包管理器**: uv
- **构建工具**: PyInstaller

### 触发条件

工作流在以下情况下触发：

1. **自动触发**: 推送格式为`v*`的标签（如`v1.0.0`、`v2.1.3`）
2. **手动触发**: 在GitHub Actions页面手动运行

### 构建步骤

```yaml
1. 检出代码 (actions/checkout@v4)
2. 安装Python (actions/setup-python@v4)
3. 安装uv (astral-sh/setup-uv@v3)
4. 安装项目依赖 (uv sync)
5. 构建exe文件 (uv run python build.py)
6. 验证构建结果
7. 上传构建产物 (actions/upload-artifact@v4)
8. 创建Release (softprops/action-gh-release@v1)
```

## 🛠️ 本地测试

在发布前，建议先在本地测试构建流程：

```powershell
# 运行本地构建测试
uv run python scripts/test-build.py
```

这个脚本会：
- 检查必要文件是否存在
- 模拟GitHub Actions的构建流程
- 验证exe文件是否正确生成
- 报告构建时间和文件大小

## 📦 Release内容

每个自动创建的Release包含：

### 文件
- `TextPolish.exe` - Windows可执行文件

### Release说明
- 版本号和下载链接
- 功能特性说明
- 系统要求
- 使用说明
- 构建信息（时间、Git提交等）

## 🔧 版本管理

### 版本号格式

使用语义化版本号：`MAJOR.MINOR.PATCH`

- **MAJOR**: 重大更改，可能破坏兼容性
- **MINOR**: 新功能，向后兼容
- **PATCH**: bug修复，向后兼容

### 自动版本递增

`release.py` 脚本支持：

1. **补丁版本** (1.0.0 → 1.0.1): bug修复
2. **次要版本** (1.0.0 → 1.1.0): 新功能
3. **主要版本** (1.0.0 → 2.0.0): 重大更改
4. **自定义版本**: 手动指定版本号
5. **当前版本**: 使用现有版本号重新发布

## 🐛 故障排除

### 常见问题

#### 1. 构建失败

**问题**: GitHub Actions构建失败
**解决方案**:
- 检查`pyproject.toml`中的依赖是否正确
- 确保`build.py`能在本地正常运行
- 查看Actions日志获取详细错误信息

#### 2. exe文件无法运行

**问题**: 生成的exe在目标机器上无法运行
**解决方案**:
- 检查PyInstaller的`--add-data`参数
- 确保所有必要的资源文件都被包含
- 检查目标机器是否有必要的运行时库

#### 3. 标签推送失败

**问题**: 无法推送标签到GitHub
**解决方案**:
- 检查SSH密钥配置
- 确保有仓库的写权限
- 检查标签是否已存在

### 调试步骤

1. **本地测试**: 先运行`test-build.py`确保本地构建正常
2. **检查日志**: 查看GitHub Actions的详细日志
3. **分步调试**: 可以注释workflow中的部分步骤进行调试
4. **手动触发**: 使用workflow_dispatch手动触发测试

## 🔄 更新工作流

如需修改构建流程，编辑`.github/workflows/build-and-release.yml`：

### 常见修改

1. **更改Python版本**:
   ```yaml
   env:
     PYTHON_VERSION: '3.12'  # 改为所需版本
   ```

2. **添加构建参数**:
   ```yaml
   - name: 构建exe文件
     run: |
       uv run python build.py --additional-param
   ```

3. **修改Release内容**:
   编辑`body:`部分的Markdown内容

## 📚 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [PyInstaller 文档](https://pyinstaller.readthedocs.io/)
- [uv 文档](https://docs.astral.sh/uv/)
- [语义化版本规范](https://semver.org/lang/zh-CN/)

## 🤝 贡献

如果你需要改进自动发布流程：

1. 修改相关脚本或workflow文件
2. 在本地充分测试
3. 提交Pull Request并说明更改原因
4. 等待代码审查和合并

---

## 📞 支持

如果遇到问题：

1. 首先查看本文档的故障排除部分
2. 检查GitHub Actions的运行日志
3. 在项目Issues中搜索类似问题
4. 创建新Issue描述具体问题和错误信息
