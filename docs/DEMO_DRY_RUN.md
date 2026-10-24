# Live-demo dry-run record

24 October 2026, Asia/Singapore. Target: 10.96.189.36 / tel3g3.

## Server and terminal verification

- TCP 1433 reachable through the existing NTU GlobalProtect route, utun4. SQL Server authentication and `python run.py test` passed.
- `python run.py demo --dry-run` completed Q1-Q6 in order, printing each full question/SQL/output and accepting Enter between queries. Q1/Q2/Q3/Q4/Q6 returned 10/5/7/6/2 rows.
- Q5 performed its original reset, checks and real corporate/warranty inserts inside an outer transaction. The retail insert raised the expected ALLOCATION BLOCKED error and rolled back the outer transaction. Final SELECTs still ran, returning the original prepared 9001/9002 rows and stock 1.
- `python run.py q3` passed independently. Both inline SQL and a SQL-file argument passed using the ad-hoc command.
- All ten demo/practice SELECT queries ran on tel3g3. Outputs are recorded in each file's final comment. Row counts: 1, 2, 0, 5, 1, 9, 6, 6, 6, 1.
- All 17 tables' complete sorted row hashes and row counts were compared before and after the terminal run: exactly identical, including allocation timestamps. Local evidence is in ignored outputs/live_demo_before.json and outputs/live_demo_after_terminal.json.
- Seven automated checks passed: GO parsing in strings/comments/identifiers, GO repetition, byte-for-byte preservation of the Appendix B SQL copies/Q5 partitions, and reset/all cancellation without credentials or database operations.
- The destructive reset's cancellation path was tested; no rebuild, DDL, seeding, password change, or committed server-data change was performed for this request.

## IDE verification

- Official Microsoft MSSQL extension 1.47.0 installed in Antigravity IDE 1.107.0 and official Visual Studio Code 1.143.1 (Apple Silicon). The .NET runtime helper and SQL Tools Service were installed and connected successfully.
- Saved workspace profile **TechPulse tel3g3** connected using SQL Login tel3g3, database tel3g3, Mandatory encryption and Trust Server Certificate true. It has `savePassword: false` and no password field. The extension prompted securely; a reload prompted again.
- Antigravity showed Q1's ten-row grid, but its preview became unreliable. VS Code is the main demo tool and was used to execute every Appendix B query with Cmd+Shift+E.
- VS Code visibly displayed Q1/Q2/Q3/Q4/Q6 grids with **10/5/7/6/2** rows. Q2 showed Smartphone 19 orders, labour 3597.92, parts 3361.68, total 6959.60. Q6 showed Harbourfront Tablet 06/2026 count 4 and Northwind Smartphone 03/2026 count 5.
- For Q5, an ignored temporary file wrapped the **unchanged full demo/Q5.sql** in BEGIN TRANSACTION / final conditional ROLLBACK. This preserved server data while exercising real inserts and the trigger. Messages visibly showed **ALLOCATION ALLOWED** and **Msg 50000 / ALLOCATION BLOCKED: stock is below 20%**, followed by the expected transaction-ended-in-trigger diagnostic.
- The extension **continued after the Q5 error**. Results Preview contained four result sets: initial part check (stock 3, threshold 20, restricted below 4), three job-eligibility rows, final allocations 9001/9002 at 79.00, and BAT-IP15 stock 1. The last two result grids were inspected after the error. The split Q5a/Q5b/Q5c files are also provided for the two-speaker sequence and an explicit results step.
- A stale preview occurred after a long pause. **Developer: Reload Window**, reconnecting and executing resolved it. The preview renderer remains enabled; the alternative renderer was tried and returned an empty pane. No complete Antigravity grid dry run is claimed.
- The current window may show Restricted Mode. Queries work in that mode; the user must trust this specific repository to enable workspace tasks. No global trust/security setting was disabled.

## Preservation and remaining lab-day actions

All original SQL under tables/, seed/, queries/, triggers/ and ssms/ is unchanged. Full sorted row hashes and counts for all 17 tables were identical after both the terminal and IDE rehearsals; allocation timestamps were preserved. Evidence is local and ignored under outputs/live_demo_*.json. No reset/rebuild or export replay was run against the preserved database.

On lab day, supply the SQL password in the hidden prompt, complete NTU VPN/MFA if needed, and perform the campus NTUSECURE connectivity test described in DEMO_DAY.md. Direct campus Wi-Fi access cannot be proven from this Mac's present VPN connection. The SSMS fallback and the unseen-query workflow are in the same checklist.
