ATTACH TABLE _ UUID '7582afc7-6a08-4a08-8469-a611337bef0a'
(
    `src` LowCardinality(String) CODEC(ZSTD(1)),
    `dest` LowCardinality(String) CODEC(ZSTD(1)),
    `duration_quantiles_state` AggregateFunction(quantiles(0.5, 0.75, 0.9, 0.95, 0.99), Float64) CODEC(Default),
    `error_count` SimpleAggregateFunction(sum, UInt64) CODEC(T64, ZSTD(1)),
    `total_count` SimpleAggregateFunction(sum, UInt64) CODEC(T64, ZSTD(1)),
    `timestamp` DateTime CODEC(DoubleDelta, LZ4)
)
ENGINE = AggregatingMergeTree
PARTITION BY toDate(timestamp)
ORDER BY (timestamp, src, dest)
TTL toDateTime(timestamp) + toIntervalSecond(1296000)
SETTINGS index_granularity = 8192, ttl_only_drop_parts = 1
