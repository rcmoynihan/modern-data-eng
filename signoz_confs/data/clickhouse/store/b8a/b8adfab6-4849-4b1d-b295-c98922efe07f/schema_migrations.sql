ATTACH TABLE _ UUID '77d1de9d-41d8-4086-96b9-9f3bdec15844'
(
    `version` Int64,
    `dirty` UInt8,
    `sequence` UInt64
)
ENGINE = MergeTree
ORDER BY sequence
SETTINGS index_granularity = 8192
