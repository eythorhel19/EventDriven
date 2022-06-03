SELECT *
FROM (
    SELECT DISTINCT ON (EENT.id) EENT.id, 
        EENT.name, 
        EENT.description, 
        EENT.image_url, 
        MIN(EVE.start_date) AS next_event_date, 
        HLOC.name AS location_name
    FROM 
        ENTERTAINERS_ENTERTAINER AS EENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT 
        ON EENT.ID = HEVENT.ENTERTAINER_ID
        JOIN EVENTS_EVENT AS EVE 
        ON EVE.ID = HEVENT.EVENT_ID
        JOIN HOME_LOCATION AS HLOC 
        ON HLOC.ID = EVE.LOCATION_ID
    WHERE 
        EVE.START_DATE >= CURRENT_DATE
    GROUP BY 
        EENT.id, EENT.name, EENT.description, EENT.image_url, HLOC.name, EVE.id, EVE.start_date
    ) AS FRO_GROUP_BY
ORDER BY 
    FRO_GROUP_BY.next_event_date;