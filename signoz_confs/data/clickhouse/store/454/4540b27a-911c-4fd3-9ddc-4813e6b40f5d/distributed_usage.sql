ATTACH TABLE _ UUID '03b98eb9-ee9d-4630-92ce-14838efd1789'
(
    `tenant` String,
    `collector_id` String,
    `exporter_id` String,
    `timestamp` DateTime,
    `data` String
)
ENGINE = Distributed('cluster', 'signoz_logs', 'usage', cityHash64(rand()))
