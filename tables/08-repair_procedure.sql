-- tables/08-repair_procedure.sql
IF OBJECT_ID(N'dbo.REPAIR_PROCEDURE', 'U') IS NULL
    BEGIN
        CREATE TABLE REPAIR_PROCEDURE (
            Procedure_ID        INT           NOT NULL,
            Procedure_Type      VARCHAR(20)   NOT NULL,
            Procedure_Details   VARCHAR(200)  NOT NULL,
            Total_Time_Spent    INT           NOT NULL DEFAULT 0,   -- minutes, = SUM(WORK_SESSION.Billable_Time)
            Service_Ticket_ID   INT           NOT NULL,
            PRIMARY KEY (Procedure_ID),
            CONSTRAINT CK_Proc_Type CHECK (Procedure_Type IN
                ('Display','Battery','Audio','Logic Board','Enclosure')),
            CONSTRAINT CK_Proc_Time CHECK (Total_Time_Spent >= 0),
            FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    END
