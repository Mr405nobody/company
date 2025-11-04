#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定价表处理模块 - 支持Excel读取
"""

import pandas as pd


def read_price_excel(file_path):
    """
    读取定价表Excel文件
    支持两种格式：
    1. 标准格式（2列）：菜品 | 价格
    2. 双列格式（4列）：菜品1 | 价格1 | 菜品2 | 价格2
    
    参数:
        file_path (str): Excel文件路径
    
    返回:
        dict: {菜品名: 定价} 的字典
    """
    try:
        # 读取Excel文件（不使用第一行作为表头，以便灵活处理）
        df = pd.read_excel(file_path, header=None)
        
        # 构建字典
        price_table = {}
        
        # 检测是否为4列格式（双列菜品）
        if len(df.columns) >= 4:
            # 双列格式：第0,1列和第2,3列都是菜品-价格对
            # 跳过第一行（可能是表头）
            start_row = 0
            
            # 检测第一行是否为表头
            first_row = df.iloc[0]
            if any(str(val).strip() in ['品名', '菜品', '名称', '单价', '价格', '定价'] for val in first_row if pd.notna(val)):
                start_row = 1
            
            # 读取第一组（第0,1列）
            for index in range(start_row, len(df)):
                row = df.iloc[index]
                
                # 处理第0,1列
                if pd.notna(row[0]) and pd.notna(row[1]):
                    vegetable = str(row[0]).strip()
                    if vegetable and vegetable != 'nan':
                        try:
                            price = float(row[1])
                            price_table[vegetable] = price
                        except (ValueError, TypeError):
                            pass
                
                # 处理第2,3列
                if pd.notna(row[2]) and pd.notna(row[3]):
                    vegetable = str(row[2]).strip()
                    if vegetable and vegetable != 'nan':
                        try:
                            price = float(row[3])
                            price_table[vegetable] = price
                        except (ValueError, TypeError):
                            pass
        
        else:
            # 标准2列格式
            # 读取Excel文件（使用第一行作为表头）
            df = pd.read_excel(file_path)
            
            # 查找菜品和价格列
            vegetable_col = None
            price_col = None
            
            # 尝试查找列名
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['菜品', '名称', '品名', '商品']):
                    vegetable_col = col
                elif any(keyword in col_lower for keyword in ['价格', '单价', '定价', '售价']):
                    price_col = col
            
            # 如果没找到，使用前两列
            if vegetable_col is None:
                vegetable_col = df.columns[0]
            if price_col is None:
                price_col = df.columns[1]
            
            for index, row in df.iterrows():
                vegetable = str(row[vegetable_col]).strip()
                
                # 跳过空行和无效行
                if pd.isna(row[vegetable_col]) or vegetable == '' or vegetable == 'nan':
                    continue
                
                try:
                    price = float(row[price_col])
                    price_table[vegetable] = price
                except (ValueError, TypeError):
                    # 如果价格无法转换为数字，跳过
                    continue
        
        return price_table
    
    except Exception as e:
        raise Exception(f"读取定价表Excel失败: {str(e)}")


if __name__ == "__main__":
    # 测试
    result = read_price_excel("定价表.xlsx")
    print(result)
