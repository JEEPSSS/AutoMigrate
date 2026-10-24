/* Q5c: run last - show 9001/9002 and BAT-IP15 quantity 1.
This SELECT-only file works even if the extension stops after Q5b. */

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
