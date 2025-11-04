#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit 前端：将现有功能封装为网页应用

主要功能：
- 输入/粘贴订单文字并解析
- 上传定价表（Excel）
- 上传进价表（Excel）
- 生成并下载利润表 Excel

说明：尽量复用仓库内的模块（parser, price_table_handler, excel_handler, profit_calculator）
"""

import streamlit as st
import io
import tempfile
import os
from parser import parse_text_list
from price_table_handler import read_price_excel
from excel_handler import read_purchase_price_excel
from profit_calculator import calculate_profit_and_generate_excel

# OCR 模块已移除


def ensure_session_state():
    if 'text_data' not in st.session_state:
        st.session_state['text_data'] = ''
    if 'price_table' not in st.session_state:
        st.session_state['price_table'] = {}
    if 'purchase_table' not in st.session_state:
        st.session_state['purchase_table'] = {}


def sidebar_instructions():
    st.sidebar.title('说明')
    st.sidebar.markdown('''
    - 将仓库原有功能迁移到网页端
    - 定价表请上传 Excel
    - 进价表请上传 Excel
    - 生成的利润表可直接下载
    ''')


def page_input_orders():
    st.header('1. 输入/粘贴订单文字')
    st.markdown('请按原有格式输入：单位名 单独一行，后续为菜品+数量+斤')
    text = st.text_area('订单文本', value=st.session_state.get('text_data', ''), height=240)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('解析文字'):
            st.session_state['text_data'] = text
            try:
                orders = parse_text_list(text)
                st.success(f'解析完成：共 {len(orders)} 条记录')
                st.experimental_set_query_params(parsed=len(orders))
                st.session_state['last_orders'] = orders
            except Exception as e:
                st.error(f'解析失败：{e}')
    with col2:
        if st.button('清空'):
            st.session_state['text_data'] = ''
            st.session_state['last_orders'] = []
            st.experimental_rerun()

    if st.session_state.get('last_orders'):
        st.write('示例解析（前20条）：')
        import pandas as pd
        df = pd.DataFrame(st.session_state['last_orders'])
        st.dataframe(df.head(20))


def page_price_table():
    st.header('2. 定价表（Excel）')
    st.markdown('请上传定价表 Excel 文件。')
    
    excel_file = st.file_uploader('上传定价表 Excel', type=['xlsx', 'xls'])

    if excel_file is not None:
        with st.spinner('正在读取 Excel...'):
            try:
                # pandas 能接受 BytesIO
                bytes_io = io.BytesIO(excel_file.read())
                price_table = read_price_excel(bytes_io)
                st.session_state['price_table'] = price_table
                st.success(f'定价表加载完成，共 {len(price_table)} 个菜品')
            except Exception as e:
                st.error(f'读取 Excel 失败：{e}')

    if st.session_state.get('price_table'):
        import pandas as pd
        df = pd.DataFrame(list(st.session_state['price_table'].items()), columns=['菜品', '定价'])
        st.dataframe(df.head(200))


def page_purchase_table():
    st.header('3. 进价表（上传 Excel）')
    purchase_file = st.file_uploader('上传进价表 Excel', type=['xlsx', 'xls'], key='purchase')
    if purchase_file is not None:
        with st.spinner('正在读取进价表...'):
            try:
                bytes_io = io.BytesIO(purchase_file.read())
                purchase_table = read_purchase_price_excel(bytes_io)
                st.session_state['purchase_table'] = purchase_table
                st.success(f'进价表加载完成，共 {len(purchase_table)} 个菜品')
            except Exception as e:
                st.error(f'读取进价表失败：{e}')

    if st.session_state.get('purchase_table'):
        import pandas as pd
        df = pd.DataFrame(list(st.session_state['purchase_table'].items()), columns=['菜品', '进价'])
        st.dataframe(df.head(200))


def page_generate():
    st.header('4. 生成并下载利润表')
    st.markdown('请先在“输入订单”“定价表”“进价表”三个步骤完成数据准备，然后执行生成。')
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button('生成利润表'):
            orders = st.session_state.get('last_orders') or parse_text_list(st.session_state.get('text_data', ''))
            price_table = st.session_state.get('price_table', {})
            purchase_table = st.session_state.get('purchase_table', {})

            if not orders:
                st.error('订单为空，请先解析或粘贴订单')
            elif not price_table:
                st.error('定价表为空，请上传图片或 Excel')
            elif not purchase_table:
                st.error('进价表为空，请上传进价 Excel')
            else:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
                        tmp_path = tmp.name
                    total_profit = calculate_profit_and_generate_excel(orders, price_table, purchase_table, tmp_path)
                    st.success(f'利润表生成成功，总利润：¥{total_profit:.2f}\n 可点击下方按钮下载')
                    with open(tmp_path, 'rb') as f:
                        data = f.read()
                    st.download_button('下载利润表（Excel）', data, file_name='利润表.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                    # 保留文件一段时间，让用户下载
                except Exception as e:
                    st.error(f'生成失败：{e}')
    with col2:
        st.markdown('开发者提示：')
        st.write('- 可以考虑备份生成的利润表。')


def main():
    st.set_page_config(page_title='蔬菜公司 Excel 助手', layout='wide')
    ensure_session_state()
    sidebar_instructions()

    st.title('🥬 蔬菜公司 Excel 助手（Web）')

    page = st.sidebar.selectbox('选择功能', ['输入订单', '定价表', '进价表', '生成与下载'])

    if page == '输入订单':
        page_input_orders()
    elif page == '定价表':
        page_price_table()
    elif page == '进价表':
        page_purchase_table()
    elif page == '生成与下载':
        page_generate()


if __name__ == '__main__':
    main()
