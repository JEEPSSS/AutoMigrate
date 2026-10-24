-- tables/14-restock_request.sql
IF OBJECT_ID(N'dbo.RESTOCK_REQUEST', 'U') IS NULL
    BEGIN
        CREATE TABLE RESTOCK_REQUEST (
            Req_ID        INT          NOT NULL,
            Req_Date      DATE         NOT NULL,
            Quantity_Req  INT          NOT NULL,
            Part_Code     VARCHAR(12)  NOT NULL,
            PRIMARY KEY (Req_ID),
            CONSTRAINT CK_Req_Qty CHECK (Quantity_Req > 0),
            FOREIGN KEY (Part_Code) REFERENCES PART(Part_Code)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
