-- tables/12-vendor.sql
IF OBJECT_ID(N'dbo.VENDOR', 'U') IS NULL
    BEGIN
        CREATE TABLE VENDOR (
            Vendor_ID              INT           NOT NULL,
            Name                   VARCHAR(100)  NOT NULL,
            Phone_Number           VARCHAR(20)   NOT NULL,
            Email                  VARCHAR(100)  NOT NULL,
            Agreed_Payment_Terms   VARCHAR(10)   NOT NULL,
            PRIMARY KEY (Vendor_ID),
            CONSTRAINT CK_Vendor_Terms CHECK (Agreed_Payment_Terms IN ('Cash','Credit'))
        );
    END
