ATTACH TABLE _ UUID 'bb7d4e57-6603-4449-b19d-1a68728a706d'
(
    `timestamp` DateTime64(9) CODEC(DoubleDelta, LZ4),
    `service_name` LowCardinality(String) CODEC(ZSTD(1)),
    `count` UInt64 CODEC(T64, ZSTD(1))
)
ENGINE = Distributed('cluster', 'signoz_traces', 'usage_explorer', cityHash64(rand()))
