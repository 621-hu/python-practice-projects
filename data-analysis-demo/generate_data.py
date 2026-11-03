#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成可复现的示例电商销售数据。

固定随机种子，每次运行生成完全相同的 600 条销售记录，
输出到 data/sales.csv，字段包括:
    date, category, region, product, price, quantity, sales
"""

import csv
import os
import random
from datetime import date, timedelta

SEED = 42
N_RECORDS = 600
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT_FILE = os.path.join(OUT_DIR, "sales.csv")

# 品类 -> 商品与价格区间（单位：元）
CATEGORY_PRODUCTS = {
    "手机数码": [("智能手机", (1500, 3200)), ("平板电脑", (1200, 2800)), ("蓝牙耳机", (150, 800))],
    "家用电器": [("空调", (2000, 4500)), ("洗衣机", (900, 2500)), ("电饭煲", (200, 600))],
    "服饰": [("羽绒服", (300, 900)), ("运动鞋", (200, 600)), ("衬衫", (80, 250))],
    "美妆": [("精华液", (200, 600)), ("口红", (100, 300)), ("面霜", (150, 450))],
    "食品": [("坚果礼盒", (50, 150)), ("咖啡豆", (60, 180)), ("进口牛奶", (40, 120))],
}

REGIONS = ["华东", "华北", "华南", "华中", "西南", "东北", "西北"]

# 品类出现权重，模拟真实销量分布
CATEGORY_WEIGHTS = [30, 25, 20, 13, 12]


def random_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def main():
    random.seed(SEED)

    start = date(2024, 1, 1)
    end = date(2025, 10, 31)

    categories = list(CATEGORY_PRODUCTS.keys())

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "region", "product", "price", "quantity", "sales"])
        for _ in range(N_RECORDS):
            category = random.choices(categories, weights=CATEGORY_WEIGHTS, k=1)[0]
            product, (low, high) = random.choice(CATEGORY_PRODUCTS[category])
            price = round(random.uniform(low, high), 2)
            quantity = random.randint(1, 8)
            d = random_date(start, end)
            writer.writerow([
                d.isoformat(), category, random.choice(REGIONS),
                product, price, quantity, round(price * quantity, 2),
            ])

    print("已生成 {} 条示例数据 -> {}".format(N_RECORDS, OUT_FILE))


if __name__ == "__main__":
    main()
