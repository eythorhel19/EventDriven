SELECT 
    *
FROM 
    HOME_EVENTTICKETTYPEPRICE AS HETT
JOIN 
    HOME_TICKETTYPE AS HTT ON HTT.id = HETT.ticket_type_id
WHERE 
    HETT.event_id = {event_id};