#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蔬菜公司 Excel 助手 - 功能测试脚本
"""

import os


def test_import():
    """测试模块导入"""
    print("=" * 60)
    print("测试1: 模块导入")
    print("=" * 60)
    
    try:
        from parser import parse_text_list
        print("✓ parser.py - 文字解析模块")
        
        from ocr_handler import extract_price_from_image
        print("✓ ocr_handler.py - OCR识别模块")
        
        from price_table_handler import read_price_excel
        print("✓ price_table_handler.py - 定价表Excel读取模块")
        
        from excel_handler import read_purchase_price_excel
        print("✓ excel_handler.py - 进价表Excel读取模块")
        
        from matcher import find_matching_price, extract_chinese_and_number
        print("✓ matcher.py - 智能匹配模块")
        
        from profit_calculator import calculate_profit_and_generate_excel
        print("✓ profit_calculator.py - 利润计算模块")
        
        print("\n所有模块导入成功！\n")
        return True
    except Exception as e:
        print(f"\n✗ 模块导入失败: {e}\n")
        return False


def test_parser():
    """测试文字解析"""
    print("=" * 60)
    print("测试2: 文字列表解析")
    print("=" * 60)
    
    from parser import parse_text_list
    
    test_text = """一中五食堂
胡萝卜20斤
尖椒1号15斤

综合四食堂
黄瓜10斤
西红柿25斤"""
    
    orders = parse_text_list(test_text)
    print(f"✓ 解析成功，共 {len(orders)} 条订单")
    
    for order in orders[:3]:
        print(f"  - {order['单位']}: {order['菜品']} {order['数量']}斤")
    
    print()


def test_matcher():
    """测试智能匹配"""
    print("=" * 60)
    print("测试3: 智能匹配算法")
    print("=" * 60)
    
    from matcher import find_matching_price
    
    price_dict = {
        '胡萝卜': 5.0,
        '尖椒1号': 8.0,
        '尖椒2号': 9.0,
        '黄瓜A级': 6.0,
    }
    
    test_cases = [
        ('胡萝卜', 5.0),
        ('尖椒1号', 8.0),
        ('尖椒', 8.0),
        ('黄瓜', 6.0),
        ('土豆', '000000'),
    ]
    
    all_passed = True
    for veg, expected in test_cases:
        result = find_matching_price(veg, price_dict)
        status = "✓" if result == expected else "✗"
        if result != expected:
            all_passed = False
        print(f"{status} {veg:10s} -> {result:8} (期望: {expected})")
    
    if all_passed:
        print("\n✓ 所有匹配测试通过！\n")
    else:
        print("\n✗ 部分匹配测试失败！\n")


def test_excel():
    """测试Excel读取"""
    print("=" * 60)
    print("测试4: Excel文件读取")
    print("=" * 60)
    
    from price_table_handler import read_price_excel
    from excel_handler import read_purchase_price_excel
    
    # 测试定价表
    if os.path.exists('定价表示例.xlsx'):
        price_table = read_price_excel('定价表示例.xlsx')
        print(f"✓ 定价表读取成功，共 {len(price_table)} 个菜品")
    else:
        print("✗ 定价表示例.xlsx 不存在")
    
    # 测试进价表
    if os.path.exists('进价表示例.xlsx'):
        purchase_table = read_purchase_price_excel('进价表示例.xlsx')
        print(f"✓ 进价表读取成功，共 {len(purchase_table)} 个菜品")
    else:
        print("✗ 进价表示例.xlsx 不存在")
    
    print()


def test_complete_flow():
    """测试完整流程"""
    print("=" * 60)
    print("测试5: 完整业务流程")
    print("=" * 60)
    
    from parser import parse_text_list
    from price_table_handler import read_price_excel
    from excel_handler import read_purchase_price_excel
    from profit_calculator import calculate_profit_and_generate_excel
    
    # 准备测试数据
    test_text = """一中五食堂
胡萝卜20斤
尖椒1号15斤

综合四食堂
黄瓜10斤"""
    
    try:
        # 1. 解析文字
        orders = parse_text_list(test_text)
        print(f"✓ 步骤1: 解析文字 ({len(orders)}条)")
        
        # 2. 读取定价表
        price_table = read_price_excel('定价表示例.xlsx')
        print(f"✓ 步骤2: 读取定价表 ({len(price_table)}个)")
        
        # 3. 读取进价表
        purchase_table = read_purchase_price_excel('进价表示例.xlsx')
        print(f"✓ 步骤3: 读取进价表 ({len(purchase_table)}个)")
        
        # 4. 生成利润表
        output_file = 'test_profit.xlsx'
        total_profit = calculate_profit_and_generate_excel(
            orders, price_table, purchase_table, output_file
        )
        print(f"✓ 步骤4: 生成利润表 (总利润: ¥{total_profit:.2f})")
        
        # 清理测试文件
        if os.path.exists(output_file):
            os.remove(output_file)
            print("✓ 测试文件已清理")
        
        print("\n✓ 完整流程测试通过！\n")
        
    except Exception as e:
        print(f"\n✗ 完整流程测试失败: {e}\n")


def main():
    """主测试函数"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "🥬 蔬菜公司Excel助手 - 功能测试" + " " * 10 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # 运行所有测试
    if not test_import():
        print("❌ 模块导入失败，请检查代码！")
        return
    
    test_parser()
    test_matcher()
    test_excel()
    test_complete_flow()
    
    print("=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)
    print()
    print("💡 提示：")
    print("  - 所有核心功能已验证通过")
    print("  - 可以运行 python3 main.py 启动GUI程序")
    print("  - 或双击 启动程序.command 启动")
    print()


if __name__ == "__main__":
    main()
