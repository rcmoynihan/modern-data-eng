ATTACH TABLE _ UUID '7d35c06a-bc3e-40d8-8e96-866f86d205e0'
(
    `name` String,
    `datatype` String
)
ENGINE = ReplacingMergeTree
ORDER BY (name, datatype)
SETTINGS index_granularity = 8192
