-- 创建 ODS 外部表（原始数据）
CREATE EXTERNAL TABLE ods_user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id BIGINT,
    behavior_type STRING,
    `timestamp` BIGINT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/ods_user_behavior';

-- 创建 DWD 明细表（清洗后，ORC 格式，分区）
CREATE TABLE dwd_user_behavior (
    user_id BIGINT,
    item_id BIGINT,
    category_id BIGINT,
    behavior_type STRING,
    behavior_time TIMESTAMP
)
PARTITIONED BY (dt STRING)
STORED AS ORC;

-- 插入 DWD 数据（需先上传原始 CSV 到 ODS 目录）
-- INSERT OVERWRITE TABLE dwd_user_behavior PARTITION (dt)
-- SELECT ... 具体语句见 Python 脚本说明

-- 创建 DWS 用户日汇总表
CREATE EXTERNAL TABLE dws_user_daily (
    user_id BIGINT,
    dt STRING,
    pv_cnt INT,
    fav_cnt INT,
    cart_cnt INT,
    buy_cnt INT
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/dws_user_daily';