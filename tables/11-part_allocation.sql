-- tables/11-part_allocation.sql
IF OBJECT_ID(N'dbo.PART_ALLOCATION', 'U') IS NULL
    BEGIN
        CREATE TABLE PART_ALLOCATION (
            Allocated_ID         INT            NOT NULL,
            Procedure_ID         INT            NOT NULL,
            Quantity_Allocated   INT            NOT NULL,
            Locked_Unit_Price    DECIMAL(10,2)  NOT NULL,   -- price frozen at time of allocation
            Allocated_Time       DATETIME       NOT NULL,
            Part_Code            VARCHAR(12)    NOT NULL,
            PRIMARY KEY (Allocated_ID, Procedure_ID),
            CONSTRAINT CK_Alloc_Qty CHECK (Quantity_Allocated > 0),
            CONSTRAINT CK_Alloc_Price CHECK (Locked_Unit_Price >= 0),
            FOREIGN KEY (Procedure_ID) REFERENCES REPAIR_PROCEDURE(Procedure_ID)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (Part_Code) REFERENCES PART(Part_Code)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
