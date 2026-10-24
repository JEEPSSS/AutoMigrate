-- Busiest workstation by total assigned tickets; retain tied leaders.
SELECT TOP (1) WITH TIES w.Workstation_ID, w.Workstation_Type,
       COUNT(st.Service_Ticket_ID) AS Tickets
FROM WORKSTATION w
LEFT JOIN SERVICE_TICKET st ON st.Workstation_ID = w.Workstation_ID
GROUP BY w.Workstation_ID, w.Workstation_Type
ORDER BY COUNT(st.Service_Ticket_ID) DESC;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.950028+08:00
+------------------+-----------------------+-----------+
| Workstation_ID   | Workstation_Type      | Tickets   |
+==================+=======================+===========+
| 1                | ESD-Safe Mobile Bench | 20        |
+------------------+-----------------------+-----------+
1 row(s).
*/
