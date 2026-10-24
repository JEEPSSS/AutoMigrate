/* =====================================================================
   SC2207 Lab 5 - TEL3 Team 3 - 03_queries.sql  (Appendix B, Q1-Q4, Q6)
   Q5 is in 04_q5_trigger_demo.sql
   Run each query block on its own (highlight + F5) when recording.
   ===================================================================== */

/* ---------------------------------------------------------------------
   Q1. For each repair station, count procedures that took < 180 minutes
       to complete, broken down by device category.
   --------------------------------------------------------------------- */
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


/* ---------------------------------------------------------------------
   Q2. For each device category, total revenue from completed work orders,
       split into Labour Fees and Spare Parts.
   --------------------------------------------------------------------- */
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


/* ---------------------------------------------------------------------
   Q3. Customers who filed warranty claims on jobs where a technician worked
       on a procedure outside their specialisation; count each such
       customer's total claims, broken down by device manufacturer.
   --------------------------------------------------------------------- */
WITH MismatchTickets AS (
    SELECT DISTINCT p.Service_Ticket_ID
    FROM REPAIR_PROCEDURE p
    JOIN WORK_SESSION ws ON ws.Procedure_ID = p.Procedure_ID
    JOIN TECHNICIAN t    ON t.Technician_ID = ws.Technician_ID
    WHERE t.Primary_Specialisation <> p.Procedure_Type
),
AffectedCustomers AS (
    SELECT DISTINCT d.Client_ID
    FROM WARRANTY_CLAIM wc
    JOIN BILLING_STATEMENT b ON b.Bill_ID = wc.Bill_ID
    JOIN SERVICE_TICKET st   ON st.Service_Ticket_ID = b.Service_Ticket_ID
    JOIN DEVICE d            ON d.Device_ID = st.Device_ID
    WHERE st.Service_Ticket_ID IN (SELECT Service_Ticket_ID FROM MismatchTickets)
)
SELECT c.Client_ID, c.Name AS Customer_Name, dt.Manufacturer_Name,
       COUNT(wc.Claim_ID) AS Total_Warranty_Claims
FROM AffectedCustomers ac
JOIN CLIENT c            ON c.Client_ID = ac.Client_ID
JOIN DEVICE d            ON d.Client_ID = c.Client_ID
JOIN DEVICE_TYPE dt      ON dt.Model_ID = d.Model_ID
JOIN SERVICE_TICKET st   ON st.Device_ID = d.Device_ID
JOIN BILLING_STATEMENT b ON b.Service_Ticket_ID = st.Service_Ticket_ID
JOIN WARRANTY_CLAIM wc   ON wc.Bill_ID = b.Bill_ID
GROUP BY c.Client_ID, c.Name, dt.Manufacturer_Name
ORDER BY c.Client_ID, dt.Manufacturer_Name;


/* ---------------------------------------------------------------------
   Q4. Customers with warranty claims on devices whose initial diagnostic
       showed liquid damage / tripped indicator: claim count and total
       payout requested.
   --------------------------------------------------------------------- */
SELECT c.Name AS Customer_Name, c.Email,
       COUNT(wc.Claim_ID)                                   AS Water_Damage_Claims,
       SUM(wc.Requested_Refund_Value)                       AS Total_Requested_Payout,
       SUM(COALESCE(wc.Approved_Refund_Value, 0))           AS Total_Approved_Payout
FROM WARRANTY_CLAIM wc
JOIN BILLING_STATEMENT b        ON b.Bill_ID = wc.Bill_ID
JOIN SERVICE_TICKET st          ON st.Service_Ticket_ID = b.Service_Ticket_ID
JOIN DIAGNOSTIC_ASSESSMENT da   ON da.Service_Ticket_ID = st.Service_Ticket_ID
JOIN DEVICE d                   ON d.Device_ID = st.Device_ID
JOIN CLIENT c                   ON c.Client_ID = d.Client_ID
WHERE da.Health_Results IN ('Liquid Damage', 'Tripped')
GROUP BY c.Client_ID, c.Name, c.Email
ORDER BY Total_Requested_Payout DESC;


/* ---------------------------------------------------------------------
   Q6. Customers with more than three work orders in the same calendar
       month for devices of the same category; list the IMEI/serials.
   --------------------------------------------------------------------- */
WITH TicketInfo AS (
    SELECT d.Client_ID, dt.Device_Category, d.IMEI_Serial_No,
           YEAR(st.Date_Received)  AS Yr,
           MONTH(st.Date_Received) AS Mth
    FROM SERVICE_TICKET st
    JOIN DEVICE d       ON d.Device_ID = st.Device_ID
    JOIN DEVICE_TYPE dt ON dt.Model_ID = d.Model_ID
)
SELECT c.Name AS Customer_Name, c.Email, ti.Device_Category,
       CONCAT(RIGHT(CONCAT('0', ti.Mth), 2), '/', ti.Yr) AS Month_Year,
       COUNT(*) AS Work_Orders,
       STRING_AGG(ti.IMEI_Serial_No, ', ') AS IMEI_Serial_Numbers
FROM TicketInfo ti
JOIN CLIENT c ON c.Client_ID = ti.Client_ID
GROUP BY c.Client_ID, c.Name, c.Email, ti.Device_Category, ti.Yr, ti.Mth
HAVING COUNT(*) > 3
ORDER BY c.Name, ti.Yr, ti.Mth;
