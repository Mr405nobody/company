#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诊断定价不匹配问题
帮助用户快速定位问题
"""

from price_table_handler import read_price_excel
from excel_handler import read_purchase_price_excel
from matcher import find_matching_price

print("=" * 70)
print("🔍 诊断定价不匹配问题")
print("=" * 70)

# 获取用户输入
print("\n请回答以下问题：")
print("-" * 70)

# 1. 使用哪个定价表
print("\n1. 您上传的定价表文件名是？")
print("   常见选项：")
print("   a) 结果表格-2.xlsx")
print("   b) 定价表示例.xlsx")
print("   c) 其他文件")
price_file = input("   请输入文件名（或按回车使用 结果表格-2.xlsx）: ").strip()
if not price_file:
    price_file = "结果表格-2.xlsx"

# 2. 使用哪个进价表
print("\n2. 您上传的进价表文件名是？")
print("   常见选项：")
print("   a) 进价表示例.xlsx")
print("   b) 徐水平台10月统计.xls")
print("   c) 其他文件")
purchase_file = input("   请输入文件名（或按回车使用 进价表示例.xlsx）: ").strip()
if not purchase_file:
    purchase_file = "进价表示例.xlsx"

# 3. 订单中的菜品
print("\n3. 请输入您订单中的菜品名称（多个用逗号分隔）")
print("   例如：白萝卜,菠菜,西红柿")
vegetables_input = input("   菜品名称: ").strip()
if not vegetables_input:
    vegetables_input = "白萝卜,菠菜,西红柿"

vegetables = [v.strip() for v in vegetables_input.split(',')]

# 开始诊断
print("\n" + "=" * 70)
print("📊 诊断结果")
print("=" * 70)

# 读取定价表
print(f"\n【步骤1】读取定价表：{price_file}")
try:
    price_table = read_price_excel(price_file)
    print(f"✅ 成功读取 {len(price_table)} 个菜品")
    print(f"   前5个菜品：")
    for i, (name, price) in enumerate(list(price_table.items())[:5]):
        print(f"   {i+1}. {name}: ¥{price}")
except Exception as e:
    print(f"❌ 失败：{e}")
    exit(1)

# 读取进价表
print(f"\n【步骤2】读取进价表：{purchase_file}")
try:
    purchase_table = read_purchase_price_excel(purchase_file)
    print(f"✅ 成功读取 {len(purchase_table)} 个菜品")
    print(f"   前5个菜品：")
    for i, (name, price) in enumerate(list(purchase_table.items())[:5]):
        print(f"   {i+1}. {name}: ¥{price}")
except Exception as e:
    print(f"❌ 失败：{e}")
    exit(1)

# 测试匹配
print(f"\n【步骤3】测试菜品匹配")
print("-" * 70)
print(f"{'订单菜品':20s} | {'定价':10s} | {'进价':10s} | {'状态'}")
print("-" * 70)

all_ok = True
for veg in vegetables:
    # 查找定价
    selling_price = find_matching_price(veg, price_table)
    # 查找进价
    purchase_price = find_matching_price(veg, purchase_table)
    
    # 判断状态
    if selling_price == "000000":
        status = "❌ 定价缺失"
        all_ok = False
    elif purchase_price == "000000":
        status = "⚠️  进价缺失"
        all_ok = False
    else:
        status = "✅ 正常"
    
    print(f"{veg:20s} | ¥{str(selling_price):8s} | ¥{str(purchase_price):8s} | {status}")

# 总结
print("\n" + "=" * 70)
print("📋 诊断总结")
print("=" * 70)

if all_ok:
    print("\n✅ 所有菜品都能正常匹配！")
    print("\n如果GUI程序中还是不匹配，问题是：")
    print("   ⚠️  GUI程序使用的是旧代码（Python缓存问题）")
    print("\n解决方法：")
    print("   1. 关闭GUI窗口")
    print("   2. 运行：rm -rf __pycache__")
    print("   3. 运行：python3 main.py")
    print("   4. 重新上传定价表和进价表")
else:
    print("\n❌ 发现匹配问题！")
    print("\n可能原因：")
    print("   1. 定价表或进价表中缺少该菜品")
    print("   2. 菜品名称不一致（汉字部分需要完全相同）")
    print("\n解决方法：")
    print("   1. 在定价表中添加缺失的菜品")
    print("   2. 检查菜品名称是否一致")
    print("      - 订单：白萝卜 ↔ 定价表：XS-白萝卜 ✅（前缀会自动忽略）")
    print("      - 订单：萝卜 ↔ 定价表：胡萝卜 ❌（汉字不同）")

print("\n" + "=" * 70)

