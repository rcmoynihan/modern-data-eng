ATTACH MATERIALIZED VIEW _ UUID 'de6e7ca1-6c95-4d72-bf34-242f8aa7a5cb' TO signoz_logs.logs_attribute_keys
(
    `name` String,
    `datatype` String
) AS
SELECT DISTINCT
    arrayJoin(attributes_float64_key) AS name,
    'Float64' AS datatype
FROM signoz_logs.logs
ORDER BY name ASC
