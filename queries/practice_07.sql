-- P7. Billed revenue by billing month in 2026, before tax and discounts.
-- Invoiced charges are reported; cash receipts cannot be derived without payments.
SELECT CONVERT(CHAR(7), b.Billing_Date, 120) AS Billing_Month,
       COUNT(*) AS Bills,
       SUM(b.Total_Labour_Charges) AS Labour_Revenue,
       SUM(b.Total_Component_Costs) AS Parts_Revenue,
       SUM(b.Total_Labour_Charges + b.Total_Component_Costs) AS Total_Revenue
FROM BILLING_STATEMENT b
WHERE b.Billing_Date >= '20260101' AND b.Billing_Date < '20270101'
GROUP BY CONVERT(CHAR(7), b.Billing_Date, 120)
ORDER BY Billing_Month;
