-- P6. Ticket count per workstation and ticket status, including empty stations.
SELECT w.Workstation_ID, w.Workstation_Type, w.Status AS Station_Status,
       COALESCE(st.Status, '(no tickets)') AS Ticket_Status,
       COUNT(st.Service_Ticket_ID) AS Tickets
FROM WORKSTATION w
LEFT JOIN SERVICE_TICKET st ON st.Workstation_ID = w.Workstation_ID
GROUP BY w.Workstation_ID, w.Workstation_Type, w.Status, st.Status
ORDER BY w.Workstation_ID, st.Status;
