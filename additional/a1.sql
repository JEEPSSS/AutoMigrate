-- A1. Bill integrity check: recompute every bill from work sessions and locked part prices. Every row should show Labour_OK = 'Y' and Parts_OK = 'Y'.
WITH Labour AS (
    SELECT p.Service_Ticket_ID, SUM(ws.Billable_Time / 60.0 * t.Standard_Hourly_Billing_Rate) AS Calc_Labour
    FROM REPAIR_PROCEDURE p
    JOIN WORK_SESSION ws ON ws.Procedure_ID = p.Procedure_ID
    JOIN TECHNICIAN t    ON t.Technician_ID = ws.Technician_ID
    GROUP BY p.Service_Ticket_ID
),
Parts AS (
    SELECT p.Service_Ticket_ID, SUM(pa.Quantity_Allocated * pa.Locked_Unit_Price) AS Calc_Parts
    FROM REPAIR_PROCEDURE p
    JOIN PART_ALLOCATION pa ON pa.Procedure_ID = p.Procedure_ID
    GROUP BY p.Service_Ticket_ID
)
SELECT b.Bill_ID, b.Service_Ticket_ID,
       b.Total_Labour_Charges, CAST(COALESCE(l.Calc_Labour, 0) AS DECIMAL(10,2)) AS Calc_Labour,
       b.Total_Component_Costs, CAST(COALESCE(pr.Calc_Parts, 0) AS DECIMAL(10,2)) AS Calc_Parts,
       CASE WHEN ABS(b.Total_Labour_Charges - COALESCE(l.Calc_Labour, 0)) <= 0.05 THEN 'Y' ELSE 'N' END AS Labour_OK,
       CASE WHEN ABS(b.Total_Component_Costs - COALESCE(pr.Calc_Parts, 0)) <= 0.01 THEN 'Y' ELSE 'N' END AS Parts_OK
FROM BILLING_STATEMENT b
LEFT JOIN Labour l ON l.Service_Ticket_ID = b.Service_Ticket_ID
LEFT JOIN Parts pr ON pr.Service_Ticket_ID = b.Service_Ticket_ID
ORDER BY b.Bill_ID;
