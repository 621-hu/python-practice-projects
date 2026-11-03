# README

# 📊 销售数据可视化分析（data-analysis-demo）

一个端到端的 Python 数据分析小项目：从「生成示例数据」到「清洗 → 统计 → 可视化 → 输出报告」全流程覆盖。
适合实习生展示**数据处理与可视化**能力。

## ✨ 项目亮点

- **可复现数据**：`generate_data.py` 用固定随机种子生成 600 条电商销售数据
- **数据清洗**：日期解析、类型转换、异常行剔除
- **多维分析**：月度趋势、品类占比、地区对比、Top 商品
- **可视化**：折线图 / 饼图 / 柱状图（matplotlib）
- **中文字体自适应**：检测不到中文字体时自动回退英文标签，图表绝不乱码

## 🚀 运行步骤

```bash
pip install -r requirements.txt

# 1) 生成示例数据（可选，仓库已附带 data/sales.csv）
python generate_data.py

# 2) 执行分析并生成图表与报告
python analyze.py
```

运行后会在 `output/` 目录生成三张图表，并在根目录生成 `report.txt` 文本报告。

## 📁 项目结构

```
data-analysis-demo/
├── generate_data.py   # 生成可复现的示例销售数据
├── analyze.py         # 清洗 / 统计 / 可视化 / 报告
├── data/
│   └── sales.csv      # 示例数据（已附带）
├── output/            # 生成的图表（已忽略）
├── report.txt         # 文本报告（已忽略）
├── requirements.txt
└── README.md
```

## 📌 适合学习的技术点

- `pandas` 数据读取、分组聚合（`groupby`）、时间序列处理
- 数据清洗与缺失值处理
- `matplotlib` 基础绘图与排版
- 字体检测与跨平台兼容性处理
- 脚本化、可复现的数据分析流程

## 🖼 示例图表

| 月度趋势 | 品类占比 | 地区对比 |
| --- | --- | --- |
| `output/monthly_trend.png` | `output/category_pie.png` | `output/region_bar.png` |
