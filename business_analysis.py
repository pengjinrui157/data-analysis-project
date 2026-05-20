"""
业务分析脚本
生成:整体KPI、月度趋势、商品类别、省份排名、帕累托图、高利润商品
"""

import pandas as pd
import matplotlib.pyplot as plt

# 设置中文显示（Windows）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取清洗后的数据
df = pd.read_csv("cleaned_sales_data.csv", encoding="utf-8-sig")
print(f"数据加载成功，共 {len(df)} 行")

# 整体KPI
total_sales = df["销售额"].sum()
total_cost = df["成本额"].sum()
total_profit = df["毛利额"].sum()
overall_margin = (total_profit / total_sales) * 100

print("\n========== 整体KPI ==========")
print(f"总销售额: {total_sales:,.2f} 元")
print(f"总成本: {total_cost:,.2f} 元")
print(f"总毛利: {total_profit:,.2f} 元")
print(f"整体毛利率: {overall_margin:.2f}%")

# 月度销售趋势
monthly = df.groupby("月份")["销售额"].sum()
plt.figure(figsize=(8,4))
plt.plot(monthly.index, monthly.values, marker='o')
plt.title("2019年1-8月月度销售额趋势")
plt.xlabel("月份")
plt.ylabel("销售额（元）")
plt.grid(True)
plt.savefig("monthly_sales.png")
plt.show()

# 商品类别分析 
category = df.groupby("商品类别").agg({
    "销售额": "sum",
    "毛利额": "sum",
    "利润率": "mean"
}).sort_values("毛利额", ascending=False)
print("\n========== 商品类别表现 ==========")
print(category)

category["毛利额"].plot(kind='bar', color='skyblue')
plt.title("各商品类别毛利额")
plt.xlabel("商品类别")
plt.ylabel("毛利额（元）")
plt.xticks(rotation=45)
plt.savefig("category_profit.png")
plt.show()

# 省份毛利前10后5
province = df.groupby("省份")["毛利额"].sum().sort_values(ascending=False)
print("\n========== 毛利额 TOP10 省份 ==========")
print(province.head(10))
print("\n========== 毛利额 后5 省份（需关注） ==========")
print(province.tail(5))

province.head(10).plot(kind='bar', color='lightcoral')
plt.title("毛利额最高的10个省份")
plt.xlabel("省份")
plt.ylabel("毛利额（元）")
plt.xticks(rotation=45)
plt.savefig("top10_provinces.png")
plt.show()

# 高利润商品 TOP20
top_products = df.groupby("商品名称").agg({
    "毛利额": "sum",
    "销售额": "sum",
    "利润率": "mean",
    "销售数量": "sum"
}).sort_values("毛利额", ascending=False).head(20)
print("\n========== 毛利额 TOP20 商品 ==========")
print(top_products[["毛利额", "销售额", "利润率", "销售数量"]])

# 保存为CSV供Power BI使用
top_products.to_csv("top20_products.csv")

# 帕累托分析
product_profit = df.groupby("商品名称")["毛利额"].sum().sort_values(ascending=False)
cumsum = product_profit.cumsum() / product_profit.sum()

plt.figure(figsize=(10,5))
plt.plot(range(1, len(cumsum)+1), cumsum.values, marker='.')
plt.axhline(y=0.8, color='r', linestyle='--', label='80%贡献线')
plt.title("帕累托图：商品累计毛利贡献")
plt.xlabel("商品排名（按毛利从高到低）")
plt.ylabel("累计毛利占比")
plt.legend()
plt.grid(True)
plt.savefig("pareto.png")
plt.show()

n_80 = (cumsum <= 0.8).sum()
print(f"\n达到80%总毛利所需的商品数量: {n_80} 个(占总数 {n_80/len(product_profit)*100:.1f}%)")

print("\n 所有分析完成！")