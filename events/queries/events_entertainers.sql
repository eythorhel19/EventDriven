SELECT *
FROM (
    SELECT DISTINCT ON (EENT.id) 
        EENT.id, 
        EENT.name, 
        EENT.description, 
        EENT.image_url, 
        MIN(EVE.start_date) AS next_event_id, 
        HLOC.name AS location_name
    FROM 
        ENTERTAINERS_ENTERTAINER AS EENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT 
        ON EENT.id = HEVENT.entertainer_id
        JOIN EVENTS_EVENT AS EVE 
        ON EVE.id = HEVENT.event_id
        JOIN HOME_LOCATION AS HLOC 
        ON HLOC.id = EVE.location_id
    WHERE 
        EVE.start_date >= CURRENT_DATE
    GROUP BY 
        EENT.id, EENT.name, EENT.description, EENT.image_url, HLOC.name, EVE.id, EVE.start_date
    HAVING 
        EVE.ID = {event_id}) AS FRO_GROUP_BY
ORDER BY 
    FRO_GROUP_BY.next_event_id;