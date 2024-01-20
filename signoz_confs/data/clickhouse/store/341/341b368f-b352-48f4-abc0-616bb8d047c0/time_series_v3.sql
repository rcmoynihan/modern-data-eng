ATTACH TABLE _ UUID '497e79c6-a932-43f6-b555-d1e8d5e4b6b9'
(
    `env` LowCardinality(String) DEFAULT 'default',
    `temporality` LowCardinality(String) DEFAULT 'Unspecified',
    `metric_name` LowCardinality(String),
    `fingerprint` UInt64 CODEC(Delta(8), ZSTD(1)),
    `timestamp_ms` Int64 CODEC(Delta(8), ZSTD(1)),
    `labels` String CODEC(ZSTD(5)),
    `description` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `unit` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `type` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `is_monotonic` Bool DEFAULT false CODEC(ZSTD(1))
)
ENGINE = ReplacingMergeTree
PARTITION BY toDate(timestamp_ms / 1000)
ORDER BY (env, temporality, metric_name, fingerprint)
SETTINGS index_granularity = 8192
