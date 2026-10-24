-- SUCCESS scenario: warranty rework job
INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated, Locked_Unit_Price, Allocated_Time, Part_Code)
SELECT 9002, rp.Procedure_ID, 1, 0.00, GETDATE(), 'BAT-IP15'
FROM REPAIR_PROCEDURE rp
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = rp.Service_Ticket_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery' AND st.Warranty_Claim_ID IS NOT NULL;
