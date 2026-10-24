-- tables/09-work_session.sql
IF OBJECT_ID(N'dbo.WORK_SESSION', 'U') IS NULL
    BEGIN
        CREATE TABLE WORK_SESSION (
            Session_ID      INT       NOT NULL,
            Start_Time      DATETIME  NOT NULL,
            End_Time        DATETIME  NOT NULL,
            Billable_Time   INT       NOT NULL,     -- minutes
            Procedure_ID    INT       NOT NULL,
            Technician_ID   INT       NOT NULL,
            PRIMARY KEY (Session_ID),
            CONSTRAINT CK_Session_Times CHECK (End_Time > Start_Time),
            CONSTRAINT CK_Session_Billable CHECK (Billable_Time > 0),
            FOREIGN KEY (Procedure_ID)  REFERENCES REPAIR_PROCEDURE(Procedure_ID)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (Technician_ID) REFERENCES TECHNICIAN(Technician_ID)
                ON DELETE NO ACTION ON UPDATE NO ACTION
        );
    END
