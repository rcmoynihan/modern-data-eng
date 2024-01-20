ATTACH MATERIALIZED VIEW _ UUID 'd43bbb55-bd32-4b85-bcea-5e7f00beb1fd' TO signoz_traces.top_level_operations
(
    `name` LowCardinality(String),
    `serviceName` LowCardinality(String)
) AS
SELECT DISTINCT
    name,
    serviceName
FROM signoz_traces.signoz_index_v2
WHERE parentSpanID = ''
