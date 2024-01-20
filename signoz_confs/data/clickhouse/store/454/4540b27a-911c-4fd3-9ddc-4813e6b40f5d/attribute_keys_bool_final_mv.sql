ATTACH MATERIALIZED VIEW _ UUID '2fb1a463-7bf0-49d2-818e-93176c261669' TO signoz_logs.logs_attribute_keys
(
    `name` String,
    `datatype` String
) AS
SELECT DISTINCT
    arrayJoin(attributes_bool_key) AS name,
    'Bool' AS datatype
FROM signoz_logs.logs
ORDER BY name ASC
