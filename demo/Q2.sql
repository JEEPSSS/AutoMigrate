/*
Appendix B - Q2
For each Device Category, list the total revenue generated across all completed work orders. Display
the total revenue collected from Labor Fees (derived from technician work logs) and Spare Parts
(derived from allocated parts at locked-in prices) separately.

Calculate labour and locked-price parts in separate per-ticket CTEs.
Combine those totals once per billed order, then sum by category.
*/

-- Q2. For each device category, total revenue from completed work orders, split into Labour Fees and Spare Parts.
WITH Completed AS (                     -- a bill exists only once all procedures are done
    SELECT st.Service_Ticket_ID, dt.Device_Category
    FROM SERVICE_TICKET st
    JOIN BILLING_STATEMENT b ON b.Service_Ticket_ID = st.Service_Ticket_ID
    JOIN DEVICE d            ON d.Device_ID = st.Device_ID
    JOIN DEVICE_TYPE dt      ON dt.Model_ID = d.Model_ID
),
Labour AS (
    SELECT p.Service_Ticket_ID,
           SUM(ws.Billable_Time / 60.0 * t.Standard_Hourly_Billing_Rate) AS Labour_Fee
    FROM REPAIR_PROCEDURE p
    JOIN WORK_SESSION ws ON ws.Procedure_ID = p.Procedure_ID
    JOIN TECHNICIAN t    ON t.Technician_ID = ws.Technician_ID
    GROUP BY p.Service_Ticket_ID
),
Parts AS (
    SELECT p.Service_Ticket_ID,
           SUM(pa.Quantity_Allocated * pa.Locked_Unit_Price) AS Parts_Fee
    FROM REPAIR_PROCEDURE p
    JOIN PART_ALLOCATION pa ON pa.Procedure_ID = p.Procedure_ID
    GROUP BY p.Service_Ticket_ID
)
SELECT c.Device_Category,
       COUNT(*)                                                    AS Completed_Work_Orders,
       CAST(SUM(COALESCE(l.Labour_Fee, 0)) AS DECIMAL(12,2))       AS Labour_Revenue,
       CAST(SUM(COALESCE(pr.Parts_Fee, 0)) AS DECIMAL(12,2))       AS Spare_Parts_Revenue,
       CAST(SUM(COALESCE(l.Labour_Fee, 0) + COALESCE(pr.Parts_Fee, 0)) AS DECIMAL(12,2)) AS Total_Revenue
FROM Completed c
LEFT JOIN Labour l ON l.Service_Ticket_ID = c.Service_Ticket_ID
LEFT JOIN Parts pr ON pr.Service_Ticket_ID = c.Service_Ticket_ID
GROUP BY c.Device_Category
ORDER BY Total_Revenue DESC;
