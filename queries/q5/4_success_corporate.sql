-- SUCCESS scenario: corporate job
INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated, Locked_Unit_Price, Allocated_Time, Part_Code)
SELECT 9001, rp.Procedure_ID, 1, 0.00 /* placeholder - trigger locks catalogue price */, GETDATE(), 'BAT-IP15'
FROM REPAIR_PROCEDURE rp
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = rp.Service_Ticket_ID
JOIN DEVICE d          ON d.Device_ID = st.Device_ID
JOIN CLIENT c          ON c.Client_ID = d.Client_ID
WHERE st.Status = 'In Progress' AND rp.Procedure_Type = 'Battery' AND c.Type = 'Corporate';
