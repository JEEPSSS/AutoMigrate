-- Data check: is BAT-IP15 below 20% of its reorder threshold?
SELECT Part_Code, Item_Description, Current_Quantity, Minimum_Reorder_Quantity,
       0.2 * Minimum_Reorder_Quantity AS Restricted_Below,
       CASE WHEN Current_Quantity < 0.2 * Minimum_Reorder_Quantity
            THEN 'RESTRICTED' ELSE 'OPEN' END AS Stock_Status
FROM PART
WHERE Part_Code = 'BAT-IP15';
