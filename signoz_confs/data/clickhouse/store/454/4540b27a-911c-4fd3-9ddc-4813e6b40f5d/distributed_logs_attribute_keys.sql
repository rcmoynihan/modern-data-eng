ATTACH TABLE _ UUID '71b35767-6ddd-4064-a7dd-0bf01faebebd'
(
    `name` String,
    `datatype` String
)
ENGINE = Distributed('cluster', 'signoz_logs', 'logs_attribute_keys', cityHash64(datatype))
