-- seed/18-ticket_claim_link.sql
-- Link warranty rework tickets to their claim (claims must exist first)
UPDATE SERVICE_TICKET SET Warranty_Claim_ID = 15 WHERE Service_Ticket_ID = 45;
