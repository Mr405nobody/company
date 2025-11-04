#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel处理模块 - 读取进价表
"""

import pandas as pd


def read_purchase_price_excel(file_path):
    """
    读取进价表Excel文件
    
    参数:
        file_path (str): Excel文件路径
    
    返回:
        dict: {菜品名: 进价} 的字典
    """
    try:
        # 读取Excel文件（不使用第一行作为表头，以便灵活处理）
        df = pd.read_excel(file_path, header=None)
        purchase_table = {}

        # 检测是否为4列格式（双列菜品）
        if len(df.columns) >= 4:
            start_row = 0
            first_row = df.iloc[0]
            if any(str(val).strip() in ['品名', '菜品', '名称', '单价', '价格', '定价', '进价', '成本'] for val in first_row if pd.notna(val)):
                start_row = 1

            for index in range(start_row, len(df)):
                row = df.iloc[index]
                # 处理第0,1列
                if pd.notna(row[0]) and pd.notna(row[1]):
                    vegetable = str(row[0]).strip()
                    if vegetable and vegetable != 'nan':
                        try:
                            price = float(row[1])
                            purchase_table[vegetable] = price
                        except (ValueError, TypeError):
                            pass
                # 处理第2,3列
                if pd.notna(row[2]) and pd.notna(row[3]):
                    vegetable = str(row[2]).strip()
                    if vegetable and vegetable != 'nan':
                        try:
                            price = float(row[3])
                            purchase_table[vegetable] = price
                        except (ValueError, TypeError):
                            pass
        else:
            # 标准2列格式
            df = pd.read_excel(file_path)
            vegetable_col = None
            price_col = None
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['菜品', '名称', '品名', '商品']):
                    vegetable_col = col
                elif any(keyword in col_lower for keyword in ['价格', '单价', '进价', '成本']):
                    price_col = col
            if vegetable_col is None:
                vegetable_col = df.columns[0]
            if price_col is None:
                price_col = df.columns[1]
            for index, row in df.iterrows():
                vegetable = str(row[vegetable_col]).strip()
                if pd.isna(row[vegetable_col]) or vegetable == '' or vegetable == 'nan':
                    continue
                try:
                    price = float(row[price_col])
                    purchase_table[vegetable] = price
                except (ValueError, TypeError):
                    continue
        return purchase_table
    except Exception as e:
        raise Exception(f"读取Excel失败: {str(e)}")


if __name__ == "__main__":
    # 测试
    result = read_purchase_price_excel("进价表.xlsx")
    print(result)
