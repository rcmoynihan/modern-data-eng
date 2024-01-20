ATTACH TABLE _ UUID '2839cb11-a6bb-4576-a16c-262cffb900b1'
(
    `tenant` String,
    `collector_id` String,
    `exporter_id` String,
    `timestamp` DateTime,
    `data` String
)
ENGINE = Distributed('cluster', 'signoz_traces', 'usage', cityHash64(rand()))
