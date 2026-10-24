# SC2207 Lab 5 — TechPulse (TEL3 Team 3)

Database for **TechPulse**, an authorised mobile-device repair centre (SC2207 Lab Manual 2026/27 Sem 1, Appendix A/B), running on the NTU lab SQL Server.

Structure and workflow are adapted from [maxwellau2/SC2207-Lab5-AutoMigrate](https://github.com/maxwellau2/SC2207-Lab5-AutoMigrate): one SQL file per table and per seed, plus Python scripts that wipe, create, seed and query the database in one go.

## Layout

| Folder / file | What it is |
|---|---|
| `tables/` | One `CREATE TABLE` per file, run in filename order (requirement order: intake → workshop → repair → inventory → billing) |
| `seed/` | One INSERT file per table (15 clients, 39 devices, 45 tickets, 70 work sessions, 46 part allocations, 40 bills, 15 warranty claims) |
| `triggers/` | `trg_PartAllocation_Guard`: Q5 stock-reservation rule plus the locked-in-price rule. Created **after** seeding. |
| `queries/q1–q6` | Appendix B queries. `queries/q5/` is the step-by-step success/fail demo. |
| `additional/` | Extra-effort checks: bill integrity (A1), restock alert (A2), 90-day warranty window (A3) |
| `ssms/` | The same SQL as combined scripts, for running and screen-recording in SSMS |
| `docs/report_notes.md` | Changes from Lab 3, assumptions, per-query explanations (<150 words) |
| `docs/gen_data.py` | Deterministic generator the seed data came from |

## Setup

1. **Network:** be on the NTU network or connected to the NTU VPN. The server is `10.96.189.36`.
2. **ODBC driver:** install *ODBC Driver 17 (or 18) for SQL Server*.
   - Windows: Microsoft's installer.
   - Ubuntu/WSL: [Microsoft's guide](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).
   - macOS: `brew install msodbcsql17`.
3. **Config:** `cp config.example.py config.py` and fill in the team login and password. `config.py` is git-ignored, so never commit the password.
4. **Python env:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Run

```bash
python run.py test       # check the connection
python run.py all        # down -> up -> seed -> triggers  (asks for confirmation)
python run.py query      # run Q1–Q6 (+ Q5 success/fail demo) and A1–A3
python run.py export     # also writes outputs/*.csv, outputs/results.md, outputs/all_tables.md for the report
```

`make run-all`, `make query` and `make export` do the same on Linux/macOS.

> ⚠️ `down` / `all` drops **every** table in the configured database, not just TechPulse's. Check with your team before running it against a database that holds other work.

## Changes from Lab 3 (TA feedback)

- Removed redundant relationships:
  - `SERVICE_TICKET.Client_ID` (the client is reached via `DEVICE`)
  - `WARRANTY_CLAIM.Client_ID` (the client is reached via `BILLING_STATEMENT`)
  - `GENERATES` (replaced by `BILLING_STATEMENT.Service_Ticket_ID`, UNIQUE)
- Added `DEVICE.IMEI_Serial_No` (candidate key), `TECHNICIAN.Name`, and `SERVICE_TICKET.Warranty_Claim_ID` (identifies warranty rework jobs for Q5).
- Renamed `PROCEDURE` to `REPAIR_PROCEDURE`, because `PROCEDURE` is a reserved word in T-SQL.

## Expected results

- **Q1:** 10 rows.
- **Q2:** Smartphone leads with 19 orders, total 6959.60.
- **Q3:** 7 rows.
- **Q4:** 6 rows.
- **Q5:** corporate and warranty allocations are ALLOWED, the retail one is BLOCKED, and BAT-IP15 stock goes 3 → 1.
- **Q6:** Northwind (Smartphone, 03/2026) and Harbourfront (Tablet, 06/2026).
- **A1 / A3:** all rows show `Y`.
