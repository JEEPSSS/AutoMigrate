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
