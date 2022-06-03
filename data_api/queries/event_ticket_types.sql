SELECT
    TT.*,
    ETTP.price,
    CONCAT(TT.description,' - ', ETTP.price) AS option_description
FROM
    HOME_TICKETTYPE AS TT
    INNER JOIN HOME_EVENTTICKETTYPEPRICE AS ETTP
    ON TT.id = ETTP.ticket_type_id
WHERE
    ETTP.event_id = {event_id};