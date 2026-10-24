-- tables/03-device.sql
IF OBJECT_ID(N'dbo.DEVICE', 'U') IS NULL
    BEGIN
        CREATE TABLE DEVICE (
            Device_ID         INT           NOT NULL,
            IMEI_Serial_No    VARCHAR(20)   NOT NULL,
            Description       VARCHAR(200)  NOT NULL,
            Colour            VARCHAR(30)   NOT NULL,
            Storage_Capacity  INT           NULL,          -- GB; NULL for audio wearables
            Model_ID          INT           NOT NULL,
            Client_ID         INT           NOT NULL,
            PRIMARY KEY (Device_ID),
            CONSTRAINT UQ_Device_IMEI UNIQUE (IMEI_Serial_No),
            CONSTRAINT CK_Device_Storage CHECK (Storage_Capacity IS NULL OR Storage_Capacity > 0),
            FOREIGN KEY (Model_ID)  REFERENCES DEVICE_TYPE(Model_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE,
            FOREIGN KEY (Client_ID) REFERENCES CLIENT(Client_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
