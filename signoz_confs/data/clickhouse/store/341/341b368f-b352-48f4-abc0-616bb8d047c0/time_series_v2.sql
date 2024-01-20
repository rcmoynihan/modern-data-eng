ATTACH TABLE _ UUID '6e9503b9-02b2-4653-966f-7fe302217e18'
(
    `metric_name` LowCardinality(String),
    `fingerprint` UInt64 CODEC(DoubleDelta, LZ4),
    `timestamp_ms` Int64 CODEC(DoubleDelta, LZ4),
    `labels` String CODEC(ZSTD(5)),
    `temporality` LowCardinality(String) DEFAULT 'Unspecified' CODEC(ZSTD(5)),
    `description` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `unit` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `type` LowCardinality(String) DEFAULT '' CODEC(ZSTD(1)),
    `is_monotonic` Bool DEFAULT false CODEC(ZSTD(1)),
    INDEX temporality_index temporality TYPE SET(3) GRANULARITY 1
)
ENGINE = ReplacingMergeTree
PARTITION BY toDate(timestamp_ms / 1000)
ORDER BY (metric_name, fingerprint)
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1
