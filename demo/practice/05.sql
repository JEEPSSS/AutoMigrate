-- P5. Vendor(s) with the largest total purchase-order value; retain ties.
SELECT TOP (1) WITH TIES v.Vendor_ID, v.Name AS Vendor_Name,
       COUNT(*) AS Purchase_Orders,
       SUM(po.Total_Order_Cost) AS Total_Order_Value
FROM VENDOR v
JOIN PURCHASE_ORDER po ON po.Vendor_ID = v.Vendor_ID
GROUP BY v.Vendor_ID, v.Name
ORDER BY SUM(po.Total_Order_Cost) DESC;

/*
Verified on 10.96.189.36 / tel3g3 at 2026-10-24T21:13:46.869150+08:00
+-------------+---------------------------+-------------------+---------------------+
| Vendor_ID   | Vendor_Name               | Purchase_Orders   | Total_Order_Value   |
+=============+===========================+===================+=====================+
| 4           | Pacific Display Solutions | 2                 | 6249.00             |
+-------------+---------------------------+-------------------+---------------------+
1 row(s).
*/
