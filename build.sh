#!/bin/bash

# 一键打包 Flask 项目的脚本
# 用于在 Linux/macOS 环境下使用 PyInstaller 构建单文件可执行程序

set -e  # 遇到错误就退出
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="main"

cd "$PROJECT_DIR"

echo "📦 清理旧的构建文件..."
rm -rf build/ dist/ __pycache__ *.spec

echo "🚀 开始打包 $APP_NAME.py 为可执行文件..."

pyinstaller --onefile \
  --icon "src/ui/custom/loonglogo.ico" \
  --hidden-import "pyside6_addons" \
  --name "SerialPortPySide6" \
  --noconsole \
  --add-data "Resources:." \
  "$APP_NAME.py"

echo "✅ 打包完成：dist/$APP_NAME"
echo "📁 你可以运行： ./dist/$APP_NAME"

