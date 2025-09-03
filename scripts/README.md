# TextPolish 发布脚本

这个目录包含了用于自动化发布流程的脚本。

## 📁 脚本说明

### `release.py`
版本发布脚本，用于：
- 自动更新版本号
- 创建Git标签
- 推送到GitHub触发自动构建

**使用方法**:
```powershell
uv run python scripts/release.py
```

### `test-build.py`
本地构建测试脚本，用于：
- 模拟GitHub Actions构建环境
- 本地验证构建流程
- 确保发布前构建正常

**使用方法**:
```powershell
uv run python scripts/test-build.py
```

## 🚀 发布流程

1. **开发完成**: 确保所有功能开发和测试完成
2. **本地测试**: 运行`test-build.py`验证构建
3. **版本发布**: 运行`release.py`创建新版本
4. **自动构建**: GitHub Actions自动构建并发布

## ⚠️ 注意事项

- 发布前确保工作区干净（无未提交更改）
- 建议先运行本地测试确保构建正常
- 版本号遵循语义化版本规范（x.y.z）
- 推送标签后无法轻易撤销，请谨慎操作
