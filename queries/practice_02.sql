-- P2. Recorded bill balances for unpaid/partial bills, grouped by client.
-- Balance_Due is the stored invoice amount. There is no payment ledger,
-- so this query cannot calculate the amount remaining after partial payments.
SELECT c.Client_ID, c.Name AS Client_Name,
       COUNT(*) AS Unsettled_Bills,
       SUM(b.Balance_Due) AS Recorded_Bill_Balance
FROM BILLING_STATEMENT b
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = b.Service_Ticket_ID
JOIN DEVICE d ON d.Device_ID = st.Device_ID
JOIN CLIENT c ON c.Client_ID = d.Client_ID
WHERE b.Payment_Status IN ('Unpaid', 'Partial')
GROUP BY c.Client_ID, c.Name
ORDER BY Recorded_Bill_Balance DESC, c.Client_ID;
