-- P3. Parts at/below reorder level with no pending or shipped purchase order.
SELECT p.Part_Code, p.Item_Description, p.Current_Quantity,
       p.Minimum_Reorder_Quantity
FROM PART p
WHERE p.Current_Quantity <= p.Minimum_Reorder_Quantity
  AND NOT EXISTS (
      SELECT 1
      FROM RESTOCK_REQUEST rr
      JOIN CREATES cr ON cr.Req_ID = rr.Req_ID
      JOIN PURCHASE_ORDER po ON po.Order_ID = cr.Order_ID
      WHERE rr.Part_Code = p.Part_Code
        AND po.Order_Status IN ('Pending', 'Shipped')
  )
ORDER BY p.Part_Code;
