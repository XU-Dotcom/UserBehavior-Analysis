import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ================== 配置 ==================
csv_path = r"D:\Drivers\UserBehavior.csv"  # 原始数据路径
chunk_size = 500000  # 每块行数
output_csv = r"user_daily.csv"  # 聚合结果保存路径
output_dir = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 列名（无表头）
names = ['user_id', 'item_id', 'category_id', 'behavior_type', 'timestamp']

# 时间戳范围（秒级，2017-11-01 ～ 2017-12-31）
min_ts = 1509494400
max_ts = 1514736000

# 有效行为（根据你的检测结果：数据中行为类型已是字符串）
valid_behaviors = ['pv', 'fav', 'buy', 'cart']  # 顺序可调整

# ================== 1. 分块读取并聚合 ==================
print("开始分块读取并聚合...")
agg_chunks = []

for i, chunk in enumerate(pd.read_csv(csv_path, names=names, chunksize=chunk_size)):
    print(f"处理第 {i + 1} 块，原始行数: {len(chunk)}")

    # 1) 过滤时间戳范围
    chunk = chunk[(chunk['timestamp'] >= min_ts) & (chunk['timestamp'] <= max_ts)]
    print(f"  过滤时间戳后行数: {len(chunk)}")
    if len(chunk) == 0:
        continue

    # 2) 过滤有效行为类型（已是字符串）
    chunk = chunk[chunk['behavior_type'].isin(valid_behaviors)]
    print(f"  过滤行为后行数: {len(chunk)}")
    if len(chunk) == 0:
        continue

    # 3) 转换时间戳为日期
    chunk['behavior_time'] = pd.to_datetime(chunk['timestamp'], unit='s')
    chunk['dt'] = chunk['behavior_time'].dt.date

    # 4) 按用户、日期、行为类型计数
    daily = chunk.groupby(['user_id', 'dt', 'behavior_type']).size().unstack(fill_value=0).reset_index()
    daily.columns.name = None

    # 确保所有行为列都存在
    for col in valid_behaviors:
        if col not in daily.columns:
            daily[col] = 0

    # 重命名列（加 _cnt 后缀）
    daily = daily.rename(columns={b: f'{b}_cnt' for b in valid_behaviors})

    agg_chunks.append(daily)

# 合并所有分块
if agg_chunks:
    user_daily = pd.concat(agg_chunks, ignore_index=True)
    # 二次聚合（同一用户可能出现在不同块）
    user_daily = user_daily.groupby(['user_id', 'dt'])[[f'{b}_cnt' for b in valid_behaviors]].sum().reset_index()
    print(f"聚合完成，共 {len(user_daily)} 行")
    user_daily.to_csv(output_csv, index=False)
    print(f"聚合结果已保存至: {output_csv}")
else:
    print("错误：没有有效数据，请检查路径或时间戳范围。")
    exit()

# ================== 2. 漏斗分析 ==================
print("\n开始漏斗分析...")
funnel = user_daily.groupby('dt').agg({
    f'{b}_cnt': lambda x: (x > 0).sum() for b in valid_behaviors
}).reset_index()

# 找出浏览用户数最多的一天（pv_cnt 最大）
max_day = funnel.loc[funnel['pv_cnt'].idxmax(), 'dt']
print(f"活跃用户数最多的一天: {max_day}")
day_data = funnel[funnel['dt'] == max_day]

# 构造展示顺序（pv -> fav -> cart -> buy）
display_order = ['pv', 'fav', 'cart', 'buy']
stages = []
counts = []
for b in display_order:
    if b in valid_behaviors:
        col = f'{b}_cnt'
        if col in day_data.columns:
            cnt = day_data[col].iloc[0]
            stages.append(b)
            counts.append(cnt)
        else:
            print(f"警告：行为 {b} 不在聚合表中")

# 绘制漏斗图（水平条形图）
plt.figure(figsize=(8, 4))
plt.barh(stages, counts, color='skyblue')
plt.xlabel('独立用户数')
plt.title(f'{max_day} 用户行为转化漏斗')
for i, v in enumerate(counts):
    plt.text(v + 1000, i, f'{v:,}', va='center')
plt.tight_layout()
funnel_png = os.path.join(output_dir, 'funnel.png')
plt.savefig(funnel_png, dpi=150)
plt.show()
print(f"漏斗图已保存至: {funnel_png}")

# ================== 3. 留存分析 ==================
print("\n开始留存分析...")
# 选择有购买行为的用户（避免数据过大，且留存通常关注核心用户）
active_users = user_daily[user_daily['buy_cnt'] > 0].copy()
if len(active_users) == 0:
    print("警告：没有购买用户，无法计算留存。")
else:
    # 计算每个用户首次活跃日期
    first = active_users.groupby('user_id')['dt'].min().reset_index()
    first.columns = ['user_id', 'first_dt']
    merged = active_users.merge(first, on='user_id')
    merged['days_diff'] = (pd.to_datetime(merged['dt']) - pd.to_datetime(merged['first_dt'])).dt.days

    # 构建留存矩阵
    retention = merged.groupby(['first_dt', 'days_diff']).size().unstack(fill_value=0)
    # 只显示前 7 天
    retention_7 = retention.iloc[:, 1:8]  # days_diff 1~7

    # 限制首次日期数量，避免图片过大
    if retention_7.shape[0] > 50:
        retention_7 = retention_7.iloc[:50, :]

    # 绘制热力图
    plt.figure(figsize=(12, max(6, retention_7.shape[0] * 0.3)))
    sns.heatmap(retention_7, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': '用户数'})
    plt.title('用户留存热力图（购买用户，第1-7天）')
    plt.xlabel('首次后第几天')
    plt.ylabel('首次活跃日期')
    plt.tight_layout()
    retention_png = os.path.join(output_dir, 'retention.png')
    plt.savefig(retention_png, dpi=150)
    plt.show()
    print(f"留存热力图已保存至: {retention_png}")

print("\n所有分析完成！")