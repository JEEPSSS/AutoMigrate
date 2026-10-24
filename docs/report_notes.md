# Lab 5 report notes — TEL3 Team 3 (TechPulse)

Use these sections verbatim in Lab5_TEL3_Team3.pdf.

## Team (cover page — names exactly as on student cards)
- KALAISELVAN SANJEEV (U2322159B)
- SEOW JIA XIAN (U2322995F)
- WONG YONG KANG, NIGEL (U2540457E)
- WENG SITING (U2540717D)
- YOU HANYUE (U2410731B)
- SETHI MEHAR (U2323314H)
- SETHI KAVYA (U2323682C)

Lab group: TEL3 · Team: 3 · Course: SC2207 Introduction to Databases

## Changes from Lab 3 (following TA feedback)
1. **Redundant relationships removed.** SERVICE_TICKET no longer stores Client_ID because the client is reached through DEVICE (Device_ID → Client_ID). WARRANTY_CLAIM no longer stores Client_ID because it is reached through BILLING_STATEMENT → SERVICE_TICKET → DEVICE.
2. **GENERATES dropped.** Each service ticket has at most one bill, so BILLING_STATEMENT now holds Service_Ticket_ID directly (UNIQUE foreign key). This was already implied by the Lab 3 FD Bill_ID → …, Service_Ticket_ID.
3. **DEVICE.IMEI_Serial_No added** as a UNIQUE candidate key: the real-world identifier from our Lab 1 assumption. It is a key, so the relation stays in BCNF.
4. **TECHNICIAN.Name added** for readable output.
5. **SERVICE_TICKET.Warranty_Claim_ID added** (nullable FK). A warranty rework job points to the claim that caused it, which Q5 needs to recognise warranty jobs. Warranty_Claim_ID depends only on the key, so BCNF holds.
6. **PROCEDURE renamed REPAIR_PROCEDURE** because PROCEDURE is a reserved word in T-SQL.
7. Tables are grouped by requirement (1 Intake, 2 Workshop, 3 Repair/Labour, 4 Inventory, 5 Billing/Warranty), as the TA suggested.

## Assumptions used by the queries
- Billable_Time and Total_Time_Spent are in minutes. Total_Time_Spent = SUM of the procedure's work sessions.
- Labour fee for a session = Billable_Time / 60 × the technician's Standard_Hourly_Billing_Rate.
- A work order is **completed** once a BILLING_STATEMENT exists for it. The spec says a bill is generated only when all procedures are finished.
- Revenue figures (Q2) are before GST and discounts, so labour and parts can be compared directly.
- A technician is **mismatched** when Primary_Specialisation ≠ Procedure_Type (our Lab 1 assumption).
- "Liquid Damage" and "Tripped" are values of DIAGNOSTIC_ASSESSMENT.Health_Results. "Payout requested" = Requested_Refund_Value.
- A **warranty job** is a ticket whose Warranty_Claim_ID is not NULL. A **corporate job** is a ticket whose device belongs to a CLIENT with Type = 'Corporate'.

## Query explanations (each under 150 words)

**Q1.** The CTE sums each procedure's work-session minutes (γ Procedure_ID; SUM(Billable_Time)) and keeps only procedures on finished tickets (Ready for Pickup / Completed). A procedure counts as finished only when its ticket is done. The main query joins each procedure to its ticket's workstation and to the device's category (via DEVICE → DEVICE_TYPE), keeps procedures with total time < 180 minutes, and groups by workstation and category to count them. The Micro-Soldering Desk (3) does not appear because logic-board jobs in our data all ran 180 minutes or more.

**Q2.** Completed work orders are tickets that have a billing statement. Labour and parts are aggregated per ticket in two separate CTEs *before* joining. Joining work sessions and part allocations together would multiply rows: two sessions × two parts would double-count both. Labour = Σ(Billable_Time/60 × hourly rate). Parts = Σ(Quantity × Locked_Unit_Price), the price frozen at allocation, so later catalogue price changes do not alter revenue. The per-ticket totals are then grouped by device category.

**Q3.** MismatchTickets finds tickets with at least one work session where the technician's Primary_Specialisation differs from the procedure's Procedure_Type. AffectedCustomers is the set of clients who filed a warranty claim on one of those tickets. For each affected customer, *all* their warranty claims are then counted and grouped by device manufacturer. Priya Raman, for example, has 2 Sony claims (from a mismatched headphone repair) and 1 Samsung claim.

**Q4.** Each warranty claim is traced back through BILLING_STATEMENT → SERVICE_TICKET to that ticket's DIAGNOSTIC_ASSESSMENT. Only claims whose initial assessment recorded Health_Results = 'Liquid Damage' or 'Tripped' are kept. The rows are grouped by customer (name, email) to count claims and sum Requested_Refund_Value. The approved total is shown alongside for comparison.

**Q5.** An INSTEAD OF INSERT trigger on PART_ALLOCATION enforces the rule. For each new allocation it checks whether the part's Current_Quantity < 20% of Minimum_Reorder_Quantity. If so, it blocks the insert (RAISERROR + ROLLBACK) unless the client is Corporate or the ticket is a warranty job (Warranty_Claim_ID not NULL). Allowed rows are inserted with Locked_Unit_Price copied from PART.Selling_Price at that moment, which also enforces the price-lock rule, and stock is deducted. In the demo, BAT-IP15 has 3 units (threshold 20, so the restricted level is below 4). The Northwind (corporate) and Hannah Goh (warranty rework) allocations succeed and stock drops 3 → 1. Sophie Ong's retail allocation is rejected with an error.

**Q6.** Each ticket is tagged with its client, device category and the year/month it was received. Grouping by client, category, year and month with HAVING COUNT(*) > 3 keeps only groups of four or more work orders. STRING_AGG lists the IMEI/serial numbers in each group. Lumen Design (3 phones in Aug) is excluded because 3 is not more than three. Client Tan Wei Ming (4 tickets in Aug but in 4 different categories) is also excluded.

## Additional effort
- CHECK constraints on every status, category, price and quantity column; UNIQUE constraints on Email, IMEI, one assessment per ticket, and one bill per ticket.
- ON DELETE / ON UPDATE actions chosen per relationship. For example, deleting a ticket cascades to its procedures, sessions and assessment, while deleting a client is blocked if they still have devices.
- Trigger trg_PartAllocation_Guard enforces both the Q5 stock reservation rule and the locked-in price rule automatically.
- Derived values are consistent: every bill's labour and parts totals were recomputed from raw sessions and allocations (06_additional_effort.sql, A1). All 40 bills match.
- Restock alert query (A2) and 90-day warranty-window validation (A3).
- Realistic Singapore data: 15 clients (3 corporate), 39 devices, 45 tickets, 52 procedures, 70 work sessions, 46 part allocations, 40 bills and 15 warranty claims. It includes deliberate boundary cases for Q6.
