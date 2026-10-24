# TechPulse Lab 5 - live demo day

TEL3 Team 3 | NTU SQL Server `10.96.189.36`, database `tel3g3`.

## Before the lab

1. Open this repository folder in **Visual Studio Code** (`/Applications/Visual Studio Code.app`, version 1.143.1). The official Microsoft **SQL Server (mssql)** extension (`ms-mssql.mssql` 1.47.0) and Microsoft's .NET runtime helper are installed in both VS Code and Antigravity. VS Code is the tested main demo tool: Antigravity installed the extension and showed Q1, but its results preview was unreliable during automation. `.vscode/extensions.json` recommends the extensions for another machine. If VS Code shows Restricted Mode, use **Manage -> Trust** for this repository to enable the terminal tasks; do not trust unrelated folders.
2. In the repository terminal, run:

   ```bash
   git pull --ff-only
   source venv/bin/activate
   python run.py test
   ```

   If creating a new checkout, first run `python3 -m venv venv`, activate it, and `python -m pip install -r requirements.txt`. `run.py` creates the ignored local configuration from the example when needed. It asks for the SQL password with hidden input and passes it only in process memory/environment. No password is written to the configuration or repository. A second terminal may ask again.
3. Check the network using the plan below. Do not reset an already built database for the demonstration.
4. Open `demo/Q1.sql`. Click inside the SQL editor, press **Cmd+Shift+E**, choose **TechPulse tel3g3**, and enter the shared SQL password when prompted. The connection uses SQL Login `tel3g3`, database `tel3g3`, TLS encryption Mandatory and Trust Server Certificate true. The saved profile contains no password and `savePassword` is false. A file can need its own connection selection; reuse the same named profile.
5. Wait for the connection to finish. If connecting does not also execute the query, press **Cmd+Shift+E** once more after the server status appears. Check that the connection banner/status bar says **10.96.189.36 / tel3g3**. Show **Query Results** and its **Messages** tab. If a keyboard shortcut is intercepted, use **Cmd+Shift+P -> MS SQL: Execute Query**, or click the editor's green Execute Query button.
   If the preview stays empty after execution, use **Cmd+Shift+P -> Developer: Reload Window**, reconnect, and execute again. This resolved a stale preview during the dry run. The preview renderer is enabled in this Mac's VS Code user settings (`mssql.preview.betaResultsGrid: true`); its alternative renderer gave an empty pane in this installation. Keep the terminal backup ready.
6. Editor and results font size is 18; terminal size is 17. Hide the Agent pane with **Option+Cmd+B**, and hide/show the Explorer with **Cmd+B** when more room is needed. Drag the Query Results divider upward to show more rows; use its maximize button if needed. Scroll horizontally for long email/serial columns.
7. Clear any text selection before executing the whole file. The extension executes a selection when one exists. Do not paste credentials into SQL, the scratch file, terminal command arguments, or screenshots.
8. Rehearse once using `python run.py demo --dry-run`. This rollback-only rehearsal leaves all server rows unchanged. The normal `demo`/`q5` command and `demo/Q5.sql` perform the documented Q5 scratch reset/replay; the reset does not rebuild the database.

The execute shortcut and connection workflow are documented in the [official Microsoft extension README](https://github.com/microsoft/vscode-mssql/blob/main/README.md). Microsoft documents [password storage and connection profiles](https://github.com/microsoft/vscode-mssql/wiki/manage-connection-profiles); this workspace instead prompts without saving the password.

## Connectivity plan

Verified on this Mac on 24 October 2026: TCP port 1433 on `10.96.189.36` is reachable and SQL authentication succeeds. The route is **utun4**, gateway/tunnel address **10.22.88.29**, for route `10.96.0.0/14`. GlobalProtect reports connected and its configured student portal is **vpngate-student.ntu.edu.sg**. This establishes that today's working path is the NTU VPN. The underlying Wi-Fi SSID was not exposed by macOS; a direct campus Wi-Fi connection was not tested remotely.

On lab day:

1. On campus, connect your Mac to **NTUSECURE**, the university's authenticated campus Wi-Fi. Follow the [official NTU macOS Wi-Fi instructions](https://www.ntu.edu.sg/docs/default-source/life-at-ntu/it-services/ntu_secure_macos.pdf?sfvrsn=ff1f1442_8) if the profile is missing. This is the Nanyang Technological University Singapore network, not a similarly named university's VPN instructions.
2. Run `python run.py test`. If it succeeds directly over campus networking, **no VPN is needed for that connection**. We have not verified direct campus access from this current location, so this test is the deciding check.
3. If direct access fails, use the already configured GlobalProtect student connection, complete NTU login/MFA, and test again. Today's verified working path is GlobalProtect, so keep it available. Off campus or on a personal hotspot, use a working internet connection plus this NTU VPN.
4. Optional diagnostic commands (no database writes):

   ```bash
   route -n get 10.96.189.36
   nc -vz -G 5 10.96.189.36 1433
   python run.py test
   ```

5. If the laptop still cannot reach SQL Server, switch to a lab PC and the SSMS fallback below. A TCP success followed by a login error is an authentication/configuration problem; a timeout is a network/path problem. Do not change the team's shared password.

## What each member presents

All seven members should understand every query. These are suggested speaking roles, not contribution claims. For Q1-Q4 and Q6, open the indicated file, click inside it, clear the selection, press **Cmd+Shift+E**, then show the returned grid.

| Query | Presenter | File | What to say | Verified output |
|---|---|---|---|---|
| Q1 | KALAISELVAN SANJEEV | `demo/Q1.sql` | We sum work-session minutes once per procedure on a finished ticket. Then we count procedures below 180 minutes for each station and device category. | 10 rows; station 1 / Smartphone = 10. Micro-Soldering Desk (3) is absent. |
| Q2 | SEOW JIA XIAN | `demo/Q2.sql` | A billing statement identifies a completed order. Labour and parts are aggregated separately per ticket before joining, preventing one-to-many joins from multiplying charges. | 5 rows; Smartphone first, 19 orders, labour 3597.92, parts 3361.68, total 6959.60. |
| Q3 | WONG YONG KANG, NIGEL | `demo/Q3.sql` | First identify customers with a claim after a technician worked outside the repair task's specialisation. Then count all claims from each affected customer, grouped by manufacturer. | 7 rows; Priya Raman has Samsung 1 and Sony 2. |
| Q4 | WENG SITING | `demo/Q4.sql` | Follow each claim back to its original diagnosis and retain Liquid Damage or Tripped. Count the claims and sum requested refunds per customer, keeping approved payouts separate. | 6 rows; Rajesh Kumar first, requested 280.00, approved 0.00. |
| Q5 first half | YOU HANYUE | `demo/Q5a.sql` | BAT-IP15 has stock 3 against reorder threshold 20, so 3 is below 20% of 20 = 4. Corporate ticket 43 and warranty ticket 45 are eligible; both allocations succeed. | Part check RESTRICTED; jobs 43 allowed, 44 blocked, 45 allowed; two ALLOWED messages. |
| Q5 second half | SETHI MEHAR | `demo/Q5b.sql`, then `demo/Q5c.sql` | The retail allocation must be rejected by the INSTEAD OF trigger. Show the actual error, then the final allocation rows and remaining stock. | BLOCKED error; IDs 9001 and 9002 only, locked price 79.00 each; stock 1. |
| Q6 | SETHI KAVYA | `demo/Q6.sql` | Group by customer, category and calendar month/year. HAVING COUNT(*) > 3 keeps groups of at least four orders; STRING_AGG lists their serial numbers. | 2 rows: Harbourfront Consulting Pte Ltd / Tablet / 06/2026 / 4; Northwind Logistics Pte Ltd / Smartphone / 03/2026 / 5. |

The full Q5 flow is also in `demo/Q5.sql`, copied without changing SQL from sections 2-5 of the SSMS script; it does not recreate the trigger. The full file was verified in VS Code: Messages showed the BLOCKED error and the following SELECTs still produced grids. You can also use **Q5a -> Q5b -> Q5c** for the suggested two-speaker sequence: the separate Q5c SELECTs remain runnable even if the extension stops execution after the expected error in Q5b. Switch to **Messages** after Q5b. The extra transaction-ended-in-trigger diagnostic may appear and is normal; the important error contains `ALLOCATION BLOCKED: stock is below 20%`.

Q5 resets its own prepared demonstration state before replaying, so the prepared dataset can be demonstrated repeatedly. Its supplied reset deletes allocation IDs **>= 9000** and sets BAT-IP15 stock to 3; reserve those IDs for the demo and do not run it while another member is editing that state. It does not restore unrelated arbitrary edits or make `reset` safe. The usual end state is 48 allocations total (46 seeded plus the 2 successful demo rows) and BAT-IP15 stock 1.

## Terminal backup and additional effort

From the activated repository terminal:

```bash
python run.py demo                    # full SQL, results, Enter between Q1-Q6
python run.py demo --dry-run          # rehearsal: Q5 rolls back, preserving stored data
python run.py q1
python run.py q2
python run.py q3
python run.py q4
python run.py q5                      # applies the original Q5 reset/replay
python run.py q5 --dry-run            # rollback-only Q5 rehearsal
python run.py q6
python run.py sql "SELECT COUNT(*) AS Tickets FROM SERVICE_TICKET;"
python run.py sql demo/EXTRA_scratch.sql
```

The ad-hoc runner supports multiple result sets and SSMS-style standalone `GO` batches. Errors other than Q5's specifically expected rejection cause a failure exit code. Money is printed as returned by SQL Server, retaining decimal precision and NULL values.

In a rollback-only Q5 rehearsal, the original reset and two successful inserts execute inside an outer transaction. The retail trigger's ROLLBACK restores the original stored rows; the final SELECTs show that original state. With the current prepared database this is also IDs 9001/9002 and stock 1. This mode demonstrates the trigger without committing demo timestamps or stock changes. The normal mode uses the original autocommit flow.

For Command Palette tasks: **Cmd+Shift+P -> Tasks: Run Task**, then select **Demo all queries**, **Run Q1** through **Run Q6**, **Reset database**, or **Export outputs**. The task uses `venv/bin/python` even if the terminal has not activated the venv. Password input is hidden and not saved. Export outputs uses the original runner's Q5 replay as part of its export, so it also changes the prepared demo state.

`python run.py reset` and the Reset database task are the destructive showcase: they drop all tables and rebuild/seed/install the trigger. They display a large warning and require the exact phrase **RESET tel3g3**; any other input cancels before connecting. Do not confirm it during the TA demo or against existing team work without a fresh backup and team approval. The command is implemented, but this task's dry run tests its cancellation path rather than rebuilding a database the user asked to preserve. `all` has the same protection.

## The unseen extra query

Open `demo/EXTRA_scratch.sql`. Its comment lists all 17 tables and the key join paths. Ask what one output row represents, identify the starting table, add only required joins, filter rows with WHERE, and group at the requested grain. Use HAVING only for conditions on grouped totals. Aggregate independent child collections separately to avoid fan-out.

Write the query below the comment, save, connect to TechPulse tel3g3, and press **Cmd+Shift+E**. If the grid is unavailable, run `python run.py sql demo/EXTRA_scratch.sql`. A short statement can be passed as one quoted argument to `python run.py sql "SELECT ..."`. Prefer the file form for long SQL, quoted strings, or several statements. Never run a scratch DROP/DELETE/UPDATE just to adjust an answer.

Ten practice solutions, each with actual server output in its final comment:

| File | Question | Verified result |
|---|---|---|
| `demo/practice/01.sql` | Top technician by billable hours | Evelyn Chua, 18.00 hours; 1 row. |
| `demo/practice/02.sql` | Recorded unpaid/partial bill amounts by client | 2 rows; Sophie Ong 683.07, Muhammad Faris 465.34. There is no payment ledger, so these are stored invoice balances rather than calculated remaining partial-payment receivables. |
| `demo/practice/03.sql` | Low-stock parts with no pending/shipped purchase order | 0 rows, which is the verified answer. |
| `demo/practice/04.sql` | Mean received-to-billed calendar days by category | 5 rows; Tablet 1.57 days is highest. DATEDIFF counts calendar-day boundaries. |
| `demo/practice/05.sql` | Highest total purchase-order value by vendor | Pacific Display Solutions, 2 orders, 6249.00; 1 row. |
| `demo/practice/06.sql` | Monthly billed revenue in 2026 | 9 months; June total 2968.98. Before tax/discount, not cash receipts. |
| `demo/practice/07.sql` | Approval rate per manufacturer | 6 rows; Bose 100%, Apple and Samsung 75%. Under Review stays in the denominator. |
| `demo/practice/08.sql` | Devices with more than one ticket | 6 rows; each has 2 tickets. |
| `demo/practice/09.sql` | Technicians who never worked outside their specialisation | 6 rows; require at least one session. |
| `demo/practice/10.sql` | Busiest workstation by assigned tickets | Station 1, ESD-Safe Mobile Bench, 20 tickets. |

## Likely TA questions

- **Why separate labour and parts in Q2?** Joining two sessions with three allocations creates six rows. Aggregating each child to one row per ticket first avoids counting the same charge repeatedly.
- **How do locked prices protect history?** PART_ALLOCATION stores Locked_Unit_Price at allocation time. Historical revenue reads that stored value instead of the current PART.Selling_Price. The INSERT trigger sets it from the catalogue for new allocations.
- **Why INSTEAD OF rather than AFTER?** INSTEAD OF replaces the attempted insert, allowing validation and a price-controlled insert. AFTER runs after the action and relevant constraints succeed; it can also reject a transaction, but is not how this implementation supplies the price.
- **What redundant relationships did the TA ask us to fix?** Client ownership is derived through DEVICE, so it is not duplicated in SERVICE_TICKET or WARRANTY_CLAIM. GENERATES is replaced by BILLING_STATEMENT.Service_Ticket_ID, a UNIQUE foreign key modelling at most one bill per ticket.
- **Why HAVING COUNT(*) > 3?** More than three means four or more. HAVING filters groups after aggregation; WHERE filters rows before grouping. Including year and category prevents different years/categories from being merged.
- **CASCADE versus NO ACTION?** Ticket deletion can cascade to its assessment, procedures, sessions and allocations. Other foreign keys can still block it: a bill references its ticket with NO ACTION, and a client with devices cannot simply be deleted. CASCADE does not override those constraints.
- **Why is the Micro-Soldering Desk missing in Q1?** Its completed logic-board procedures all took at least 180 billable minutes and fail the strict less-than filter. This query reports qualifying groups rather than a zero-filled list of every station.
- **Why add Warranty_Claim_ID to SERVICE_TICKET?** It marks a new warranty rework ticket by linking to the claim that caused it. Q5 needs that link to recognise a warranty job. Normal tickets leave it NULL.
- **Why is Q3 compared against Procedure_Type?** It is the project's recorded assumption: technician specialisations Display/Battery/Audio align with repair task types, rather than directly with Smartphone/Tablet device categories.
- **Why are there 48 allocations when the seed notes say 46?** Two successful Q5 demonstration allocations are added to the 46 seed records. Retail 9003 is rejected.
- **Does Q2 measure cash collected?** No. It measures completed-order labour and parts charges before tax/discount; payment status is separate. The schema has no receipt ledger.
- **Why create the trigger after seeding?** Historic allocations already contain locked prices, and seed stock is the starting post-history snapshot. Applying the live trigger during seeding would replace historical prices and deduct stock twice.

## SSMS fallback on the lab PC

1. Open SSMS on the lab PC connected to the lab network. Use server `10.96.189.36`, SQL Server Authentication, login `tel3g3`, database `tel3g3`, and the shared password. Select Encryption Optional if required by the lab configuration; Trust Server Certificate is enabled where needed.
2. Use the existing database. **Do not run** `ssms/01_create_tables.sql` or `ssms/02_insert_data.sql` as part of a demo of an already built database.
3. Open `ssms/03_queries.sql`. Highlight the Q1 block, press **F5**, and show the grid; repeat for Q2-Q4 and Q6. Selecting only one query avoids executing unintended blocks.
4. For Q5, open `ssms/04_q5_trigger_demo.sql`, select sections **2-5** only, and press F5. The trigger already exists. Show the success grids, the retail BLOCKED message, and the final two allocations/stock. If execution stops after the expected error, select section 5 alone and run it.
5. For additional effort, open `ssms/06_additional_effort.sql`. For the unseen query, open a new query window on tel3g3 and use the join-path notes in `demo/EXTRA_scratch.sql`.
6. Keep a local copy of the repo/scripts before lab day; do not depend on downloading GitHub files during the timed demo. If the lab PC cannot authenticate or reach the lab server, ask the lab executive about connectivity/account access, rather than asking the TA to check solution correctness.

## End-of-demo check

All seven members spoke, Q1-Q6 ran, Q5's expected error and final results were shown, and one extra query was solved live. Do not reset/drop tables just to clean up. Never commit config.py or a password. See `docs/DEMO_DRY_RUN.md` for the actual verification record. The separate submission PDF still needs the physically signed Appendix C scan before submission.
