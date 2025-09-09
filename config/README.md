# 📁 配置文件说明

## 配置文件结构

### `app_config.json` - 统一应用配置文件

这是合并后的统一配置文件，包含了应用程序的所有默认设置。

#### 配置文件结构

```json
{
  "app_info": {
    "name": "TextPolish",
    "version": "2.0.0", 
    "description": "Gemini文本格式修复工具"
  },
  "ui_framework": {
    "QFluentWidgets": {
      "ThemeColor": "#ff009faa",
      "ThemeMode": "Dark"
    }
  },
  "default_user_config": {
    "h1": { "style": {...}, "patterns": [...] },
    "h2": { "style": {...}, "patterns": [...] },
    "h3": { "style": {...}, "patterns": [...] },
    "normal": { "style": {...}, "patterns": [...] },
    "special_format": { "style": {...}, "patterns": [...] }
  },
  "default_ui_settings": {
    "enable_h1": true,
    "enable_h2": true,
    "enable_h3": true,
    "enable_special": true
  }
}
```

#### 各部分说明

1. **`app_info`**: 应用程序基本信息
2. **`ui_framework`**: UI框架配置（QFluentWidgets主题设置）
3. **`default_user_config`**: 默认用户配置（样式、正则表达式）
4. **`default_ui_settings`**: 默认界面设置（标题级别开关）

## 配置加载优先级

### 1. 用户配置优先
```
程序启动 → 检查用户配置 (/home/user/.config/TextPolish/TextPolish.conf)
          ↓ 如果存在
          加载用户配置 ✅
```

### 2. 默认配置备用
```
程序启动 → 用户配置不存在
          ↓
          加载 app_config.json 中的 default_user_config ✅
          ↓
          保存为用户配置
```

### 3. 代码配置兜底
```
app_config.json 不存在或损坏
          ↓
          使用代码中硬编码的默认配置 ✅
```

## 配置修改流程

### 用户修改配置
1. **通过界面修改** → 实时保存到用户配置文件
2. **导入配置文件** → 覆盖用户配置
3. **重置为默认** → 从 `app_config.json` 重新加载

### 开发者修改默认配置
1. **编辑 `app_config.json`** → 修改默认设置
2. **用户重置配置** → 应用新的默认设置

## 与旧配置文件的对比

### ❌ 旧的配置结构
```
config/config.json         # QFluentWidgets配置
config_backup.json          # 用户配置备份
```

### ✅ 新的配置结构  
```
config/app_config.json      # 统一配置文件
```

## 优势

1. **统一管理**: 所有配置在一个文件中
2. **结构清晰**: 分模块组织，易于理解和维护
3. **扩展性好**: 可以轻松添加新的配置项
4. **版本管理**: 包含应用信息，便于版本控制
5. **主题集成**: UI框架配置与应用配置统一管理

## 配置项说明

### 样式配置 (style)
- `font_family`: 字体名称
- `font_size`: 字号（如："16.0000pt"）
- `font_kerning`: 字符间距
- `font_weight`: 字重（"normal"/"bold"）
- `alignment`: 对齐方式（"left"/"center"/"right"/"justify"）
- `text_indent`: 首行缩进（如："36.0000pt"）

### 正则表达式 (patterns)
- `pattern`: 正则表达式字符串
- `name`: 规则名称
- `enabled`: 是否启用
- `description`: 规则描述

### 界面设置 (ui_settings)
- `enable_h1`: 是否启用一级标题
- `enable_h2`: 是否启用二级标题  
- `enable_h3`: 是否启用三级标题
- `enable_special`: 是否启用特殊格式
