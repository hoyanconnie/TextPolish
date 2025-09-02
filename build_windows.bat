@echo off
chcp 65001
echo ========================================
echo TextPolish Windows exe 构建工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo 当前Python版本：
python --version
echo.

REM 创建虚拟环境（可选）
echo 创建虚拟环境...
if not exist "venv" (
    python -m venv venv
)
call venv\Scripts\activate.bat
echo 虚拟环境已激活
echo.

REM 安装依赖
echo 安装构建依赖...
pip install --upgrade pip
pip install pyinstaller pyperclip "PyQt6-Fluent-Widgets[full]"
echo.

REM 清理旧文件
echo 清理旧的构建文件...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "*.spec" del /q *.spec
echo.

REM 创建版本信息文件
echo 创建版本信息文件...
(
echo # UTF-8
echo VSVersionInfo^(
echo   ffi=FixedFileInfo^(
echo     filevers=^(0,1,0,0^),
echo     prodvers=^(0,1,0,0^),
echo     mask=0x3f,
echo     flags=0x0,
echo     OS=0x4,
echo     fileType=0x1,
echo     subtype=0x0,
echo     date=^(0, 0^)
echo   ^),
echo   kids=[
echo     StringFileInfo^(
echo       [StringTable^(
echo         u'080404B0',
echo         [StringStruct^(u'CompanyName', u'TextPolish'^),
echo         StringStruct^(u'FileDescription', u'Gemini文本格式修复工具'^),
echo         StringStruct^(u'FileVersion', u'0.1.0'^),
echo         StringStruct^(u'InternalName', u'TextPolish'^),
echo         StringStruct^(u'LegalCopyright', u'Copyright ^(c^) 2025'^),
echo         StringStruct^(u'OriginalFilename', u'TextPolish.exe'^),
echo         StringStruct^(u'ProductName', u'TextPolish - Gemini文本格式修复工具'^),
echo         StringStruct^(u'ProductVersion', u'0.1.0'^)]^)
echo       ]^), 
echo     VarFileInfo^([VarStruct^(u'Translation', [2052, 1200]^)]^)
echo   ]
echo ^)
) > version_info.txt
echo.

REM 使用PyInstaller构建
echo 开始构建TextPolish.exe...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name=TextPolish ^
    --distpath=dist ^
    --workpath=build ^
    --clean ^
    --noconfirm ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=qfluentwidgets ^
    --hidden-import=pyperclip ^
    --version-file=version_info.txt ^
    main.py

if errorlevel 1 (
    echo.
    echo 构建失败！请检查错误信息。
    pause
    exit /b 1
)

REM 检查构建结果
if exist "dist\TextPolish.exe" (
    echo.
    echo ========================================
    echo 🎉 构建成功！
    echo ========================================
    echo.
    echo exe文件位置：%CD%\dist\TextPolish.exe
    for %%A in ("dist\TextPolish.exe") do echo 文件大小：%%~zA bytes ^(%.1f MB^)
    echo.
    echo 使用说明：
    echo 1. dist\TextPolish.exe 就是可执行文件
    echo 2. 双击即可运行，无需安装Python
    echo 3. 可以复制到任何Windows电脑上使用
    echo.
) else (
    echo.
    echo ⚠️  警告：未找到生成的exe文件
    echo 请检查构建过程中是否有错误
    echo.
)

REM 清理临时文件
if exist "version_info.txt" del version_info.txt

echo 构建完成！
pause
