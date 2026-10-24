-- tables/18-fk_ticket_claim.sql
-- Rework tickets point back to the warranty claim that caused them (added last: WARRANTY_CLAIM must exist)
IF OBJECT_ID(N'dbo.FK_Ticket_Claim', 'F') IS NULL
    ALTER TABLE SERVICE_TICKET ADD CONSTRAINT FK_Ticket_Claim
        FOREIGN KEY (Warranty_Claim_ID) REFERENCES WARRANTY_CLAIM(Claim_ID)
        ON DELETE NO ACTION ON UPDATE NO ACTION;
