-- triggers/01-trg_part_allocation_guard.sql
-- Q5 rule + locked-in price rule. Created AFTER seeding so historical prices are untouched.
CREATE OR ALTER TRIGGER trg_PartAllocation_Guard
ON PART_ALLOCATION
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Rule check: critically low part requested by a job that is neither corporate nor warranty
    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN PART p             ON p.Part_Code = i.Part_Code
        JOIN REPAIR_PROCEDURE rp ON rp.Procedure_ID = i.Procedure_ID
        JOIN SERVICE_TICKET st  ON st.Service_Ticket_ID = rp.Service_Ticket_ID
        JOIN DEVICE d           ON d.Device_ID = st.Device_ID
        JOIN CLIENT c           ON c.Client_ID = d.Client_ID
        WHERE p.Current_Quantity < 0.2 * p.Minimum_Reorder_Quantity
          AND c.Type <> 'Corporate'
          AND st.Warranty_Claim_ID IS NULL
    )
    BEGIN
        RAISERROR('ALLOCATION BLOCKED: stock is below 20%% of the reorder threshold. Remaining units are reserved for Corporate or Warranty jobs.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Basic stock check
    IF EXISTS (SELECT 1 FROM inserted i JOIN PART p ON p.Part_Code = i.Part_Code
               WHERE i.Quantity_Allocated > p.Current_Quantity)
    BEGIN
        RAISERROR('ALLOCATION BLOCKED: insufficient stock on hand.', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Allowed: insert with the price locked in from the catalogue right now
    INSERT INTO PART_ALLOCATION (Allocated_ID, Procedure_ID, Quantity_Allocated,
                                 Locked_Unit_Price, Allocated_Time, Part_Code)
    SELECT i.Allocated_ID, i.Procedure_ID, i.Quantity_Allocated,
           p.Selling_Price, COALESCE(i.Allocated_Time, GETDATE()), i.Part_Code
    FROM inserted i
    JOIN PART p ON p.Part_Code = i.Part_Code;

    -- Deduct stock
    UPDATE p
    SET p.Current_Quantity = p.Current_Quantity - x.Qty
    FROM PART p
    JOIN (SELECT Part_Code, SUM(Quantity_Allocated) AS Qty
          FROM inserted GROUP BY Part_Code) x ON x.Part_Code = p.Part_Code;

    PRINT 'ALLOCATION ALLOWED: part allocated and stock deducted.';
END;
