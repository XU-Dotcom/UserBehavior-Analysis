# 电商 APP 用户行为埋点设计方案（以“双十一大促”为例）

## 1. 埋点目标
- 监控用户在大促期间的浏览、加购、支付行为，评估活动效果。
- 为转化漏斗、用户路径分析提供数据支撑。

## 2. 事件设计
| 事件名称 | 触发时机 | 属性字段 |
|---------|---------|---------|
| page_view | 进入商品详情页 | user_id, page_id, page_name, referrer, timestamp |
| add_to_cart | 点击“加入购物车” | user_id, item_id, category_id, price, quantity, timestamp |
| purchase | 支付成功 | user_id, order_id, total_amount, item_list, timestamp |

## 3. 埋点质量保障
- 开发前：与业务、开发对齐事件定义，编写埋点文档。
- 开发中：使用埋点测试工具（如 Charles、抓包）验证上报参数。
- 上线后：每日监控埋点数据量，核对关键指标（如 DAU、购买事件量）是否符合预期。

## 4. 数据校验示例
- 检查 purchase 事件中 user_id 是否为空。
- 确保 add_to_cart 事件的 price 字段为数字且 >0。
