ATTACH TABLE _ UUID 'bcab14f2-4494-4ee3-b5c8-3d7bb1145aa8'
(
    `name` LowCardinality(String) CODEC(ZSTD(1)),
    `serviceName` LowCardinality(String) CODEC(ZSTD(1))
)
ENGINE = Distributed('cluster', 'signoz_traces', 'top_level_operations', cityHash64(rand()))
