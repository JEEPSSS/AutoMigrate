-- tables/04-workstation.sql
IF OBJECT_ID(N'dbo.WORKSTATION', 'U') IS NULL
    BEGIN
        CREATE TABLE WORKSTATION (
            Workstation_ID    INT          NOT NULL,
            Workstation_Type  VARCHAR(40)  NOT NULL,
            Status            VARCHAR(12)  NOT NULL,
            PRIMARY KEY (Workstation_ID),
            CONSTRAINT CK_Workstation_Status CHECK (Status IN ('Occupied','Free','Maintenance'))
        );
    END
