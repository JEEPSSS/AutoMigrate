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

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.823112+08:00
+-------------+----------------+-------------------+-------------------------+
| Client_ID   | Client_Name    | Unsettled_Bills   | Recorded_Bill_Balance   |
+=============+================+===================+=========================+
| 10          | Sophie Ong     | 1                 | 683.07                  |
+-------------+----------------+-------------------+-------------------------+
| 4           | Muhammad Faris | 1                 | 465.34                  |
+-------------+----------------+-------------------+-------------------------+
2 row(s).
*/
