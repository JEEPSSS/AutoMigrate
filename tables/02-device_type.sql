-- tables/02-device_type.sql
IF OBJECT_ID(N'dbo.DEVICE_TYPE', 'U') IS NULL
    BEGIN
        CREATE TABLE DEVICE_TYPE (
            Model_ID                        INT           NOT NULL,
            Model_Name                      VARCHAR(60)   NOT NULL,
            Device_Category                 VARCHAR(20)   NOT NULL,
            Manufacturer_Name               VARCHAR(40)   NOT NULL,
            Manufacturer_Warranty_Duration  INT           NOT NULL,   -- months
            PRIMARY KEY (Model_ID),
            CONSTRAINT CK_DeviceType_Category CHECK (Device_Category IN
                ('Smartphone','Tablet','Smartwatch','Earbuds','Headphones')),
            CONSTRAINT CK_DeviceType_Warranty CHECK (Manufacturer_Warranty_Duration >= 0)
        );
    END
