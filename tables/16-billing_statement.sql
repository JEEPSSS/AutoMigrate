-- tables/16-billing_statement.sql
IF OBJECT_ID(N'dbo.BILLING_STATEMENT', 'U') IS NULL
    BEGIN
        CREATE TABLE BILLING_STATEMENT (
            Bill_ID                 INT            NOT NULL,
            Billing_Date            DATE           NOT NULL,
            Total_Component_Costs   DECIMAL(10,2)  NOT NULL,
            Total_Labour_Charges    DECIMAL(10,2)  NOT NULL,
            Tax_Rates               DECIMAL(5,2)   NOT NULL,    -- percent, e.g. 9.00
            Discount                DECIMAL(10,2)  NOT NULL DEFAULT 0,
            Balance_Due             DECIMAL(10,2)  NOT NULL,
            Payment_Status          VARCHAR(10)    NOT NULL,
            Service_Ticket_ID       INT            NOT NULL,
            PRIMARY KEY (Bill_ID),
            CONSTRAINT UQ_Bill_Ticket UNIQUE (Service_Ticket_ID),
            CONSTRAINT CK_Bill_Status CHECK (Payment_Status IN ('Unpaid','Paid','Partial')),
            CONSTRAINT CK_Bill_Amounts CHECK (Total_Component_Costs >= 0 AND Total_Labour_Charges >= 0
                                              AND Discount >= 0 AND Balance_Due >= 0
                                              AND Tax_Rates BETWEEN 0 AND 100),
            FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
