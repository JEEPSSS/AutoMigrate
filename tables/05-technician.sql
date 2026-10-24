-- tables/05-technician.sql
IF OBJECT_ID(N'dbo.TECHNICIAN', 'U') IS NULL
    BEGIN
        CREATE TABLE TECHNICIAN (
            Technician_ID                 INT           NOT NULL,
            Name                          VARCHAR(100)  NOT NULL,
            Primary_Specialisation        VARCHAR(20)   NOT NULL,
            Certification_Level           VARCHAR(10)   NOT NULL,
            Standard_Hourly_Billing_Rate  DECIMAL(6,2)  NOT NULL,
            PRIMARY KEY (Technician_ID),
            CONSTRAINT CK_Tech_Spec CHECK (Primary_Specialisation IN
                ('Display','Battery','Audio','Logic Board','Enclosure')),
            CONSTRAINT CK_Tech_Cert CHECK (Certification_Level IN ('Junior','Senior','Expert')),
            CONSTRAINT CK_Tech_Rate CHECK (Standard_Hourly_Billing_Rate > 0)
        );
    END
