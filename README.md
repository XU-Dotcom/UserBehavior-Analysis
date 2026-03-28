# 电商用户行为数据分析与数仓建设

## 项目简介
- **数据来源**：阿里天池 UserBehavior 数据集（3.5GB，包含浏览、收藏、加购、购买行为）
- **目标**：清洗数据、构建数仓分层、分析用户转化漏斗与留存，输出可视化报表

## 技术栈
- Python（Pandas, Matplotlib, Seaborn）
- Hive（数仓建模，ODS-DWD-DWS 分层）
- Tableau（可视化仪表板）

## 处理流程
1. **Python 分块处理**：读取 3.5GB 原始数据，过滤无效记录，聚合生成用户日行为表（约 710 万行）
2. **Hive 数仓建设**：将聚合结果导入 Hive 外部表，设计数仓分层
3. **数据分析**：计算转化漏斗与用户留存
4. **可视化**：使用 Tableau 制作日活趋势图、转化漏斗图，并撰写业务建议

## 核心结论
- 加购→购买转化率约为 52.9%（174,698 / 330,388），建议优化结算流程。
- 购买用户次日留存率约 10~30%，可作为用户召回重点对象。

## 文件说明
- `process_data.py`：Python 分块处理与聚合脚本
- `create_tables.sql`：Hive 建表与查询 SQL
- `funnel.png` / `retention.png`：Python 生成的分析图
- `dashboard.twbx`：Tableau 仪表板文件（如有）
- `dashboard_screenshot.png`：仪表板截图（如有）

## 运行说明
- Python 依赖：pandas, matplotlib, seaborn
- 如需重新处理，修改脚本中的文件路径后运行即可。
- Hive 环境需预先部署（本机或虚拟机）。

## 数据来源
[阿里天池 UserBehavior 数据集](https://tianchi.aliyun.com/dataset/649)
## 补充材料
- [埋点设计文档](./docs/event_tracking.md)
- [宽表设计方案](./docs/wide_table_design.md)
- [活动效果分析报告](./docs/campaign_analysis.md)
