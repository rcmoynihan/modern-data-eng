ATTACH TABLE _ UUID '5890d9f5-f331-41e2-ba5d-a1d7d8133497'
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
ENGINE = Distributed('cluster', 'signoz_metrics', 'time_series_v3', cityHash64(env, temporality, metric_name, fingerprint))
