ATTACH MATERIALIZED VIEW _ UUID 'fb493f8d-9fb8-4397-8265-e119551ef2cf' TO signoz_logs.logs_attribute_keys
(
    `name` String,
    `datatype` String
) AS
SELECT DISTINCT
    arrayJoin(attributes_int64_key) AS name,
    'Int64' AS datatype
FROM signoz_logs.logs
ORDER BY name ASC
