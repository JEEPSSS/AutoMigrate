-- P1. Technician(s) with the most billable hours; retain ties.
WITH Hours AS (
    SELECT t.Technician_ID, t.Name,
           SUM(ws.Billable_Time) AS Billable_Minutes
    FROM TECHNICIAN t
    JOIN WORK_SESSION ws ON ws.Technician_ID = t.Technician_ID
    GROUP BY t.Technician_ID, t.Name
)
SELECT TOP (1) WITH TIES Technician_ID, Name,
       CAST(Billable_Minutes / 60.0 AS DECIMAL(10,2)) AS Billable_Hours
FROM Hours
ORDER BY Billable_Minutes DESC;
