-- tables/01-client.sql
IF OBJECT_ID(N'dbo.CLIENT', 'U') IS NULL
    BEGIN
        CREATE TABLE CLIENT (
            Client_ID               INT           NOT NULL,
            Name                    VARCHAR(100)  NOT NULL,
            Address                 VARCHAR(200)  NOT NULL,
            Type                    VARCHAR(10)   NOT NULL,
            Contact_Details         VARCHAR(20)   NOT NULL,
            Email                   VARCHAR(100)  NOT NULL,
            Account_Creation_Date   DATE          NOT NULL,
            PRIMARY KEY (Client_ID),
            CONSTRAINT UQ_Client_Email UNIQUE (Email),
            CONSTRAINT CK_Client_Type CHECK (Type IN ('Retail','Corporate'))
        );
    END
