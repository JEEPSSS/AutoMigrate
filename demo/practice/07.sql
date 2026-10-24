-- P8. Approved warranty claims as a percentage of all submitted claims.
-- Under Review claims remain in the denominator.
SELECT dt.Manufacturer_Name, COUNT(*) AS Total_Claims,
       SUM(CASE WHEN wc.Review_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved,
       CAST(100.0 * SUM(CASE WHEN wc.Review_Status = 'Approved' THEN 1 ELSE 0 END)
            / COUNT(*) AS DECIMAL(6,2)) AS Approval_Rate_Percent
FROM WARRANTY_CLAIM wc
JOIN BILLING_STATEMENT b ON b.Bill_ID = wc.Bill_ID
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = b.Service_Ticket_ID
JOIN DEVICE d ON d.Device_ID = st.Device_ID
JOIN DEVICE_TYPE dt ON dt.Model_ID = d.Model_ID
GROUP BY dt.Manufacturer_Name
ORDER BY Approval_Rate_Percent DESC, dt.Manufacturer_Name;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.892367+08:00
+---------------------+----------------+------------+-------------------------+
| Manufacturer_Name   | Total_Claims   | Approved   | Approval_Rate_Percent   |
+=====================+================+============+=========================+
| Bose                | 1              | 1          | 100.00                  |
+---------------------+----------------+------------+-------------------------+
| Apple               | 4              | 3          | 75.00                   |
+---------------------+----------------+------------+-------------------------+
| Samsung             | 4              | 3          | 75.00                   |
+---------------------+----------------+------------+-------------------------+
| Sony                | 4              | 2          | 50.00                   |
+---------------------+----------------+------------+-------------------------+
| Google              | 1              | 0          | 0.00                    |
+---------------------+----------------+------------+-------------------------+
| Xiaomi              | 1              | 0          | 0.00                    |
+---------------------+----------------+------------+-------------------------+
6 row(s).
*/
