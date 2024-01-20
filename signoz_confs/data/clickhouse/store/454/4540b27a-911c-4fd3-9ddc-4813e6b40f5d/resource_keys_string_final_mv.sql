ATTACH MATERIALIZED VIEW _ UUID '210926cb-1a93-454a-821f-aaa9599d4678' TO signoz_logs.logs_resource_keys
(
    `name` String,
    `datatype` String
) AS
SELECT DISTINCT
    arrayJoin(resources_string_key) AS name,
    'String' AS datatype
FROM signoz_logs.logs
ORDER BY name ASC
