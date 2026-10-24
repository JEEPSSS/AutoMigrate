-- Q1. For each repair station, count procedures that took < 180 minutes to complete, broken down by device category.
WITH ProcTime AS (
    SELECT p.Procedure_ID, p.Service_Ticket_ID,
           SUM(ws.Billable_Time) AS Total_Minutes
    FROM REPAIR_PROCEDURE p
    JOIN WORK_SESSION ws    ON ws.Procedure_ID = p.Procedure_ID
    JOIN SERVICE_TICKET st  ON st.Service_Ticket_ID = p.Service_Ticket_ID
    WHERE st.Status IN ('Ready for Pickup', 'Completed')      -- finished jobs only
    GROUP BY p.Procedure_ID, p.Service_Ticket_ID
)
SELECT w.Workstation_ID, w.Workstation_Type, dt.Device_Category,
       COUNT(*) AS Procedures_Under_180_Min
FROM ProcTime pt
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = pt.Service_Ticket_ID
JOIN WORKSTATION w     ON w.Workstation_ID = st.Workstation_ID
JOIN DEVICE d          ON d.Device_ID = st.Device_ID
JOIN DEVICE_TYPE dt    ON dt.Model_ID = d.Model_ID
WHERE pt.Total_Minutes < 180
GROUP BY w.Workstation_ID, w.Workstation_Type, dt.Device_Category
ORDER BY w.Workstation_ID, dt.Device_Category;
