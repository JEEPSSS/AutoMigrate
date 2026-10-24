-- P5. Vendor(s) with the largest total purchase-order value; retain ties.
SELECT TOP (1) WITH TIES v.Vendor_ID, v.Name AS Vendor_Name,
       COUNT(*) AS Purchase_Orders,
       SUM(po.Total_Order_Cost) AS Total_Order_Value
FROM VENDOR v
JOIN PURCHASE_ORDER po ON po.Vendor_ID = v.Vendor_ID
GROUP BY v.Vendor_ID, v.Name
ORDER BY SUM(po.Total_Order_Cost) DESC;
