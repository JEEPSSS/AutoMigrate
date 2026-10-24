-- tables/07-diagnostic_assessment.sql
IF OBJECT_ID(N'dbo.DIAGNOSTIC_ASSESSMENT', 'U') IS NULL
    BEGIN
        CREATE TABLE DIAGNOSTIC_ASSESSMENT (
            Assessment_ID          INT           NOT NULL,
            Health_Results         VARCHAR(30)   NOT NULL,
            Diagnostic_Error_Code  VARCHAR(20)   NULL,
            Action                 VARCHAR(200)  NOT NULL,
            Service_Ticket_ID      INT           NOT NULL,
            Technician_ID          INT           NOT NULL,
            PRIMARY KEY (Assessment_ID),
            CONSTRAINT UQ_Assess_Ticket UNIQUE (Service_Ticket_ID),   -- one assessment per ticket
            CONSTRAINT CK_Assess_Health CHECK (Health_Results IN
                ('Normal','Liquid Damage','Tripped','Battery Degraded','Physical Damage')),
            FOREIGN KEY (Service_Ticket_ID) REFERENCES SERVICE_TICKET(Service_Ticket_ID)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (Technician_ID) REFERENCES TECHNICIAN(Technician_ID)
                ON DELETE NO ACTION ON UPDATE NO ACTION
        );
    END
