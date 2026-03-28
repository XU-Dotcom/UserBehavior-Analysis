# 电商用户行为宽表设计

## 1. 设计背景
为方便业务分析人员快速获取用户行为、用户属性及商品类目等维度数据，减少多表关联的复杂度和查询耗时，需设计一张面向分析的用户行为宽表（`ads_user_behavior_wide`）。该宽表将用户日行为汇总表与用户画像、商品类目等维度信息关联，支持日常运营报表、用户画像分析和活动效果评估。

## 2. 宽表结构
| 字段名 | 类型 | 说明 |
|--------|------|------|
| user_id | BIGINT | 用户ID |
| dt | STRING | 日期（yyyy-MM-dd） |
| pv_cnt | INT | 当日浏览次数 |
| fav_cnt | INT | 当日收藏次数 |
| cart_cnt | INT | 当日加购次数 |
| buy_cnt | INT | 当日购买次数 |
| register_date | STRING | 用户注册日期（模拟） |
| user_level | STRING | 用户等级（模拟） |
| category_id | BIGINT | 用户当日主要购买类目（取购买次数最多的类目，若无购买则为空） |
| category_name | STRING | 类目名称 |

## 3. 数据来源
- **用户日行为表**：`dws_user_daily`（已通过 Python 聚合生成）
- **用户画像维度表**：`dim_user_info`（模拟数据，实际可从业务库获取）
  - 字段：user_id, register_date, user_level
- **商品类目维度表**：`dim_category`（模拟数据）
  - 字段：category_id, category_name, parent_category

## 4. 建表语句（Hive）
```sql
CREATE EXTERNAL TABLE ads_user_behavior_wide (
    user_id BIGINT,
    dt STRING,
    pv_cnt INT,
    fav_cnt INT,
    cart_cnt INT,
    buy_cnt INT,
    register_date STRING,
    user_level STRING,
    category_id BIGINT,
    category_name STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/ads_user_behavior_wide';
