"""Run every Appendix B query (+ additional-effort checks) and print the results.
   python query.py           -> print everything
   python query.py --export  -> also write outputs/*.csv and outputs/results.md for the report"""
import os
import sys
import pandas as pd
from util import fetch_file, execute_file, try_execute_file, read_sql

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 20)
pd.set_option("display.max_colwidth", 90)

EXPORT = "--export" in sys.argv
md = ["# Lab 5 query outputs (TEL3 Team 3)\n"]


def show(name: str, title: str, cols, rows):
    df = pd.DataFrame(rows, columns=cols)
    print(f"\n{'=' * 100}\n{name}. {title}\n{'=' * 100}")
    print(df.to_string(index=False) if len(df) else "(no rows)")
    if EXPORT:
        os.makedirs("outputs", exist_ok=True)
        df.to_csv(f"outputs/{name.lower().replace(' ', '_')}.csv", index=False)
        md.append(f"\n## {name}. {title}\n")
        md.append(df.to_markdown(index=False) if len(df) else "_(no rows)_")


def first_line(path):
    return read_sql(path).splitlines()[0].lstrip("- ").split(". ", 1)[-1]


for q in ["q1", "q2", "q3", "q4"]:
    show(q.upper(), first_line(f"queries/{q}.sql"), *fetch_file(f"queries/{q}.sql"))

# ---- Q5: trigger demo (success + fail) ----
print(f"\n{'=' * 100}\nQ5. Stock < 20% of reorder threshold -> only Corporate / Warranty jobs may allocate\n{'=' * 100}")
execute_file("queries/q5/1_setup.sql", "Reset demo state:")
show("Q5 check part", "BAT-IP15 stock status", *fetch_file("queries/q5/2_check_part.sql"))
show("Q5 check jobs", "Open battery jobs and expected outcome", *fetch_file("queries/q5/3_check_jobs.sql"))
q5_log = []
for f, label in [("4_success_corporate.sql", "SUCCESS scenario - Corporate job"),
                 ("5_success_warranty.sql", "SUCCESS scenario - Warranty rework job"),
                 ("6_fail_retail.sql", "FAIL scenario - Retail job")]:
    ok, msgs = try_execute_file(f"queries/q5/{f}")
    status = "ALLOWED" if ok else "BLOCKED"
    line = f"{label}: {status} -> {' | '.join(msgs) if msgs else 'inserted'}"
    print(line)
    q5_log.append(line)
if EXPORT:
    md.append("\n## Q5 allocation attempts\n")
    md += [f"- {l}" for l in q5_log]
show("Q5 result", "Demo allocations that exist after the attempts", *fetch_file("queries/q5/7_result_allocations.sql"))
show("Q5 stock", "Remaining BAT-IP15 stock", *fetch_file("queries/q5/8_result_stock.sql"))

show("Q6", first_line("queries/q6.sql"), *fetch_file("queries/q6.sql"))

for a in ["a1", "a2", "a3"]:
    show(a.upper(), first_line(f"additional/{a}.sql"), *fetch_file(f"additional/{a}.sql"))

if EXPORT:
    with open("outputs/results.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print("\nExported to outputs/ ✅")
