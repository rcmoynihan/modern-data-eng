ATTACH TABLE _ UUID '156fd286-f230-4a05-a2aa-fd31689d44b0'
(
    `timestamp` DateTime CODEC(DoubleDelta, ZSTD(1)),
    `tagKey` LowCardinality(String) CODEC(ZSTD(1)),
    `tagType` Enum8('tag' = 1, 'resource' = 2) CODEC(ZSTD(1)),
    `dataType` Enum8('string' = 1, 'bool' = 2, 'float64' = 3) CODEC(ZSTD(1)),
    `stringTagValue` String CODEC(ZSTD(1)),
    `float64TagValue` Nullable(Float64) CODEC(ZSTD(1)),
    `isColumn` Bool CODEC(ZSTD(1))
)
ENGINE = ReplacingMergeTree
ORDER BY (tagKey, tagType, dataType, stringTagValue, float64TagValue, isColumn)
TTL toDateTime(timestamp) + toIntervalSecond(172800)
SETTINGS ttl_only_drop_parts = 1, allow_nullable_key = 1, index_granularity = 8192
