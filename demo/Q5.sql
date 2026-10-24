/*
Appendix B - Q5
When a spare component's available stock drops below 20% of its minimum reorder threshold, remaining
units can only be allocated to work orders for Corporate Clients or Warranty Claims. Prepare your
SQL queries and data checks to simulate both a Success scenario (part allocation allowed for a
corporate/warranty job) and a Fail scenario (part allocation blocked for a standard retail job).

Reset the demo, check low stock and job eligibility, then try three allocations.
Corporate and warranty succeed; retail must fail; inspect the final rows and stock.
*/

/* ---------- 2. SETUP: reset demo state (safe to re-run) ---------- */
DELETE FROM PART_ALLOCATION WHERE Allocated_ID >= 9000;
UPDATE PART SET Current_Quantity = 3 WHERE Part_Code = 'BAT-IP15';
GO

/* ---------- 3. DATA CHECKS ---------- */
-- 3a. BAT-IP15 is below 20% of its reorder threshold (3 < 0.2 x 20 = 4)
SELECT Part_Code, Item_Description, Current_Quantity, Minimum_Reorder_Quantity,
       0.2 * Minimum_Reorder_Quantity AS Restricted_Below,
       CASE WHEN Current_Quantity < 0.2 * Minimum_Reorder_Quantity
            THEN 'RESTRICTED' ELSE 'OPEN' END AS Stock_Status
FROM PART
WHERE Part_Code = 'BAT-IP15';

-- 3b. Three open iPhone 15 Pro battery jobs and whether each may draw from restricted stock
SELECT st.Service_Ticket_ID, rp.Procedure_ID, c.Name AS Client_Name, c.Type AS Client_Type,
       st.Warranty_Claim_ID,
       CASE WHEN c.Type = 'Corporate' THEN 'ALLOWED (Corporate)'
            WHEN st.Warranty_Claim_ID IS NOT NULL THEN 'ALLOWED (Warranty)'
            ELSE 'BLOCKED (Retail)' END AS Expected_Result
FROM SERVICE_TICKET st
JOIN REPAIR_PROCEDURE rp ON rp.Service_Ticket_ID = st.Service_Ticket_ID
JOIN DEVICE d            ON d.Device_ID = st.Device_ID
JOIN CLIENT c            ON c.Client_ID = d.Client_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery'
ORDER BY st.Service_Ticket_ID;
GO

/* ---------- 4a. SUCCESS scenario: corporate job (Northwind Logistics) ---------- */
INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated, Locked_Unit_Price, Allocated_Time, Part_Code)
SELECT 9001, rp.Procedure_ID, 1, 0.00 /* placeholder - trigger locks catalogue price */, GETDATE(), 'BAT-IP15'
FROM REPAIR_PROCEDURE rp
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = rp.Service_Ticket_ID
JOIN DEVICE d          ON d.Device_ID = st.Device_ID
JOIN CLIENT c          ON c.Client_ID = d.Client_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery' AND c.Type = 'Corporate';
GO

/* ---------- 4b. SUCCESS scenario: warranty rework job ---------- */
INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated, Locked_Unit_Price, Allocated_Time, Part_Code)
SELECT 9002, rp.Procedure_ID, 1, 0.00, GETDATE(), 'BAT-IP15'
FROM REPAIR_PROCEDURE rp
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = rp.Service_Ticket_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery' AND st.Warranty_Claim_ID IS NOT NULL;
GO

/* ---------- 4c. FAIL scenario: standard retail job (expect error message) ---------- */
INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated, Locked_Unit_Price, Allocated_Time, Part_Code)
SELECT 9003, rp.Procedure_ID, 1, 0.00, GETDATE(), 'BAT-IP15'
FROM REPAIR_PROCEDURE rp
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = rp.Service_Ticket_ID
JOIN DEVICE d          ON d.Device_ID = st.Device_ID
JOIN CLIENT c          ON c.Client_ID = d.Client_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery'
  AND c.Type = 'Retail' AND st.Warranty_Claim_ID IS NULL;
GO

/* ---------- 5. RESULT: 9001 and 9002 exist, 9003 does not; stock went 3 -> 1 ---------- */
SELECT pa.Allocated_ID, pa.Procedure_ID, rp.Service_Ticket_ID, c.Name AS Client_Name, c.Type,
       pa.Part_Code, pa.Quantity_Allocated, pa.Locked_Unit_Price
FROM PART_ALLOCATION pa
JOIN REPAIR_PROCEDURE rp ON rp.Procedure_ID = pa.Procedure_ID
JOIN SERVICE_TICKET st   ON st.Service_Ticket_ID = rp.Service_Ticket_ID
JOIN DEVICE d            ON d.Device_ID = st.Device_ID
JOIN CLIENT c            ON c.Client_ID = d.Client_ID
WHERE pa.Allocated_ID >= 9000;

SELECT Part_Code, Current_Quantity FROM PART WHERE Part_Code = 'BAT-IP15';
GO
