ATTACH TABLE _ UUID '28040587-e21b-4e9d-bfb9-e2c286bb6f11'
(
    `timestamp` DateTime64(9) CODEC(DoubleDelta, LZ4),
    `service_name` LowCardinality(String) CODEC(ZSTD(1)),
    `count` UInt64 CODEC(T64, ZSTD(1))
)
ENGINE = SummingMergeTree
PARTITION BY toDate(timestamp)
ORDER BY (timestamp, service_name)
TTL toDateTime(timestamp) + toIntervalSecond(1296000)
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1
