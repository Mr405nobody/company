import difflib
def fuzzy_find_price(vegetable, price_dict, threshold=0.6):
    """
    更强的模糊匹配：
    1. 先用find_matching_price（原有规则）
    2. 若找不到，再用包含关系和相似度（Levenshtein/SequenceMatcher）
    3. threshold为相似度阈值（0~1）
    """
    price = find_matching_price(vegetable, price_dict)
    if price != "000000":
        return price

    # 包含关系（如“萝卜”能匹配“胡萝卜”）
    for key, value in price_dict.items():
        if vegetable in key or key in vegetable:
            return value

    # Levenshtein/SequenceMatcher相似度
    best_score = 0
    best_value = None
    for key, value in price_dict.items():
        score = difflib.SequenceMatcher(None, vegetable, key).ratio()
        if score > best_score:
            best_score = score
            best_value = value
    if best_score >= threshold:
        return best_value
    return "000000"
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
菜品匹配模块 - 汉字完全匹配，编号模糊匹配，自动忽略前缀
"""

import re


def remove_prefix(text):
    """
    去除菜品名称的常见前缀
    
    支持的前缀格式：
    - [嘉泽] XS-、[嘉泽]XS-、[供应商] XS- 等
    - XS-、JX-、JS-、XY-、YS- 等
    - [供应商] 等括号前缀
    
    参数:
        text (str): 菜品名称
    
    返回:
        str: 去除前缀后的菜品名称
    """
    # 去除 [供应商] 前缀
    text = re.sub(r'^\[[^\]]+\]\s*', '', text)
    
    # 去除字母-前缀（XS-、JX-等）
    prefix_pattern = r'^[A-Z]{2,3}-'
    text = re.sub(prefix_pattern, '', text, flags=re.IGNORECASE)
    
    return text.strip()


def extract_chinese_and_number(text):
    """
    从文本中提取汉字部分和编号部分
    
    规则：
    - 汉字部分：开头的连续汉字（菜品主名）
    - 编号部分：后续的所有字符（数字、字母、号级、规格等）
    
    参数:
        text (str): 菜品名称
    
    返回:
        tuple: (汉字部分, 编号部分)
    """
    # 匹配开头的连续汉字（菜品主名）
    match = re.match(r'^([\u4e00-\u9fff]+)', text)
    
    if match:
        chinese = match.group(1)
        # 剩余部分作为编号（包括规格信息）
        number = text[len(chinese):]
    else:
        # 没有汉字开头
        chinese = ''
        number = text
    
    return chinese, number


def normalize_specification(text):
    """
    标准化规格信息，处理不同的规格表示方式
    
    参数:
        text (str): 包含规格的文本
    
    返回:
        str: 标准化后的规格文本
    """
    if not text:
        return ''
    
    # 先处理已经带括号的情况，避免重复括号
    # 将 "一级品" 标准化为 "(一级品)"，但避免重复括号
    if not text.startswith('(') and not text.endswith(')'):
        text = re.sub(r'一级品', '(一级品)', text)
        text = re.sub(r'二级品', '(二级品)', text)
        text = re.sub(r'三级品', '(三级品)', text)
        
        # 将其他规格也标准化为括号格式
        text = re.sub(r'(特级|优级|普通)', r'(\1)', text)
    
    return text.strip()


def find_matching_price(vegetable, price_dict):
    """
    查找菜品价格 - 汉字完全匹配，编号模糊匹配，自动忽略前缀，支持规格匹配
    
    匹配规则：
    1. 优先完全匹配（包括前缀）
    2. 去除前缀后匹配（订单"白萝卜" 可匹配 定价表"XS-白萝卜"）
    3. 汉字部分必须完全一致
    4. 编号部分可以模糊匹配或不匹配
    5. 支持规格匹配（"大白菜一级品" 可匹配 "大白菜(一级品)"）
    6. 优先级：完全匹配 > 去前缀完全匹配 > 汉字+编号匹配 > 仅汉字匹配
    
    参数:
        vegetable (str): 菜品名称
        price_dict (dict): 价格字典
    
    返回:
        float or str: 价格或"000000"
    """
    # 去除空格
    vegetable_clean = vegetable.replace(' ', '').replace('　', '')
    
    # 1. 精确匹配（完全一致，包括前缀）
    if vegetable_clean in price_dict:
        return price_dict[vegetable_clean]
    
    # 2. 去除前缀后再尝试完全匹配
    vegetable_no_prefix = remove_prefix(vegetable_clean)
    for key, value in price_dict.items():
        key_no_prefix = remove_prefix(key.replace(' ', '').replace('　', ''))
        if vegetable_no_prefix == key_no_prefix:
            return value
    
    # 3. 标准化规格信息后再尝试匹配
    veg_normalized = normalize_specification(vegetable_no_prefix)
    for key, value in price_dict.items():
        key_no_prefix = remove_prefix(key.replace(' ', '').replace('　', ''))
        key_normalized = normalize_specification(key_no_prefix)
        if veg_normalized == key_normalized:
            return value
    
    # 4. 提取订单菜品的汉字和编号（去除前缀后）
    veg_chinese, veg_number = extract_chinese_and_number(vegetable_no_prefix)
    
    if not veg_chinese:
        # 如果没有汉字，无法匹配
        return "000000"
    
    # 5. 汉字+编号匹配（忽略前缀）
    candidates = []
    
    for key, value in price_dict.items():
        key_clean = key.replace(' ', '').replace('　', '')
        key_no_prefix = remove_prefix(key_clean)
        key_chinese, key_number = extract_chinese_and_number(key_no_prefix)
        
        # 汉字部分必须完全一致
        if veg_chinese == key_chinese:
            # 标准化规格信息进行匹配
            veg_spec_normalized = normalize_specification(veg_number)
            key_spec_normalized = normalize_specification(key_number)
            
            # 计算编号匹配度
            if veg_spec_normalized == key_spec_normalized:
                # 完全匹配（汉字+编号都一致，包括都为空的情况）
                candidates.append((4, value))
            elif veg_number == key_number:
                # 原始编号完全匹配
                candidates.append((3, value))
            elif veg_number and key_number:
                # 两者都有编号，检查包含关系
                if (veg_number in key_number or key_number in veg_number or 
                    veg_spec_normalized in key_spec_normalized or 
                    key_spec_normalized in veg_spec_normalized):
                    # 编号部分包含匹配
                    candidates.append((2, value))
                else:
                    # 汉字匹配但编号不匹配
                    candidates.append((1, value))
            else:
                # 一方有编号一方没有，或都没有编号
                # 仅汉字匹配
                candidates.append((1, value))
        
        # 汉字部分包含关系匹配（如"白菜"匹配"大白菜"）
        elif (veg_chinese != key_chinese and 
              (veg_chinese in key_chinese or key_chinese in veg_chinese) and
              len(veg_chinese) >= 2 and len(key_chinese) >= 2):
            # 优先选择没有规格的菜品（更通用）
            if not key_number or key_number.strip() == '':
                candidates.append((0.5, value))  # 低优先级：包含匹配+无规格
            else:
                candidates.append((0.3, value))  # 更低优先级：包含匹配+有规格
    
    # 如果有候选，返回匹配度最高的
    if candidates:
        # 按匹配度排序，取最高的
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    
    # 找不到匹配
    return "000000"


def find_matching_cost_price(vegetable, cost_dict):
    """
    查找菜品进价 - 优先精确匹配，其次汉字部分匹配（忽略规格）
    
    匹配规则：
    1. 优先精确匹配（去除前缀并标准化规格后）
    2. 如果未找到，则提取订单菜品的汉字部分，尝试匹配进价表中菜品的汉字部分（忽略规格）
       例如：订单"大白菜一级品"可以匹配进价表中的"大白菜"
    
    参数:
        vegetable (str): 菜品名称
        cost_dict (dict): 进价字典 {菜品名: 进价}
    
    返回:
        float or str: 进价或"000000"
    """
    # 去除空格
    vegetable_clean = vegetable.replace(' ', '').replace('　', '')
    
    # 1. 先尝试使用原有的精确匹配逻辑
    price = find_matching_price(vegetable, cost_dict)
    if price != "000000":
        return price
    
    # 2. 如果精确匹配失败，尝试汉字部分匹配（忽略规格）
    vegetable_no_prefix = remove_prefix(vegetable_clean)
    vegetable_normalized = normalize_specification(vegetable_no_prefix)
    veg_chinese, _ = extract_chinese_and_number(vegetable_normalized)
    
    if not veg_chinese:
        return "000000"
    
    # 3. 在进价表中查找汉字部分匹配的菜品
    candidates = []
    for key, value in cost_dict.items():
        key_clean = key.replace(' ', '').replace('　', '')
        key_no_prefix = remove_prefix(key_clean)
        key_normalized = normalize_specification(key_no_prefix)
        key_chinese, key_number = extract_chinese_and_number(key_normalized)
        
        # 汉字部分完全一致
        if veg_chinese == key_chinese:
            # 优先选择没有规格的菜品（更通用）
            if not key_number or key_number.strip() == '':
                candidates.append((2, value))  # 高优先级：无规格
            else:
                candidates.append((1, value))  # 低优先级：有规格
        
        # 汉字部分包含关系匹配（如"大白菜"匹配"白菜"）
        elif (veg_chinese != key_chinese and 
              (veg_chinese in key_chinese or key_chinese in veg_chinese) and
              len(veg_chinese) >= 2 and len(key_chinese) >= 2):
            # 优先选择没有规格的菜品（更通用）
            if not key_number or key_number.strip() == '':
                candidates.append((1.5, value))  # 中等优先级：包含匹配+无规格
            else:
                candidates.append((0.5, value))  # 低优先级：包含匹配+有规格
    
    # 如果有候选，返回优先级最高的
    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    
    # 找不到匹配
    return "000000"


if __name__ == "__main__":
    # 测试
    price_dict = {
        '胡萝卜': 5.0,
        '尖椒1号': 8.0,
        '尖椒2号': 9.0,
        '黄瓜A级': 6.0,
        '西红柿': 4.0
    }
    
    test_cases = [
        '胡萝卜',      # 完全匹配 -> 5.0
        '尖椒1号',     # 完全匹配 -> 8.0
        '尖椒',        # 汉字匹配 -> 8.0或9.0（第一个）
        '尖椒2号',     # 完全匹配 -> 9.0
        '黄瓜A级',     # 完全匹配 -> 6.0
        '黄瓜',        # 汉字匹配 -> 6.0
        '茄子',        # 无匹配 -> 000000
    ]
    
    for veg in test_cases:
        price = find_matching_price(veg, price_dict)
        print(f"{veg:10s} -> {price}")
