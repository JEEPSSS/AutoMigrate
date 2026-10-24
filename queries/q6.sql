-- Q6. Customers with more than three work orders in the same calendar month for devices of the same category; list the IMEI/serials.
WITH TicketInfo AS (
    SELECT d.Client_ID, dt.Device_Category, d.IMEI_Serial_No,
           YEAR(st.Date_Received)  AS Yr,
           MONTH(st.Date_Received) AS Mth
    FROM SERVICE_TICKET st
    JOIN DEVICE d       ON d.Device_ID = st.Device_ID
    JOIN DEVICE_TYPE dt ON dt.Model_ID = d.Model_ID
)
SELECT c.Name AS Customer_Name, c.Email, ti.Device_Category,
       CONCAT(RIGHT(CONCAT('0', ti.Mth), 2), '/', ti.Yr) AS Month_Year,
       COUNT(*) AS Work_Orders,
       STRING_AGG(ti.IMEI_Serial_No, ', ') AS IMEI_Serial_Numbers
FROM TicketInfo ti
JOIN CLIENT c ON c.Client_ID = ti.Client_ID
GROUP BY c.Client_ID, c.Name, c.Email, ti.Device_Category, ti.Yr, ti.Mth
HAVING COUNT(*) > 3
ORDER BY c.Name, ti.Yr, ti.Mth;
