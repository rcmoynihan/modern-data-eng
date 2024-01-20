ATTACH TABLE _ UUID '3eda0310-b691-4542-86b2-bec65ff2bab1'
(
    `timestamp` DateTime64(9) CODEC(DoubleDelta, LZ4),
    `traceID` FixedString(32) CODEC(ZSTD(1)),
    `model` String CODEC(ZSTD(9))
)
ENGINE = Distributed('cluster', 'signoz_traces', 'signoz_spans', cityHash64(traceID))
