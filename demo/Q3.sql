/*
Appendix B - Q3
List all customers who have filed Warranty Claims for repair jobs executed by a technician whose
specialization does not match the category of the serviced device (e.g., a technician specializing
in "Display" repairing an "Headphone" on procedure related to "Audio"). For each affected customer,
count how many total warranty claims they have filed, broken down by Device Manufacturer.

Find customers with a warranty claim after a mismatched-specialisation repair.
For those customers, count all their claims by device manufacturer.
*/

-- Q3. Customers who filed warranty claims on jobs where a technician worked on a procedure outside their specialisation; count each such customer's total claims, broken down by device manufacturer.
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
