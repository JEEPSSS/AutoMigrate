-- Devices with more than one service ticket.
SELECT d.Device_ID, d.IMEI_Serial_No, c.Name AS Client_Name,
       COUNT(*) AS Ticket_Count
FROM DEVICE d
JOIN CLIENT c ON c.Client_ID = d.Client_ID
JOIN SERVICE_TICKET st ON st.Device_ID = d.Device_ID
GROUP BY d.Device_ID, d.IMEI_Serial_No, c.Name
HAVING COUNT(*) > 1
ORDER BY Ticket_Count DESC, d.Device_ID;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.918905+08:00
+-------------+------------------+---------------+----------------+
| Device_ID   | IMEI_Serial_No   | Client_Name   | Ticket_Count   |
+=============+==================+===============+================+
| 1           | 355834859800674  | Tan Wei Ming  | 2              |
+-------------+------------------+---------------+----------------+
| 2           | HP0862776071     | Tan Wei Ming  | 2              |
+-------------+------------------+---------------+----------------+
| 7           | 358119327905235  | Lim Jia Hui   | 2              |
+-------------+------------------+---------------+----------------+
| 17          | 352443723599973  | Nur Hidayah   | 2              |
+-------------+------------------+---------------+----------------+
| 20          | 355690668435121  | Sophie Ong    | 2              |
+-------------+------------------+---------------+----------------+
| 24          | 357145848158667  | Hannah Goh    | 2              |
+-------------+------------------+---------------+----------------+
6 row(s).
*/
