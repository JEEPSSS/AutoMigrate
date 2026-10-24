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

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.813488+08:00
+-----------------+-------------+------------------+
| Technician_ID   | Name        | Billable_Hours   |
+=================+=============+==================+
| 5               | Evelyn Chua | 18.00            |
+-----------------+-------------+------------------+
1 row(s).
*/
