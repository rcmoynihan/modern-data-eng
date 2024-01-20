ATTACH TABLE _ UUID '8eddaea4-8eb7-4269-ac05-83f16676664b'
(
    `name` String,
    `datatype` String
)
ENGINE = Distributed('cluster', 'signoz_logs', 'logs_resource_keys', cityHash64(datatype))
