-- tables/15-creates.sql
IF OBJECT_ID(N'dbo.CREATES', 'U') IS NULL
    BEGIN
        CREATE TABLE CREATES (            -- restock requests combined into purchase orders
            Req_ID    INT  NOT NULL,
            Order_ID  INT  NOT NULL,
            PRIMARY KEY (Req_ID, Order_ID),
            FOREIGN KEY (Req_ID)   REFERENCES RESTOCK_REQUEST(Req_ID)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (Order_ID) REFERENCES PURCHASE_ORDER(Order_ID)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    END
