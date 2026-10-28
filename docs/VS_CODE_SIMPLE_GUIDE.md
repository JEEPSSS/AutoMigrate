# AutoMigrate: a simple VS Code guide for your Mac

Start with steps 1–4. The later sections explain the commands, files and SQL words.

The database was already created and seeded on the NTU server. You normally only need to connect and run queries. GitHub stores the code and seed scripts; the [GitHub Pages site](https://jeepsss.github.io/AutoMigrate/) shows saved results. Opening the website does not run SQL.

## 1. Open the project

1. Open **Visual Studio Code** from Applications.
2. Choose **File → Open Folder…**.
3. Select this folder on your Mac:

   ```text
   /Users/sanjeevkalaiselvan/Documents/ChatGPT/database/SC2207-Lab5-TechPulse
   ```

4. You should see `run.py`, `demo`, `tables` and `seed` in the Explorer on the left. If Explorer is hidden, press **Cmd+B**.
5. If VS Code shows Restricted Mode, trust this specific project to enable its terminal tasks.

The GitHub repo is named **AutoMigrate**. Your existing local folder still has the name **SC2207-Lab5-TechPulse**; both refer to the same project.

## 2. Connect to the NTU network

Off campus, connect the existing **NTU GlobalProtect VPN** and complete login/MFA. On campus, use **NTUSECURE** and try the connection test below; use the VPN if direct access fails.

The SQL Server address is `10.96.189.36`. The working connection verified on 24 October used NTU VPN; direct campus Wi-Fi access was not verified. A timeout means a connection could not be established, not that the tables need to be recreated.

## 3. Prepare the terminal and test the connection

Choose **Terminal → New Terminal** in VS Code. Paste these commands one line at a time:

```bash
cd "/Users/sanjeevkalaiselvan/Documents/ChatGPT/database/SC2207-Lab5-TechPulse"
git pull --ff-only
source venv/bin/activate
python run.py test
```

| Command | Simple meaning |
|---|---|
| `cd "…"` | Move the terminal into the project folder. |
| `git pull --ff-only` | Download newer code from GitHub. Stop if local history cannot move forward directly; it does not reset your files. |
| `source venv/bin/activate` | Use this project's Python and installed packages. You may see `(venv)` at the start of the terminal prompt. Repeat when opening a new terminal. |
| `python run.py test` | Ask the project's runner to check SQL Server login and print the database name. It does not rebuild or seed anything. |

Enter the shared **SQL password** when asked, then press Enter. No characters appearing while you type is normal. The runner does not save that password in a file.

Success starts with:

```text
Connected ✅  database=tel3g3  login=tel3g3
```

If `venv/bin/activate` is missing, use the first-time setup section below. If the connection times out, check VPN/network access before continuing.

## 4. Run a query and see a results grid

1. Open **`demo/Q1.sql`** in the Explorer.
2. Click in the SQL editor. Clear any selected text so the whole file runs.
3. Press **Cmd+Shift+E**. This is the Microsoft SQL extension's Execute Query command.
4. If asked for a connection, choose **TechPulse tel3g3** and enter the SQL password.
5. Wait until the connection shows `10.96.189.36` and `tel3g3`. If connecting did not also run the SQL, press **Cmd+Shift+E** once more.
6. Read the **Query Results** grid below the editor. For the prepared dataset, Q1 has **10 rows**.

If the shortcut does not work, press **Cmd+Shift+P**, search for **MS SQL: Execute Query**, and select it, or use the editor's green Execute Query button. If the panel is empty after execution, use **Developer: Reload Window** from the Command Palette, reconnect and try again. Drag the results divider upward for more space.

The extension and named connection were previously set up on this Mac. If the profile is missing, use **MS SQL: Connect → Create Connection Profile** or the SQL Server connection dialog, with these values:

| Setting | Value / meaning |
|---|---|
| Profile name | `TechPulse tel3g3`: a friendly label for the saved connection. |
| Server | `10.96.189.36`: the computer running SQL Server. |
| Authentication | **SQL Login**: use the lab SQL account. |
| User name | `tel3g3`: the login account. |
| Database | `tel3g3`: your team's database on that server. |
| Encrypt | **Mandatory**. |
| Trust server certificate | **True**: the setting used for this lab server. |
| Save password | **False**: let the extension ask for it. |

The extension and Python terminal use separate connections. It is normal for each to ask for the password.

## 5. Run Q1–Q6 in order

For Q1–Q4 and Q6, open the listed file and press **Cmd+Shift+E**.

| Query | File | What it answers | Recorded result |
|---|---|---|---|
| Q1 | [`demo/Q1.sql`](../demo/Q1.sql) | How many finished procedures took under 180 minutes, by station and device category? | 10 rows. |
| Q2 | [`demo/Q2.sql`](../demo/Q2.sql) | How much labour and parts revenue came from each device category? | 5 rows; Smartphone total 6959.60. |
| Q3 | [`demo/Q3.sql`](../demo/Q3.sql) | Which customers claimed after a specialisation mismatch, and how many claims do they have per manufacturer? | 7 rows. |
| Q4 | [`demo/Q4.sql`](../demo/Q4.sql) | Which customers made water-damage claims, and how much refund did they request? | 6 rows. |
| Q5 | [`Q5a`](../demo/Q5a.sql) → [`Q5b`](../demo/Q5b.sql) → [`Q5c`](../demo/Q5c.sql) in `demo/` | Does the stock rule allow corporate/warranty jobs and block retail jobs when stock is critically low? | Two allowed allocations, one blocked attempt; final stock 1. |
| Q6 | [`demo/Q6.sql`](../demo/Q6.sql) | Which customers had more than three orders for the same category in the same month? | 2 rows. |

These are the results verified on 24 October 2026. Later database edits can change the results.

For Q5, run **Q5a**, then **Q5b**, then **Q5c**. Q5a resets the prepared demo stock and makes the two allowed allocations. Q5b deliberately tries an ineligible retail allocation: show its **BLOCKED** error in **Messages**. Q5c shows the final allocation rows and stock. That particular error is the expected demonstration result.

Q5a and the full `demo/Q5.sql` change the prepared demo data. For a rehearsal that leaves stored data unchanged, use this terminal command instead:

```bash
python run.py q5 --dry-run
```

It performs the real Q5 attempts inside a transaction and rolls them back. The final SELECTs show the original stored state. `--dry-run` applies to the runner's `demo`/`q1`–`q6` commands; it does not protect SQL run directly in the extension.

## 6. Use the terminal as another way to run SQL

Type these in the activated VS Code terminal. The terminal prints text tables; the SQL extension shows a grid. Both connect to the same lab database.

| Command | What it does |
|---|---|
| `python run.py q1` | Print Q1's question, SQL and results. Replace `q1` with `q2`, `q3`, `q4` or `q6` for another SELECT query. |
| `python run.py demo --dry-run` | Rehearse all six in order. Press Enter between questions. Q5's changes roll back. Use Ctrl+C to stop. |
| `python run.py demo` | Run the live six-query demo, including Q5's reset and committed allowed allocations. |
| `python run.py q5` | Run just the live Q5 reset and attempts; it changes the prepared demo data. |
| `python run.py sql demo/practice/01.sql` | Run the first practice solution from a file. |
| `python run.py tables` | Print the contents of all the database tables. |

For example, this asks for the number of service tickets:

```bash
python run.py sql "SELECT COUNT(*) AS Tickets FROM SERVICE_TICKET;"
```

Here, **`python`** starts Python, **`run.py`** is the project's runner, **`sql`** tells it to execute your SQL, and the quoted text is the statement to send to SQL Server.

For the TA's extra query, open [`demo/EXTRA_scratch.sql`](../demo/EXTRA_scratch.sql), write your SQL below the table/join notes, save, and use Cmd+Shift+E. The terminal alternative is:

```bash
python run.py sql demo/EXTRA_scratch.sql
```

You can also press **Cmd+Shift+P → Tasks: Run Task** and choose **Run Q1** through **Run Q6**, or **Demo all queries**. These tasks use the normal live commands, so Run Q5 and Demo all queries change Q5's demo state. Use the explicit `--dry-run` terminal commands for rollback-only rehearsal.

## 7. Understand the files and common SQL words

| File / folder | Simple meaning |
|---|---|
| `run.py` | The controller: chooses which Python script or query to run. |
| `demo/` | Presentation copies of Q1–Q6 with short explanations. |
| `demo/practice/` | Ten extra-query solutions with recorded outputs. |
| `queries/` | Original SQL queries; Q5 is also divided into individual steps here. |
| `tables/` | SQL instructions to create the table structures and relationships. |
| `seed/` | SQL instructions to insert the prepared sample data and link warranty rework tickets. |
| `triggers/` | The automatic rule that checks new part allocations, locks prices and deducts stock. |
| `config.py` | Your ignored local connection configuration; do not commit credentials. |
| `venv/` | This project's Python environment and installed packages. |
| `.vscode/` | Saved editor settings, connection details and terminal tasks. |
| `outputs/` | Local exported results. It is excluded from Git. |
| `docs/index.html` | The published website containing saved SQL, schema and results. |

| SQL word | Simple meaning |
|---|---|
| `SELECT` / `FROM` | Choose which values to show and which table to read. |
| `JOIN` | Match related rows, such as a ticket and its device. |
| `WHERE` | Keep only rows meeting a condition. |
| `GROUP BY` | Put rows into groups so you can calculate a total for each group. |
| `COUNT` / `SUM` | Count rows or add values. |
| `HAVING` | Filter groups by a calculated result, such as more than three orders. |
| `ORDER BY` | Sort the result. |
| `WITH … AS` | Give a temporary name to a query result used by the following statement (a CTE). |
| `GO` | Tell the SQL tool to send the preceding block as one batch. It is a tool separator, not a table or SQL Server statement. |
| Trigger | Code SQL Server runs automatically when a specified table operation is attempted. |
| Transaction / rollback | A group of changes / undoing those changes before they become permanent. |

## First-time setup on another Mac

Skip this if the existing environment and connection already work.

1. Install VS Code, Git and a compatible Python 3. These pinned packages support Python 3.12.
2. In a terminal, download and enter the project:

   ```bash
   git clone https://github.com/JEEPSSS/AutoMigrate.git
   cd AutoMigrate
   ```

3. Open that **AutoMigrate** folder in VS Code. In **Terminal → New Terminal**, run:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   ```

   The first command creates a project Python environment. The second uses it. The third installs the listed packages: **pyodbc** connects Python to SQL Server, **pandas** helps format/export data, and **tabulate** prints tables.

4. Install Microsoft's **ODBC Driver 17 for SQL Server** using the [official macOS installation instructions](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos#previous-versions). This is needed by the Python runner; the VS Code MSSQL extension manages its own SQL Tools Service. If you use Driver 18 instead, set `TECHPULSE_SQL_DRIVER` to `ODBC Driver 18 for SQL Server` in the terminal before running Python.
5. Open Extensions with **Cmd+Shift+X** and install **SQL Server (mssql)** by Microsoft (`ms-mssql.mssql`) and **Python** by Microsoft (`ms-python.python`). Accept the extension's runtime dependency setup if prompted.
6. Connect the network/VPN, then run `python run.py test`. The runner creates the ignored `config.py` from `config.example.py` if needed and asks for the SQL password.
7. Select the saved **TechPulse tel3g3** connection in a SQL editor, following step 4 above.

## Commands that change or rebuild data

You do not need these to connect to the existing database or read its tables.

| Command | Meaning |
|---|---|
| `python run.py up` | Create the tables and relationships. |
| `python run.py seed` | Insert the prepared sample rows into existing tables. Running it again over existing rows can cause duplicate-key errors. |
| `python run.py triggers` | Install/update the automatic part-allocation trigger. |
| `python run.py down` | Drop all user tables after its confirmation prompt. |
| `python run.py reset` or `python run.py all` | Drop all tables, create them again, insert sample data, then install the trigger. Requires the exact phrase `RESET tel3g3`. This replaces existing data. |
| `python run.py query` | Run Q1–Q6 and the additional checks, including the live Q5 changes. |
| `python run.py export` | Run the queries/checks, including live Q5, and save results and table contents under `outputs/`. It is not a read-only export. |

For normal practice, return to `python run.py test`, the SELECT queries, and `python run.py demo --dry-run`.

## If something goes wrong

| What you see | What to do |
|---|---|
| `python: command not found` or a missing Python module | Run `source venv/bin/activate` in this terminal. On a new checkout, complete first-time setup. |
| Cannot find `run.py` or `venv/bin/activate` | Open/enter the project root folder, not `docs/` or `demo/`. Create the venv if it does not exist yet. |
| `Can't open lib 'ODBC Driver 17 for SQL Server'` | Install that Microsoft ODBC driver. A working extension does not prove Python's separate ODBC driver is installed. |
| Login timeout / server unreachable | Check NTU VPN/network access. Do not rebuild the database to fix a network problem. |
| Login failed | Check server, SQL user, database and password. |
| Empty results pane | Click inside the SQL editor, clear the selection, check the connection and execute. If needed, use **Developer: Reload Window** and reconnect. |
| Q5 says `ALLOCATION BLOCKED: stock is below 20%…` | Expected for the retail attempt. Show Messages, then run Q5c to show the final rows. |

More detail: [demo-day checklist and TA answers](DEMO_DAY.md). Official references: [Microsoft MSSQL extension](https://github.com/microsoft/vscode-mssql/blob/main/README.md) and [VS Code Python environments](https://code.visualstudio.com/docs/python/environments).
