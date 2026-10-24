-- tables/13-purchase_order.sql
IF OBJECT_ID(N'dbo.PURCHASE_ORDER', 'U') IS NULL
    BEGIN
        CREATE TABLE PURCHASE_ORDER (
            Order_ID                INT            NOT NULL,
            Order_Date              DATE           NOT NULL,
            Order_Status            VARCHAR(10)    NOT NULL,
            Expected_Delivery_Date  DATE           NOT NULL,
            Total_Order_Cost        DECIMAL(12,2)  NOT NULL,
            Vendor_ID               INT            NOT NULL,
            PRIMARY KEY (Order_ID),
            CONSTRAINT CK_PO_Status CHECK (Order_Status IN ('Pending','Shipped','Received')),
            CONSTRAINT CK_PO_Dates CHECK (Expected_Delivery_Date >= Order_Date),
            CONSTRAINT CK_PO_Cost CHECK (Total_Order_Cost >= 0),
            FOREIGN KEY (Vendor_ID) REFERENCES VENDOR(Vendor_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
