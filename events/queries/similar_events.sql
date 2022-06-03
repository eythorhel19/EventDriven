SELECT *
FROM (
    SELECT 
        THIS_EVENT.id, 
        THIS_EVENT.title, 
        THIS_EVENT.description, 
        THIS_EVENT.maximum_capacity, 
        THIS_EVENT.start_date, 
        THIS_EVENT.end_date, 
        THIS_EVENT.location_id, 
        THIS_EVENT.main_image_url, 
        COUNT(*) as apperances
    FROM
        EVENTS_EVENT AS THIS_EVENT
        JOIN HOME_EVENTENTERTAINER AS HEENT 
        ON HEENT.event_id = THIS_EVENT.id
        JOIN HOME_EVENTCATEGORY AS HECAT 
        ON HECAT.event_id = THIS_EVENT.id
    WHERE
        HEENT.entertainer_id IN (
            SELECT HEENT.entertainer_id
            FROM EVENTS_EVENT AS EEVE
            JOIN HOME_EVENTENTERTAINER AS HEENT ON HEENT.event_id = EEVE.id
            JOIN HOME_EVENTCATEGORY AS HECAT ON HECAT.event_id = EEVE.id
            WHERE 
                EEVE.id = {event_id}
        ) OR 
        HECAT.category_id IN (
            SELECT HECAT.category_id
            FROM EVENTS_EVENT AS EEVE
            JOIN HOME_EVENTENTERTAINER AS HEENT 
            ON HEENT.event_id = EEVE.id
            JOIN HOME_EVENTCATEGORY AS HECAT 
            ON HECAT.event_id = EEVE.id
            WHERE EEVE.id = {event_id}
        ) AND THIS_EVENT.id != {event_id}
    GROUP BY 
        THIS_EVENT.id, 
        THIS_EVENT.title, 
        THIS_EVENT.description, 
        THIS_EVENT.maximum_capacity, 
        THIS_EVENT.start_date, 
        THIS_EVENT.end_date, 
        THIS_EVENT.location_id, 
        THIS_EVENT.main_image_url
    ORDER BY 
        apperances DESC
    ) AS MOST_SIMILAR_EVENTS
    JOIN HOME_LOCATION AS HLOC 
        ON HLOC.id = MOST_SIMILAR_EVENTS.location_id;