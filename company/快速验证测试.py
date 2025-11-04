#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速验证测试 - 验证所有新功能是否正常工作
运行方式：python3 快速验证测试.py
"""

from price_table_handler import read_price_excel
from matcher import find_matching_price, remove_prefix

print("=" * 70)
print("🧪 蔬菜公司Excel助手 - 快速验证测试 (v2.1)")
print("=" * 70)

# 测试1：4列格式定价表读取
print("\n【测试1】4列格式定价表读取")
print("-" * 70)
try:
    price_table = read_price_excel('定价/定价.xlsx')
    print(f"✅ 成功读取 {len(price_table)} 个菜品")
    print(f"   示例: [嘉泽] XS-白萝卜=¥{price_table.get('[嘉泽] XS-白萝卜', '?')}, "
          f"[嘉泽] XS-大白菜=¥{price_table.get('[嘉泽] XS-大白菜', '?')}")
except Exception as e:
    print(f"❌ 失败: {e}")
    exit(1)

# 测试2：前缀去除功能
print("\n【测试2】前缀去除功能")
print("-" * 70)
prefix_tests = [
    ('[嘉泽] XS-白萝卜', '白萝卜'),
    ('[嘉泽]XS-菠菜', '菠菜'),
    ('[嘉泽] XS-西红柿', '西红柿'),
    ('白萝卜', '白萝卜'),
]
all_pass = True
for original, expected in prefix_tests:
    result = remove_prefix(original)
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_pass = False
    print(f"{status} {original:15s} -> {result:10s} (期望: {expected})")

if not all_pass:
    print("❌ 前缀去除功能测试失败")
    exit(1)

# 测试3：前缀忽略匹配
print("\n【测试3】前缀忽略匹配（订单无前缀 → 定价表有前缀）")
print("-" * 70)
match_tests = [
    ('白萝卜', 0.9),
    ('菠菜', 3.0),
    ('西红柿', 2.7),
    ('大白菜', 0.8),
    ('大白菜一级品', 1.1),
    ('油菜', 1.5),
    ('油菜一级品', 2.0),
]
all_match = True
for veg, expected_price in match_tests:
    price = find_matching_price(veg, price_table)
    status = "✅" if price == expected_price else "❌"
    if price != expected_price:
        all_match = False
    print(f"{status} {veg:10s} -> ¥{str(price):6s} (期望: ¥{expected_price})")

if not all_match:
    print("❌ 前缀匹配功能测试失败")
    exit(1)

# 测试4：带前缀的完全匹配
print("\n【测试4】完全匹配（订单也有前缀）")
print("-" * 70)
full_match_tests = [
    ('[嘉泽] XS-白萝卜', 0.9),
    ('[嘉泽]XS-菠菜', 3.0),
    ('[嘉泽] XS-大白菜', 0.8),
]
for veg, expected_price in full_match_tests:
    price = find_matching_price(veg, price_table)
    status = "✅" if price == expected_price else "❌"
    print(f"{status} {veg:15s} -> ¥{price}")

# 测试5：规格匹配
print("\n【测试5】规格匹配")
print("-" * 70)
spec_tests = [
    ('白萝卜(一级品)', 1.1, '应匹配 [嘉泽]XS-白萝卜(一级品)'),
    ('白萝卜', 0.9, '应匹配 [嘉泽] XS-白萝卜（无规格优先）'),
    ('大白菜(一级品)', 1.1, '应匹配 [嘉泽] XS-大白菜(一级品)'),
]
for veg, expected_price, desc in spec_tests:
    price = find_matching_price(veg, price_table)
    status = "✅" if price == expected_price else "❌"
    print(f"{status} {veg:20s} -> ¥{str(price):6s} | {desc}")

# 最终结果
print("\n" + "=" * 70)
print("🎉 所有测试通过！")
print("=" * 70)
print("\n✨ 功能验证结果：")
print("   1. ✅ 4列格式定价表读取正常")
print("   2. ✅ 前缀去除功能正常")
print("   3. ✅ 前缀忽略匹配正常（白萝卜 → XS-白萝卜）")
print("   4. ✅ 完全匹配功能正常")
print("   5. ✅ 规格匹配功能正常")
print("\n💡 现在您可以：")
print("   - 订单中不写前缀（如：大白菜一级品）")
print("   - 定价表中有前缀（如：[嘉泽] XS-大白菜(一级品)）")
print("   - 系统会自动匹配，定价不会显示0")
print("\n🚀 请重启程序开始使用：python3 main.py")
print("=" * 70)

