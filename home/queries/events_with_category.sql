SELECT 
    EEV.*,
    HCAT.id AS category_id, 
    HCAT.name AS category_name
FROM 
    EVENTS_EVENT AS EEV
    JOIN HOME_EVENTCATEGORY AS HEVC 
    ON EEV.id = HEVC.event_id
    JOIN HOME_CATEGORY AS HCAT 
    ON HCAT.id = HEVC.category_id
WHERE 
    EEV.start_date >= CURRENT_DATE
ORDER BY 
    HEVC.category_id, EEV.start_date;