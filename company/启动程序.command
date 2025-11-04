#!/bin/bash
cd "$(dirname "$0")"
echo "正在启动蔬菜公司 Excel 助手..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.7 或更高版本"
    exit 1
fi

# 检查依赖
echo "检查依赖包..."
python3 -c "import pandas, openpyxl, tencentcloud" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖包，正在安装..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动运行: pip3 install -r requirements.txt"
        exit 1
    fi
fi

echo "✓ 依赖检查完成"
echo ""
echo "🚀 启动程序..."
python3 main.py
