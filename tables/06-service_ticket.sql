-- tables/06-service_ticket.sql
IF OBJECT_ID(N'dbo.SERVICE_TICKET', 'U') IS NULL
    BEGIN
        CREATE TABLE SERVICE_TICKET (
            Service_Ticket_ID       INT            NOT NULL,
            Problem_Desc            VARCHAR(200)   NOT NULL,
            Status                  VARCHAR(20)    NOT NULL,
            Date_Received           DATETIME       NOT NULL,
            Estimated_Repair_Cost   DECIMAL(10,2)  NOT NULL,
            Device_ID               INT            NOT NULL,
            Workstation_ID          INT            NOT NULL,
            Warranty_Claim_ID       INT            NULL,      -- set only for warranty rework jobs
            PRIMARY KEY (Service_Ticket_ID),
            CONSTRAINT CK_Ticket_Status CHECK (Status IN
                ('Received','Diagnosing','In Progress','Ready for Pickup','Completed')),
            CONSTRAINT CK_Ticket_Est CHECK (Estimated_Repair_Cost >= 0),
            FOREIGN KEY (Device_ID)      REFERENCES DEVICE(Device_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE,
            FOREIGN KEY (Workstation_ID) REFERENCES WORKSTATION(Workstation_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
