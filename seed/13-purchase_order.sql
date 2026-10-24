-- seed/13-purchase_order.sql (4 rows)
SET NOCOUNT ON;
INSERT INTO PURCHASE_ORDER (Order_ID, Order_Date, Order_Status, Expected_Delivery_Date, Total_Order_Cost, Vendor_ID) VALUES (1, '2026-07-16', 'Received', '2026-07-30', 3741.00, 4);
INSERT INTO PURCHASE_ORDER (Order_ID, Order_Date, Order_Status, Expected_Delivery_Date, Total_Order_Cost, Vendor_ID) VALUES (2, '2026-09-29', 'Shipped', '2026-10-27', 1890.00, 1);
INSERT INTO PURCHASE_ORDER (Order_ID, Order_Date, Order_Status, Expected_Delivery_Date, Total_Order_Cost, Vendor_ID) VALUES (3, '2026-10-03', 'Pending', '2026-10-31', 510.00, 3);
INSERT INTO PURCHASE_ORDER (Order_ID, Order_Date, Order_Status, Expected_Delivery_Date, Total_Order_Cost, Vendor_ID) VALUES (4, '2026-10-13', 'Pending', '2026-11-03', 2508.00, 4);
