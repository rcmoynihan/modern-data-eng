ATTACH TABLE _ UUID 'f25e8dc9-a256-4ac1-a9bc-922f7c7e9d1c'
(
    `tenant` String,
    `collector_id` String,
    `exporter_id` String,
    `timestamp` DateTime,
    `data` String
)
ENGINE = Distributed('cluster', 'signoz_metrics', 'usage', cityHash64(rand()))
