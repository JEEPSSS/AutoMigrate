-- A2. Restock alert: parts at or below reorder threshold, with any open purchase order covering them.
SELECT p.Part_Code, p.Item_Description, p.Current_Quantity, p.Minimum_Reorder_Quantity,
       rr.Req_ID, po.Order_ID, po.Order_Status, po.Expected_Delivery_Date, v.Name AS Vendor
FROM PART p
LEFT JOIN RESTOCK_REQUEST rr ON rr.Part_Code = p.Part_Code
LEFT JOIN CREATES cr         ON cr.Req_ID = rr.Req_ID
LEFT JOIN PURCHASE_ORDER po  ON po.Order_ID = cr.Order_ID AND po.Order_Status <> 'Received'
LEFT JOIN VENDOR v           ON v.Vendor_ID = po.Vendor_ID
WHERE p.Current_Quantity <= p.Minimum_Reorder_Quantity
  AND (po.Order_ID IS NOT NULL OR rr.Req_ID IS NULL)
ORDER BY p.Current_Quantity;
