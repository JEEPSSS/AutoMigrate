-- Q4. Customers with warranty claims on devices whose initial diagnostic showed liquid damage / tripped indicator: claim count and total payout requested.
SELECT c.Name AS Customer_Name, c.Email,
       COUNT(wc.Claim_ID)                                   AS Water_Damage_Claims,
       SUM(wc.Requested_Refund_Value)                       AS Total_Requested_Payout,
       SUM(COALESCE(wc.Approved_Refund_Value, 0))           AS Total_Approved_Payout
FROM WARRANTY_CLAIM wc
JOIN BILLING_STATEMENT b        ON b.Bill_ID = wc.Bill_ID
JOIN SERVICE_TICKET st          ON st.Service_Ticket_ID = b.Service_Ticket_ID
JOIN DIAGNOSTIC_ASSESSMENT da   ON da.Service_Ticket_ID = st.Service_Ticket_ID
JOIN DEVICE d                   ON d.Device_ID = st.Device_ID
JOIN CLIENT c                   ON c.Client_ID = d.Client_ID
WHERE da.Health_Results IN ('Liquid Damage', 'Tripped')
GROUP BY c.Client_ID, c.Name, c.Email
ORDER BY Total_Requested_Payout DESC;
