ATTACH TABLE _ UUID 'b83e4d69-72de-459c-9f61-47b012ab33b8'
(
    `version` Int64,
    `dirty` UInt8,
    `sequence` UInt64
)
ENGINE = MergeTree
ORDER BY sequence
SETTINGS index_granularity = 8192
