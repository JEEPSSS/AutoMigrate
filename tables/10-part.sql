-- tables/10-part.sql
IF OBJECT_ID(N'dbo.PART', 'U') IS NULL
    BEGIN
        CREATE TABLE PART (
            Part_Code                  VARCHAR(12)    NOT NULL,
            Item_Description           VARCHAR(100)   NOT NULL,
            Selling_Price              DECIMAL(10,2)  NOT NULL,
            Minimum_Reorder_Quantity   INT            NOT NULL,
            Part_Category              VARCHAR(20)    NOT NULL,
            Current_Quantity           INT            NOT NULL,
            PRIMARY KEY (Part_Code),
            CONSTRAINT CK_Part_Category CHECK (Part_Category IN
                ('Displays','Batteries','Audio Drivers','Enclosures','Flex Cables')),
            CONSTRAINT CK_Part_Price CHECK (Selling_Price > 0),
            CONSTRAINT CK_Part_Qty CHECK (Current_Quantity >= 0 AND Minimum_Reorder_Quantity >= 0)
        );
    END
