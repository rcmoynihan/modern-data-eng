ATTACH MATERIALIZED VIEW _ UUID '0b543ef5-236f-49a0-a4e4-1324b3867f05' TO signoz_logs.logs_attribute_keys
(
    `name` String,
    `datatype` String
) AS
SELECT DISTINCT
    arrayJoin(attributes_string_key) AS name,
    'String' AS datatype
FROM signoz_logs.logs
ORDER BY name ASC
