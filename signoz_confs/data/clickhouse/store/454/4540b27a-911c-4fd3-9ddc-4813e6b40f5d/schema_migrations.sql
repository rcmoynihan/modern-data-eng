ATTACH TABLE _ UUID '9d321efe-2d73-4837-b818-c0b64c89f5dc'
(
    `version` Int64,
    `dirty` UInt8,
    `sequence` UInt64
)
ENGINE = MergeTree
ORDER BY sequence
SETTINGS index_granularity = 8192
