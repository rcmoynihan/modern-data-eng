ATTACH MATERIALIZED VIEW _ UUID '381fa470-d638-40f7-9754-7db73aab9d01' TO signoz_traces.usage_explorer
(
    `timestamp` DateTime,
    `service_name` LowCardinality(String),
    `count` UInt64
) AS
SELECT
    toStartOfHour(timestamp) AS timestamp,
    serviceName AS service_name,
    count() AS count
FROM signoz_traces.signoz_index_v2
GROUP BY
    timestamp,
    serviceName
