-- A3. Warranty claims still inside the 90-day store warranty window at submission (data-quality check). Every claim should show Within_90_Days = 'Y'.
SELECT wc.Claim_ID, b.Billing_Date, wc.Submission_Date,
       DATEDIFF(DAY, b.Billing_Date, wc.Submission_Date) AS Days_After_Billing,
       CASE WHEN DATEDIFF(DAY, b.Billing_Date, wc.Submission_Date) BETWEEN 0 AND 90 THEN 'Y' ELSE 'N' END AS Within_90_Days
FROM WARRANTY_CLAIM wc
JOIN BILLING_STATEMENT b ON b.Bill_ID = wc.Bill_ID
ORDER BY wc.Claim_ID;
