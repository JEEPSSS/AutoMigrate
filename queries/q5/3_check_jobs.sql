-- Data check: which open battery jobs may draw from restricted stock?
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
