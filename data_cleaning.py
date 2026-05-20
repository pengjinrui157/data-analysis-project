"""
数据清洗脚本
处理：重复列、重复行、异常值（0或负）、逻辑错误（成本>销售额）
"""

import pandas as pd
import time

start = time.time()

#  1. 读取数据 
print("正在读取Excel文件...")
df = pd.read_excel("公司商品销售表_用例.xlsx", sheet_name="组件")
print(f"原始数据形状: {df.shape}")

#  2. 处理重复列（两列“数量”） 
if "数量.1" in df.columns:
    print("发现重复列 '数量.1'，删除该列")
    df = df.drop(columns=["数量.1"])
# 重命名保留的“数量”列
df.rename(columns={"数量": "销售数量"}, inplace=True)

#  3. 删除完全重复的行 
before_rows = len(df)
df = df.drop_duplicates()
print(f"删除重复行: 删除了 {before_rows - len(df)} 行")

#  4. 删除异常值（销售额/成本额/毛利额 <=0） 
df = df[df["销售额"] > 0]
df = df[df["成本额"] > 0]
df = df[df["毛利额"] > 0]   # 负毛利和零毛利都删除

#  5. 逻辑校验：销售额必须大于成本额 
df = df[df["销售额"] > df["成本额"]]
print(f"删除异常值后剩余行数: {len(df)}")

#  6. 删除商品名称为空的行（如果有） 
if df["商品名称"].isnull().sum() > 0:
    df = df.dropna(subset=["商品名称"])
    print("已删除商品名称为空的行")

#  7. 增加利润率字段 
df["利润率"] = (df["毛利额"] / df["销售额"]) * 100

#  8. 日期处理 
df["销售日期"] = pd.to_datetime(df["销售日期"])
df["月份"] = df["销售日期"].dt.month

#  9. 保存清洗后的数据 
output_file = "cleaned_sales_data.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"\n清洗完成，保存为: {output_file}")
print(f"最终数据形状: {df.shape}")
print(f"耗时: {time.time() - start:.2f} 秒")