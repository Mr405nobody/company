#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字列表解析模块
"""

import re


def parse_text_list(text):
    """
    解析文字列表，提取单位、菜品和数量
    
    参数:
        text (str): 原始文字列表
    
    返回:
        list: 解析后的订单列表，每项包含 {单位, 菜品, 数量}
    """
    orders = []
    lines = text.strip().split('\n')
    
    current_unit = "未指定单位"  # 默认单位
    
    for line in lines:
        line = line.strip()
        
        # 忽略空行
        if not line:
            continue
        
        # 尝试匹配菜品和数量的模式
        # 格式：菜品名 + 数字 + 斤
        match = re.search(r'(.+?)(\d+(?:\.\d+)?)\s*斤', line)
        
        if match:
            # 这是菜品行
            vegetable = match.group(1).strip()
            quantity = float(match.group(2))
            
            # 无论是否有单位，都添加订单（使用默认单位或当前单位）
            orders.append({
                '单位': current_unit,
                '菜品': vegetable,
                '数量': quantity
            })
        else:
            # 这可能是单位名称
            # 如果行中不包含数字和"斤"，则认为是单位名称
            if not re.search(r'\d+(?:\.\d+)?\s*斤', line):
                current_unit = line
    
    return orders


if __name__ == "__main__":
    # 测试
    test_text = """一中五食堂
胡萝卜20斤
尖椒20斤
黄瓜20斤

综合四食堂
胡萝卜20斤
尖椒30斤
西葫芦10斤"""
    
    result = parse_text_list(test_text)
    for order in result:
        print(order)
