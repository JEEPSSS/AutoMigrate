-- tables/17-warranty_claim.sql
IF OBJECT_ID(N'dbo.WARRANTY_CLAIM', 'U') IS NULL
    BEGIN
        CREATE TABLE WARRANTY_CLAIM (
            Claim_ID                 INT            NOT NULL,
            Fault_Description        VARCHAR(200)   NOT NULL,
            Review_Status            VARCHAR(15)    NOT NULL,
            Approved_Refund_Value    DECIMAL(10,2)  NULL,
            Requested_Refund_Value   DECIMAL(10,2)  NOT NULL,
            Approved_Remedy          VARCHAR(100)   NULL,
            Submission_Date          DATE           NOT NULL,
            Bill_ID                  INT            NOT NULL,
            PRIMARY KEY (Claim_ID),
            CONSTRAINT CK_Claim_Status CHECK (Review_Status IN ('Under Review','Approved','Rejected')),
            CONSTRAINT CK_Claim_Values CHECK (Requested_Refund_Value >= 0
                AND (Approved_Refund_Value IS NULL OR Approved_Refund_Value <= Requested_Refund_Value)),
            FOREIGN KEY (Bill_ID) REFERENCES BILLING_STATEMENT(Bill_ID)
                ON DELETE NO ACTION ON UPDATE CASCADE
        );
    END
