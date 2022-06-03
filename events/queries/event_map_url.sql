SELECT
    HLOC.id,
    HLOC.map_url
FROM 
    HOME_LOCATION AS HLOC
WHERE 
    HLOC.id = {location_id};