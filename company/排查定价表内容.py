import pandas as pd

# 读取定价表，输出所有菜品名
file_path = './定价/定价.xlsx'
df = pd.read_excel(file_path, header=None)

print('定价表所有菜品名及价格:')
if len(df.columns) >= 4:
    for idx in range(len(df)):
        row = df.iloc[idx]
        if pd.notna(row[0]) and pd.notna(row[1]):
            print(str(row[0]).strip(), row[1])
        if pd.notna(row[2]) and pd.notna(row[3]):
            print(str(row[2]).strip(), row[3])
else:
    for idx in range(len(df)):
        row = df.iloc[idx]
        if pd.notna(row[0]) and pd.notna(row[1]):
            print(str(row[0]).strip(), row[1])
