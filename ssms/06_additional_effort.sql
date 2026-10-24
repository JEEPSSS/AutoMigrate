/* SC2207 Lab 5 - TEL3 Team 3 - 06_additional_effort.sql */

/* A1. Bill integrity check: recompute every bill from work sessions and locked part prices.
       Every row should show Labour_OK = 'Y' and Parts_OK = 'Y'. */
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

/* A2. Restock alert: parts at or below reorder threshold, with any open purchase order covering them. */
SELECT p.Part_Code, p.Item_Description, p.Current_Quantity, p.Minimum_Reorder_Quantity,
       rr.Req_ID, po.Order_ID, po.Order_Status, po.Expected_Delivery_Date, v.Name AS Vendor
FROM PART p
LEFT JOIN RESTOCK_REQUEST rr ON rr.Part_Code = p.Part_Code
LEFT JOIN CREATES cr         ON cr.Req_ID = rr.Req_ID
LEFT JOIN PURCHASE_ORDER po  ON po.Order_ID = cr.Order_ID AND po.Order_Status <> 'Received'
LEFT JOIN VENDOR v           ON v.Vendor_ID = po.Vendor_ID
WHERE p.Current_Quantity <= p.Minimum_Reorder_Quantity
  AND (po.Order_ID IS NOT NULL OR rr.Req_ID IS NULL)
ORDER BY p.Current_Quantity;

/* A3. Warranty claims still inside the 90-day store warranty window at submission (data-quality check).
       Every claim should show Within_90_Days = 'Y'. */
SELECT wc.Claim_ID, b.Billing_Date, wc.Submission_Date,
       DATEDIFF(DAY, b.Billing_Date, wc.Submission_Date) AS Days_After_Billing,
       CASE WHEN DATEDIFF(DAY, b.Billing_Date, wc.Submission_Date) BETWEEN 0 AND 90 THEN 'Y' ELSE 'N' END AS Within_90_Days
FROM WARRANTY_CLAIM wc
JOIN BILLING_STATEMENT b ON b.Bill_ID = wc.Bill_ID
ORDER BY wc.Claim_ID;
