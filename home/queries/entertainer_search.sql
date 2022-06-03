SELECT *
FROM (
    SELECT DISTINCT ON (ENT.id)
        ENT.id,
        ENT.name,
        ENT.description,
        ENT.image_url,
        EVEE.title,
        EVEE.start_date,
        MIN(EVEE.start_date) AS next_event_date,
        HLOC.name AS location_name
    FROM 
        ENTERTAINERS_ENTERTAINER AS ENT
        JOIN HOME_EVENTENTERTAINER AS HEVENT
        ON ENT.id = HEVENT.entertainer_id
        JOIN EVENTS_EVENT AS EVEE
        ON EVEE.id = HEVENT.event_id
        JOIN HOME_LOCATION AS HLOC 
        ON HLOC.id = EVEE.location_id
    GROUP BY 
        ENT.id, ENT.name, ENT.description, ENT.image_url, EVEE.title, HLOC.name, EVEE.start_date
    ) AS X
WHERE 
    {where_cond} X.start_date >= CURRENT_DATE;