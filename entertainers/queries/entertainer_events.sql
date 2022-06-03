SELECT 
    EVE.*, 
    HLOC.name AS location
FROM 
    ENTERTAINERS_ENTERTAINER AS ENT
    JOIN HOME_EVENTENTERTAINER AS HEE 
    ON ENT.id = HEE.entertainer_id
    JOIN EVENTS_EVENT AS EVE 
    ON HEE.event_id = EVE.id
    JOIN HOME_LOCATION AS HLOC 
    ON HLOC.id = EVE.location_id
WHERE 
    ENT.id = {entertainer_id} AND EVE.start_date >= CURRENT_DATE
ORDER BY 
    EVE.start_date;