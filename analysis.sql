-- Active: 1777003821472@@127.0.0.1@3306@itcast
-- 销售数据分析查询
-- 假设表名为 sales_cleaned

-- 1. 整体 KPI
SELECT 
    SUM(销售额) AS 总销售额,
    SUM(成本额) AS 总成本,
    SUM(毛利额) AS 总毛利,
    ROUND(SUM(毛利额)/SUM(销售额)*100, 2) AS 毛利率
FROM sales_cleaned;

-- 2. 月度销售趋势
SELECT 
    MONTH(销售日期) AS 月份,
    SUM(销售额) AS 月销售额
FROM sales_cleaned
GROUP BY MONTH(销售日期)
ORDER BY 月份;

-- 3. 商品类别毛利排名
SELECT 
    商品类别,
    SUM(毛利额) AS 总毛利,
    AVG(利润率) AS 平均毛利率
FROM sales_cleaned
GROUP BY 商品类别
ORDER BY 总毛利 DESC;

-- 4. 省份毛利后5名（需优化）
SELECT 
    省份,
    SUM(毛利额) AS 总毛利
FROM sales_cleaned
GROUP BY 省份
ORDER BY 总毛利 ASC
LIMIT 5;

-- 5. 高利润商品 TOP10
SELECT 
    商品名称,
    SUM(毛利额) AS 总毛利,
    SUM(销售额) AS 总销售额,
    AVG(利润率) AS 平均毛利率
FROM sales_cleaned
GROUP BY 商品名称
ORDER BY 总毛利 DESC
LIMIT 10;

-- 6. 帕累托分析（MySQL 8.0+ 窗口函数）
WITH product_profit AS (
    SELECT 
        商品名称,
        SUM(毛利额) AS 毛利额
    FROM sales_cleaned
    GROUP BY 商品名称
),
ranked AS (
    SELECT 
        商品名称,
        毛利额,
        SUM(毛利额) OVER (ORDER BY 毛利额 DESC) AS running_total,
        SUM(毛利额) OVER () AS total_profit
    FROM product_profit
)
SELECT 
    商品名称,
    毛利额,
    ROUND(running_total / total_profit, 4) AS 累计毛利占比
FROM ranked
WHERE running_total / total_profit <= 0.8
ORDER BY 累计毛利占比;