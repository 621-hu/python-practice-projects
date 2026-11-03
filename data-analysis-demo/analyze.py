#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""销售数据可视化分析。

读取 data/sales.csv，完成清洗 -> 统计 -> 可视化 -> 报告输出:
    - output/monthly_trend.png  月度销售趋势折线图
    - output/category_pie.png   品类销售占比饼图
    - output/region_bar.png     地区销售对比柱状图
    - report.txt                文本分析报告
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "sales.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
REPORT_FILE = os.path.join(BASE_DIR, "report.txt")

# 品类中英文对照（报告使用英文）
CATEGORY_EN = {
    "手机数码": "Electronics",
    "家用电器": "Appliances",
    "服饰鞋包": "Apparel",
    "美妆个护": "Beauty",
    "食品生鲜": "Food",
}

# 中文字体候选；都找不到时回退英文标签，保证图表不乱码
CJK_FONTS = ["Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC",
             "WenQuanYi Micro Hei", "Arial Unicode MS"]


def setup_font():
    """探测可用中文字体；找不到则回退英文标签。"""
    available = {f.name for f in __import__("matplotlib").font_manager.fontManager.ttflist}
    for name in CJK_FONTS:
        if name in available:
            plt.rcParams["font.sans-serif"] = [name]
            plt.rcParams["axes.unicode_minus"] = False
            return True
    plt.rcParams["axes.unicode_minus"] = False
    return False


def load_and_clean():
    df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    before = len(df)
    df = df.dropna(subset=["date", "sales"])
    df = df[df["sales"] >= 0]
    dropped = before - len(df)
    if dropped:
        print("清洗：剔除异常行 {} 条".format(dropped))
    return df


def monthly_trend(df, has_cjk):
    monthly = df.set_index("date").resample("MS")["sales"].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly.values, marker="o", color="#1f77b4")
    ax.set_title("月度销售趋势" if has_cjk else "Monthly Sales Trend")
    ax.set_xlabel("月份" if has_cjk else "Month")
    ax.set_ylabel("销售额 (元)" if has_cjk else "Sales (CNY)")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "monthly_trend.png"), dpi=120)
    plt.close(fig)
    return monthly


def category_pie(df, has_cjk):
    by_cat = df.groupby("category")["sales"].sum().sort_values(ascending=False)
    labels = [CATEGORY_EN.get(c, c) if not has_cjk else c for c in by_cat.index]
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(by_cat.values, labels=labels, autopct="%.1f%%", startangle=90,
           colors=plt.cm.Set2.colors)
    ax.set_title("品类销售占比" if has_cjk else "Sales by Category")
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "category_pie.png"), dpi=120)
    plt.close(fig)
    return by_cat


def region_bar(df, has_cjk):
    by_region = df.groupby("region")["sales"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(by_region.index, by_region.values, color="#2ca02c")
    ax.set_title("地区销售对比" if has_cjk else "Sales by Region")
    ax.set_xlabel("地区" if has_cjk else "Region")
    ax.set_ylabel("销售额 (元)" if has_cjk else "Sales (CNY)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "region_bar.png"), dpi=120)
    plt.close(fig)
    return by_region


def write_report(df, by_cat, top_products):
    total_sales = df["sales"].sum()
    total_qty = int(df["quantity"].sum())
    records = len(df)
    avg_order = total_sales / records if records else 0

    lines = []
    lines.append("==== Sales Data Analysis Report ====")
    lines.append("Records       : {:,}".format(records))
    lines.append("Total sales   : ¥{:,.2f}".format(total_sales))
    lines.append("Total quantity: {:d}".format(total_qty))
    lines.append("Avg order value: ¥{:,.2f}".format(avg_order))
    lines.append("")
    lines.append("-- Sales by Category --")
    for cat, val in by_cat.items():
        lines.append("  {}: ¥{:,.2f}".format(CATEGORY_EN.get(cat, cat), val))
    lines.append("")
    lines.append("-- Top 5 Products by Sales --")
    for prod, val in top_products.items():
        lines.append("  {}: ¥{:,.2f}".format(prod, val))

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("报告已写入 {}".format(REPORT_FILE))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    has_cjk = setup_font()
    if not has_cjk:
        print("未检测到中文字体，图表标签回退英文")

    df = load_and_clean()
    monthly_trend(df, has_cjk)
    by_cat = category_pie(df, has_cjk)
    region_bar(df, has_cjk)
    top_products = df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
    write_report(df, by_cat, top_products)
    print("图表已输出到 output/ 目录")


if __name__ == "__main__":
    main()
