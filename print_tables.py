"""Print (and with --export, save) every table's records for the report's 'printout of all table records'."""
import os
import sys
import pandas as pd
from util import get_connection

TABLES = ["CLIENT", "DEVICE_TYPE", "DEVICE", "WORKSTATION", "TECHNICIAN", "SERVICE_TICKET",
          "DIAGNOSTIC_ASSESSMENT", "REPAIR_PROCEDURE", "WORK_SESSION", "PART", "PART_ALLOCATION",
          "VENDOR", "PURCHASE_ORDER", "RESTOCK_REQUEST", "CREATES", "BILLING_STATEMENT", "WARRANTY_CLAIM"]
EXPORT = "--export" in sys.argv
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 20)

conn = get_connection()
md = ["# All table records (TEL3 Team 3)\n"]
for t in TABLES:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {t} ORDER BY 1")
    df = pd.DataFrame([list(r) for r in cur.fetchall()], columns=[c[0] for c in cur.description])
    print(f"\n=== {t} ({len(df)} rows) ===")
    print(df.to_string(index=False))
    md += [f"\n## {t} ({len(df)} rows)\n", df.to_markdown(index=False)]
conn.close()
if EXPORT:
    os.makedirs("outputs", exist_ok=True)
    with open("outputs/all_tables.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\nExported to outputs/all_tables.md ✅")
