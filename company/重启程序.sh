#!/bin/bash
# 重启程序脚本

echo "🔄 正在重启蔬菜公司Excel助手..."
echo ""

# 清理Python缓存
echo "1. 清理Python缓存..."
rm -rf __pycache__
echo "   ✅ 缓存已清理"

# 关闭可能在运行的程序
echo ""
echo "2. 检查运行中的程序..."
pkill -f "python.*main.py" 2>/dev/null && echo "   ✅ 已关闭旧程序" || echo "   ℹ️  没有运行中的程序"

# 启动新程序
echo ""
echo "3. 启动程序..."
python3 main.py


