-- P4. Mean calendar-day boundaries from intake to billing, per category.
SELECT dt.Device_Category, COUNT(*) AS Billed_Orders,
       CAST(AVG(CAST(DATEDIFF(DAY, st.Date_Received, b.Billing_Date)
                     AS DECIMAL(10,2))) AS DECIMAL(10,2)) AS Average_Days
FROM BILLING_STATEMENT b
JOIN SERVICE_TICKET st ON st.Service_Ticket_ID = b.Service_Ticket_ID
JOIN DEVICE d ON d.Device_ID = st.Device_ID
JOIN DEVICE_TYPE dt ON dt.Model_ID = d.Model_ID
GROUP BY dt.Device_Category
ORDER BY Average_Days DESC, dt.Device_Category;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.846969+08:00
+-------------------+-----------------+----------------+
| Device_Category   | Billed_Orders   | Average_Days   |
+===================+=================+================+
| Tablet            | 7               | 1.57           |
+-------------------+-----------------+----------------+
| Headphones        | 5               | 1.00           |
+-------------------+-----------------+----------------+
| Smartphone        | 19              | 1.00           |
+-------------------+-----------------+----------------+
| Earbuds           | 5               | 0.80           |
+-------------------+-----------------+----------------+
| Smartwatch        | 4               | 0.50           |
+-------------------+-----------------+----------------+
5 row(s).
*/
