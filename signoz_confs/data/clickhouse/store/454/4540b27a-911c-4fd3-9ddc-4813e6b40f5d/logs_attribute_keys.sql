ATTACH TABLE _ UUID '5d211fce-9191-41b4-89ed-e7a4e6e94fbf'
(
    `name` String,
    `datatype` String
)
ENGINE = ReplacingMergeTree
ORDER BY (name, datatype)
SETTINGS index_granularity = 8192
