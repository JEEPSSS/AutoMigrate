-- Reset demo state (safe to re-run)
DELETE FROM PART_ALLOCATION WHERE Allocated_ID >= 9000;
UPDATE PART SET Current_Quantity = 3 WHERE Part_Code = 'BAT-IP15';
